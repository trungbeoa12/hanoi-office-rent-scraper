"""
Configuration file for Real Estate Web Scraper
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Chrome driver configuration
CHROMEDRIVER_PATH = BASE_DIR / "chromedriver-linux64" / "chromedriver"
CHROME_PROFILE_PATH = os.path.expanduser("~/.config/google-chrome/Default")

# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.68 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.68 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.68 Safari/537.36"
]

# Scraping settings
DEFAULT_WAIT_TIME = 10
DEFAULT_SCROLL_WAIT = 1.2
DEFAULT_MAX_SCROLLS = 15
DEFAULT_PAGE_DELAY = (2, 4)  # Random delay between pages
DEFAULT_ITEM_DELAY = (1.2, 2)  # Random delay between items

# Website configurations
WEBSITES = {
    "nhatot": {
        "base_url": "https://www.nhatot.com/thue-van-phong-mat-bang-kinh-doanh-ha-noi?page={}",
        "output_file": "output_nhatot.csv",
        "resume_file": "resume_nhatot.txt",
        "item_selector": '//*[@id="__next"]/div/div[4]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul//li/a',
        "detail_selector": '//*[@id="__next"]/div/div[4]/div[1]/div/div[4]/div'
    },
    "muaban": {
        "base_url": "https://muaban.net/bat-dong-san/cho-thue-van-phong-mat-bang-ha-noi?page={}",
        "output_file": "output_muaban.csv",
        "resume_file": "resume_muaban.txt",
        "item_selector": "div.sc-2h9t67-0 > div:nth-child(2) > a:nth-child(1)",
        "detail_selector": "/html/body/div[1]/div[2]/div[2]/div[1]"
    },
    "batdongsan": {
        "base_url": "https://batdongsan.com.vn/cho-thue-nha-mat-pho-ha-noi/p{}",
        "output_file": "output_batdongsan.csv",
        "resume_file": "resume_batdongsan.txt",
        "item_selector": '//*[@id="product-lists-web"]/div[1]/a',
        "detail_selector": '//*[@id="product-detail-web"]'
    }
}

# CSV field mappings
CSV_FIELDS = {
    "nhatot": ["Tiêu đề", "Text chi tiết", "URL"],
    "muaban": ["Tiêu đề", "Text chi tiết", "URL"],
    "batdongsan": [
        "Tiêu đề", "Địa chỉ", "Mức giá", "Diện tích", "Mặt tiền", 
        "Số tầng", "Số phòng tắm, vệ sinh", "Tiện ích", "Mô tả",
        "Ngày đăng", "Ngày hết hạn", "Loại tin", "Mã tin", 
        "SĐT liên hệ", "Tên liên hệ", "URL"
    ]
}
