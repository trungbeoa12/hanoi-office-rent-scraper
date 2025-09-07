"""
WebDriver management utilities
"""
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from ..config import CHROMEDRIVER_PATH, CHROME_PROFILE_PATH, USER_AGENTS, DEFAULT_WAIT_TIME


class WebDriverManager:
    """Manages Chrome WebDriver with anti-detection features"""
    
    def __init__(self, headless=False, use_profile=False):
        self.headless = headless
        self.use_profile = use_profile
        self.driver = None
        self.wait = None
    
    def create_driver(self):
        """Create and configure Chrome WebDriver"""
        options = Options()
        
        # User agent
        options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
        
        # Chrome profile (optional)
        if self.use_profile:
            options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")
        
        # Anti-detection settings
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--window-size=1200,800")
        
        # Headless mode
        if self.headless:
            options.add_argument("--headless")
        
        # Create service and driver
        service = Service(executable_path=str(CHROMEDRIVER_PATH))
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Execute anti-detection script
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.navigator.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'languages', {get: () => ['vi-VN', 'vi']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
                """
            },
        )
        
        # Create wait object
        self.wait = WebDriverWait(self.driver, DEFAULT_WAIT_TIME)
        
        return self.driver
    
    def safe_click(self, element):
        """Safely click an element with fallback methods"""
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
    
    def scroll_to_element(self, element):
        """Scroll to element and wait a bit"""
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(0.5)
    
    def scroll_to_bottom(self, wait_time=1.2, max_scrolls=15):
        """Scroll to bottom of page to load all content"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(max_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
