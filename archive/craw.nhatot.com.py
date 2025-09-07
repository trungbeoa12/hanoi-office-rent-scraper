import csv
import os
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException

chromedriver_path = "/home/trungdt2/Documents/work_/gia_thue_vp_hn/chromedriver-linux64/chromedriver"
chrome_profile_path = "/home/trungdt2/.config/google-chrome/Default"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.68 Safari/537.36"
base_url = "https://www.nhatot.com/thue-van-phong-mat-bang-kinh-doanh-ha-noi?page={}"
csv_file = "output_nhatot.com.csv"
resume_file = "resume_page_nhatot.txt"

def save_to_csv(output, csv_file):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(output)

def scroll_to_bottom(driver, wait_time=1.2, max_scrolls=12):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def crawl_detail_page(driver):
    wait = WebDriverWait(driver, 10)
    try:
        detail_elem = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="__next"]/div/div[4]/div[1]/div/div[4]/div')
            )
        )
        data = detail_elem.text
    except Exception as e:
        print(f"Không tìm thấy block chi tiết: {e}")
        data = ""
    try:
        title = driver.find_element(By.XPATH, "//h1").text
    except:
        title = ""
    output = {
        "Tiêu đề": title,
        "Text chi tiết": data,
        "URL": driver.current_url,
    }
    save_to_csv(output, csv_file)
    print(f"Đã lưu: {title}")

def crawl_page(page_num):
    print(f"\n==== ĐANG CRAWL PAGE {page_num} ====")
    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    # options.add_argument(f"--user-data-dir={chrome_profile_path}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--window-size=1200,800")
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Fake webdriver
    driver.execute_cdp_cmd(
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

    wait = WebDriverWait(driver, 10)
    page_url = base_url.format(page_num)
    try:
        driver.get(page_url)
        time.sleep(random.uniform(2, 4))
        scroll_to_bottom(driver, wait_time=random.uniform(1, 1.5), max_scrolls=15)

        item_links = driver.find_elements(
            By.XPATH,
            '//*[@id="__next"]/div/div[4]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul//li/a'
        )
        if len(item_links) == 0:
            print(f"Page {page_num} không còn mục nào, kết thúc crawl.")
            driver.quit()
            return False

        for idx in range(len(item_links)):
            try:
                # Lấy lại link từng mục sau mỗi lần back!
                item_links = driver.find_elements(
                    By.XPATH,
                    '//*[@id="__next"]/div/div[4]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul//li/a'
                )
                elem = item_links[idx]
                driver.execute_script("arguments[0].scrollIntoView();", elem)
                time.sleep(0.5)
                try:
                    elem.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", elem)
                wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
                crawl_detail_page(driver)
                time.sleep(random.uniform(1.2, 2))
                driver.back()
                wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            '//*[@id="__next"]/div/div[4]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul//li/a'
                        )
                    )
                )
                time.sleep(0.8)
            except Exception as e:
                print(f"Lỗi page {page_num} mục {idx+1}: {e}")
                continue
        print(f"Đã xong page {page_num}")

    except Exception as e:
        print(f"Lỗi không xác định ở page {page_num}: {e}")

    driver.quit()
    return True

# Đọc resume (số trang)
if os.path.exists(resume_file):
    with open(resume_file, "r") as f:
        start_page = int(f.read().strip())
        print(f"Resume từ page {start_page}")
else:
    start_page = 1

page_num = start_page
while True:
    res = crawl_page(page_num)
    # Lưu lại trạng thái resume:
    with open(resume_file, "w") as f:
        f.write(str(page_num + 1))
    if not res:
        print("Đã hết dữ liệu hoặc bị chặn!")
        break
    page_num += 1
    # (Rất nên) thêm sleep lâu hơn ở đây để giảm bị chặn IP:
    time.sleep(random.uniform(10, 20))

print("XONG TOÀN BỘ! Xem file", csv_file)
