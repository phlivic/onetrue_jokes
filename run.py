from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

search_keyword = "twistzz"
onetrue_lrportal = "https://www.douyu.com/topic/iemktwz2025?rid=6979222"
index = 1   # 循环次数

def main():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    # 设置 WebDriver 服务和启动时的选项
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://sb6657.cn/#/home")
        
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.el-input__inner"))
        )
        
        search_box.send_keys(search_keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "barrage-text"))
        )

        search_results = [result.text for result in results]
        print("烂梗已收集！")
        print(f'收集的烂梗如下：{search_results}')

        driver.get(onetrue_lrportal)
        input("请手动登录后，按 Enter 继续...")  

        chat_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ChatSend-txt"))
        )

        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ChatSend-button"))
        )

        for _ in range(index):
            for message in search_results:
                chat_input.clear()
                chat_input.send_keys(message)
                chat_input.send_keys(Keys.RETURN)
                print(f"已发送: {message}")
                time.sleep(20)

    except Exception as e:
        print("发生错误:", e)

    finally:
        driver.quit()

if __name__ == '__main__':
    main()