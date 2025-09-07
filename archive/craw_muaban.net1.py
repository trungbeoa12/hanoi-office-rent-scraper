import csv
import os
import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chromedriver_path = "/home/trungdt2/Documents/work_/gia_thue_vp_hn/chromedriver-linux64/chromedriver"
chrome_profile_path = "/home/trungdt2/.config/google-chrome/Default"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.68 Safari/537.36"
base_url = "https://muaban.net/bat-dong-san/cho-thue-van-phong-mat-bang-ha-noi?page={}"
csv_file = "output_muaban.net.csv"
resume_file = "resume_page_muaban.txt"

options = Options()
options.add_argument(f"user-agent={user_agent}")
options.add_argument(f"--user-data-dir={chrome_profile_path}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--window-size=1200,800")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
    """
    },
)


def save_to_csv(output, csv_file):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(output)


def crawl_detail_page(driver):
    wait = WebDriverWait(driver, 10)
    try:
        detail_elem = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]")
            )
        )
        data = detail_elem.text
    except Exception as e:
        print(f"Không tìm thấy block detail: {e}")
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


if os.path.exists(resume_file):
    with open(resume_file, "r") as f:
        start_page = int(f.read().strip())
        print(f"Resume từ page {start_page}")
else:
    start_page = 1

wait = WebDriverWait(driver, 10)
page_num = start_page
while True:
    print(f"\n==== ĐANG CRAWL PAGE {page_num} ====")
    page_url = base_url.format(page_num)
    driver.get(page_url)
    time.sleep(2)
    try:
        item_links = driver.find_elements(
            By.CSS_SELECTOR, "div.sc-2h9t67-0 > div:nth-child(2) > a:nth-child(1)"
        )
        if len(item_links) == 0:
            print(f"Page {page_num} không còn mục nào, kết thúc crawl.")
            break

        for idx in range(len(item_links)):
            try:
                # Sau mỗi lần back phải reload lại danh sách link!
                item_links = driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.sc-2h9t67-0 > div:nth-child(2) > a:nth-child(1)",
                )
                elem = item_links[idx]
                driver.execute_script("arguments[0].scrollIntoView();", elem)
                time.sleep(0.5)
                # Đóng popup nếu có
                try:
                    close_btn = driver.find_element(
                        By.CSS_SELECTOR, ".sc-1onxl1x-6.cvNCSg, .sc-1onxl1x-6"
                    )
                    if close_btn.is_displayed():
                        close_btn.click()
                        print("Đã đóng popup!")
                        time.sleep(0.5)
                except Exception:
                    pass
                try:
                    elem.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", elem)
                wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
                crawl_detail_page(driver)
                time.sleep(1.2)
                driver.back()
                wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.CSS_SELECTOR,
                            "div.sc-2h9t67-0 > div:nth-child(2) > a:nth-child(1)",
                        )
                    )
                )
                time.sleep(0.8)
            except Exception as e:
                print(f"Lỗi page {page_num} mục {idx+1}: {e}")
                continue

        with open(resume_file, "w") as f:
            f.write(str(page_num + 1))
        print(f"Đã lưu trạng thái resume: page {page_num + 1}")

        page_num += 1
    except Exception as e:
        print(f"Lỗi không xác định ở page {page_num}: {e}")
        break

print("XONG TOÀN BỘ! Xem file output_muaban.net.csv")
