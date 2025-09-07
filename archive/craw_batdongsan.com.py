import os
import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = '/home/trungdt2/Documents/work_/gia_thue_vp_hn/chromedriver-linux64/chromedriver'
service = Service(chromedriver_path)

# Tạo user-agent ngẫu nhiên
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.68 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
]

options = Options()
options.add_argument(f"user-agent={random.choice(user_agents)}")
# options.add_argument('--headless')  # Không dùng chế độ headless nếu có vấn đề

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

output_file = "output_nhatot.com.csv"
resume_file = "resume_page.txt"

def get_card_elements():
    return driver.find_elements(
        By.XPATH,
        '//*[@id="__next"]/div/div[4]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul//li/a/div/a/div[2]/h3'
    )

def crawl_card_detail(i, card_elem):
    card_text = card_elem.text
    print(f"\n=== DÒNG {i+1}: {card_text} ===")
    driver.execute_script("arguments[0].scrollIntoView();", card_elem)
    driver.execute_script("arguments[0].click();", card_elem)

    xpath_table = '//*[@id="__next"]/div/div[4]/div[1]/div/div[4]/div'
    table_elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath_table)))
    table_text = table_elem.text

    # Quay lại trang danh sách
    driver.back()
    time.sleep(random.randint(2, 4))  # Thêm độ trễ ngẫu nhiên giữa các lần request
    wait.until(EC.presence_of_element_located((By.XPATH,
        '//*[@id="__next"]/div/div[4]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul//li/a/div/a/div[2]/h3'
    )))
    return {
        "tieu_de": card_text,
        "chi_tiet": table_text
    }

def write_header_if_needed(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["stt", "tieu_de", "chi_tiet"])
            writer.writeheader()

def read_resume_page():
    if os.path.exists(resume_file):
        with open(resume_file, "r") as f:
            return int(f.read().strip())
    return 1

def write_resume_page(page):
    with open(resume_file, "w") as f:
        f.write(str(page))

def get_next_page_url(page):
    return f"https://www.nhatot.com/thue-van-phong-mat-bang-kinh-doanh-ha-noi?page={page}"

def append_to_csv(page, i, info):
    with open(output_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["stt", "tieu_de", "chi_tiet"])
        writer.writerow({"stt": f"{page}.{i+1}", **info})

# Main process
write_header_if_needed(output_file)
start_page = read_resume_page()

page = start_page
while True:
    print(f"\n=== Đang crawl trang {page} ===")
    url = get_next_page_url(page)
    driver.get(url)
    time.sleep(random.randint(3, 5))  # Đảm bảo trang đã load hoàn toàn trước khi lấy dữ liệu

    card_elements = get_card_elements()
    if len(card_elements) == 0:
        print(f"Trang {page} không còn dữ liệu, đã crawl xong!")
        break

    for i in range(len(card_elements)):
        try:
            card_elem = card_elements[i]
            info = crawl_card_detail(i, card_elem)
            append_to_csv(page, i, info)
        except Exception as e:
            print(f"Lỗi ở trang {page}, dòng {i+1}: {e}")
            # Resume lại từ trang này lần sau
            write_resume_page(page)
            driver.quit()
            exit(1)

    # Sau khi xong trang, lưu lại page vừa xong
    write_resume_page(page + 1)
    page += 1

print("Đã crawl xong tất cả các trang!")
driver.quit()
