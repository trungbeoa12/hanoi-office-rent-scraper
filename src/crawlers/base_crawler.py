"""
Base crawler class with common functionality
"""
import time
import random
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..config import WEBSITES, CSV_FIELDS, DEFAULT_PAGE_DELAY, DEFAULT_ITEM_DELAY
from ..utils.webdriver_manager import WebDriverManager
from ..utils.csv_manager import CSVManager, ResumeManager


class BaseCrawler(ABC):
    """Base class for all crawlers"""
    
    def __init__(self, website_name, headless=False, use_profile=False):
        self.website_name = website_name
        self.config = WEBSITES[website_name]
        self.csv_fields = CSV_FIELDS[website_name]
        
        # Initialize managers
        self.driver_manager = WebDriverManager(headless=headless, use_profile=use_profile)
        self.csv_manager = CSVManager(self.config["output_file"])
        self.resume_manager = ResumeManager(self.config["resume_file"])
        
        # Initialize CSV file
        self.csv_manager.write_header_if_needed(self.csv_fields)
        
        self.driver = None
        self.wait = None
    
    def start(self):
        """Start the crawling process"""
        try:
            self.driver = self.driver_manager.create_driver()
            self.wait = self.driver_manager.wait
            
            start_page = self.resume_manager.read_resume_page()
            print(f"Starting from page {start_page}")
            
            page_num = start_page
            while True:
                print(f"\n==== CRAWLING PAGE {page_num} ====")
                
                if not self.crawl_page(page_num):
                    print(f"Page {page_num} has no data, stopping...")
                    break
                
                # Save progress
                self.resume_manager.write_resume_page(page_num + 1)
                page_num += 1
                
                # Random delay between pages
                delay = random.uniform(*DEFAULT_PAGE_DELAY)
                print(f"Waiting {delay:.1f} seconds before next page...")
                time.sleep(delay)
            
            print("Crawling completed successfully!")
            
        except Exception as e:
            print(f"Error during crawling: {e}")
            raise
        finally:
            self.driver_manager.close()
    
    def crawl_page(self, page_num):
        """Crawl a single page"""
        page_url = self.config["base_url"].format(page_num)
        self.driver.get(page_url)
        
        # Wait for page to load
        time.sleep(random.uniform(2, 4))
        
        # Scroll to load all content
        self.driver_manager.scroll_to_bottom()
        
        # Get item elements
        item_elements = self.get_item_elements()
        
        if len(item_elements) == 0:
            return False
        
        # Process each item
        for idx, item_element in enumerate(item_elements):
            try:
                self.process_item(idx, item_element)
                
                # Random delay between items
                delay = random.uniform(*DEFAULT_ITEM_DELAY)
                time.sleep(delay)
                
            except Exception as e:
                print(f"Error processing item {idx + 1} on page {page_num}: {e}")
                continue
        
        return True
    
    def process_item(self, idx, item_element):
        """Process a single item"""
        # Scroll to element
        self.driver_manager.scroll_to_element(item_element)
        
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
    
    @abstractmethod
    def get_item_elements(self):
        """Get list of item elements from current page"""
        pass
    
    @abstractmethod
    def extract_item_data(self):
        """Extract data from current detail page"""
        pass
    
    @abstractmethod
    def wait_for_listing_page(self):
        """Wait for listing page to reload after going back"""
        pass
