"""
BatDongSan.com.vn crawler implementation
"""
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_crawler import BaseCrawler


class BatDongSanCrawler(BaseCrawler):
    """Crawler for BatDongSan.com.vn website"""
    
    def __init__(self, headless=False, use_profile=False):
        super().__init__("batdongsan", headless, use_profile)
    
    def get_item_elements(self):
        """Get list of item elements from BatDongSan page"""
        return self.driver.find_elements(
            By.XPATH,
            '//*[@id="product-lists-web"]/div[1]/a'
        )
    
    def extract_item_data(self):
        """Extract detailed data from BatDongSan detail page"""
        try:
            # Wait for detail element
            detail_elem = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="product-detail-web"]')
                )
            )
            detail_text = detail_elem.text
        except Exception as e:
            print(f"Could not find detail block: {e}")
            detail_text = ""
        
        # Extract structured data using regex
        def extract_field(pattern, text, default=""):
            match = re.search(pattern, text, re.MULTILINE)
            return match.group(1).strip() if match else default
        
        lines = detail_text.splitlines()
        
        return {
            "Tiêu đề": lines[0] if lines else "",
            "Địa chỉ": lines[1] if len(lines) > 1 else "",
            "Mức giá": extract_field(r"Mức giá\n(.+)", detail_text),
            "Diện tích": extract_field(r"Diện tích\n(.+)", detail_text),
            "Mặt tiền": extract_field(r"Mặt tiền ([\d,\.]+ m)", detail_text),
            "Số tầng": extract_field(r"Số tầng\n(.+)", detail_text),
            "Số phòng tắm, vệ sinh": extract_field(r"Số phòng tắm, vệ sinh\n(.+)", detail_text),
            "Tiện ích": extract_field(r"Tiện ích\n(.+)", detail_text),
            "Mô tả": extract_field(r"Thông tin mô tả\n([\s\S]+?)\nĐặc điểm bất động sản", detail_text),
            "Ngày đăng": extract_field(r"Ngày đăng\n(.+)", detail_text),
            "Ngày hết hạn": extract_field(r"Ngày hết hạn\n(.+)", detail_text),
            "Loại tin": extract_field(r"Loại tin\n(.+)", detail_text),
            "Mã tin": extract_field(r"Mã tin\n(.+)", detail_text),
            "SĐT liên hệ": extract_field(r"SĐT liên hệ:\n([\d ]+)", detail_text),
            "Tên liên hệ": extract_field(r"SĐT liên hệ:\n.+\n\((.+)\)", detail_text)
        }
    
    def wait_for_listing_page(self):
        """Wait for BatDongSan listing page to reload"""
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="product-lists-web"]/div[1]/a')
            )
        )
