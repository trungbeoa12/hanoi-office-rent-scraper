"""
MuaBan.net crawler implementation
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_crawler import BaseCrawler


class MuabanCrawler(BaseCrawler):
    """Crawler for MuaBan.net website"""
    
    def __init__(self, headless=False, use_profile=False):
        super().__init__("muaban", headless, use_profile)
    
    def get_item_elements(self):
        """Get list of item elements from MuaBan.net page"""
        return self.driver.find_elements(
            By.CSS_SELECTOR,
            "div.sc-2h9t67-0 > div:nth-child(2) > a:nth-child(1)"
        )
    
    def extract_item_data(self):
        """Extract data from MuaBan.net detail page"""
        try:
            # Get title
            title = self.driver.find_element(By.XPATH, "//h1").text
        except:
            title = ""
        
        try:
            # Get detail content
            detail_elem = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]")
                )
            )
            detail_text = detail_elem.text
        except Exception as e:
            print(f"Could not find detail block: {e}")
            detail_text = ""
        
        return {
            "Tiêu đề": title,
            "Text chi tiết": detail_text
        }
    
    def wait_for_listing_page(self):
        """Wait for MuaBan.net listing page to reload"""
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.sc-2h9t67-0 > div:nth-child(2) > a:nth-child(1)")
            )
        )
    
    def process_item(self, idx, item_element):
        """Override to handle popup closing for MuaBan.net"""
        # Scroll to element
        self.driver_manager.scroll_to_element(item_element)
        
        # Try to close popup if exists
        try:
            close_btn = self.driver.find_element(
                By.CSS_SELECTOR, ".sc-1onxl1x-6.cvNCSg, .sc-1onxl1x-6"
            )
            if close_btn.is_displayed():
                close_btn.click()
                print("Closed popup!")
        except:
            pass
        
        # Click on item
        self.driver_manager.safe_click(item_element)
        
        # Wait for detail page to load
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
        
        # Extract data
        data = self.extract_item_data()
        data["URL"] = self.driver.current_url
        
        # Save to CSV
        self.csv_manager.append_row(data)
        print(f"Saved: {data.get('Tiêu đề', 'Unknown title')}")
        
        # Go back to listing page
        self.driver.back()
        
        # Wait for listing page to reload
        self.wait_for_listing_page()
