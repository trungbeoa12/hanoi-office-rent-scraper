"""
Nhà Tốt crawler implementation
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_crawler import BaseCrawler


class NhatotCrawler(BaseCrawler):
    """Crawler for Nhà Tốt website"""
    
    def __init__(self, headless=False, use_profile=False):
        super().__init__("nhatot", headless, use_profile)
    
    def get_item_elements(self):
        """Get list of item elements from Nhà Tốt page"""
        return self.driver.find_elements(
            By.XPATH,
            '//*[@id="__next"]/div/div[4]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul//li/a'
        )
    
    def extract_item_data(self):
        """Extract data from Nhà Tốt detail page"""
        try:
            # Get title
            title = self.driver.find_element(By.XPATH, "//h1").text
        except:
            title = ""
        
        try:
            # Get detail content
            detail_elem = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="__next"]/div/div[4]/div[1]/div/div[4]/div')
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
        """Wait for Nhà Tốt listing page to reload"""
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="__next"]/div/div[4]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul//li/a')
            )
        )
