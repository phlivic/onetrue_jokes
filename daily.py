from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import time
import os
import json
import re

def main():
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    isFan = config.get("isFan", False)
    isLevelup = config.get("isLevelup", False)
    message = config.get("message", "")
    onetrue_lrportal = config.get("onetrue_lrportal", "https://www.douyu.com/topic/IEMMBR?rid=6979222")
    level_portal = config.get("level_portal", "https://www.douyu.com/topic/IEMMBR?rid=601514")
    
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # 设置 WebDriver 服务和启动时的选项
    chrome_options = Options()
    chrome_options.page_load_strategy = 'none'
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 5)
    actions = ActionChains(driver)
    
    try:
        driver.get(onetrue_lrportal)
        driver.maximize_window()
        input("请手动登录后，按 Enter 继续...")
        time.sleep(5)

        if isFan:
            # 点击背包按钮
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".BackpackButton"))).click()
            time.sleep(2)
            
            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".FansGiftPackage-OK"))).click()
                time.sleep(2)
            except:
                pass
            
            # 寻找荧光棒图片元素
            try:
                # 等待背包加载完成
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Backpack-propContainer")))
                
                # 查找荧光棒图片元素
                glow_stick = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//div[contains(@class, 'Backpack-propImage')]//img[contains(@src, '7db9beee246848252f1c7fe916259f4e.png')]"
                )))
                
                # 移动鼠标到荧光棒上并点击直到消失
                # 持续点击直到元素消失
                while True:
                    try:
                        actions.move_to_element(glow_stick).click().perform()
                        time.sleep(0.5)
                        # 检查元素是否还存在
                        driver.find_element(By.XPATH, "//div[contains(@class, 'Backpack-propImage')]//img[contains(@src, '7db9beee246848252f1c7fe916259f4e.png')]")
                    except:
                        print("荧光棒已全部赠送完毕")
                        break
                        
            except Exception as e:
                print(f"处理荧光棒时出错: {e}")
        time.sleep(10)
        if isLevelup:
            driver.get(level_portal)


            time.sleep(5)
            # 进行斗鱼的关注和发送一条弹幕
            follow_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Title-followText")))
            follow_btn.click()
            # <span class="dy-Modal-close-x"></span>
            time.sleep(5)
            try:
                close_modal_btn = driver.find_element(By.CSS_SELECTOR, "span.dy-Modal-close-x")
                close_modal_btn.click()
            except:
                pass

            print("已关注")
            time.sleep(5)

            #发送弹幕
            chat_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ChatSend-txt"))
            )
            chat_input.clear()
            chat_input.send_keys(message)
            chat_input.send_keys(Keys.RETURN)
            print(f"已发送: {message}")
            time.sleep(5)

            unfollow_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='已关注']")))
            actions.move_to_element(unfollow_elem).perform()
            cancel_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".CustomGroupMenu-cancel")))
            cancel_btn.click()
            # 点击弹窗确认的第一个按钮
            confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dy-Modal-footer .dy-btn")))
            confirm_btn.click()
            time.sleep(5)


            # driver.get("https://www.douyu.com/member/mylevel")
            # time.sleep(2)

            # # <div class="userLevel-getAll"></div>
            # try:
            #     get_exp = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'userLevel-getAll')))
            #     get_exp.click()
            #     time.sleep(2)
            # except:
            #     pass
            # time.sleep(10)

            # try:
            #     today_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.today")))
            #     today_text = today_div.text.strip()

            #     match = re.search(r'\d+', today_text)
            #     if match:
            #         exp_value = match.group(0)
            #         print(f"今日经验增加: {exp_value}")
            #     time.sleep(10)
            # except:
            #     pass

            driver.get(level_portal)
            end_time = time.time() + 1800
            while time.time() < end_time:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(30)

                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(30)
            
        driver.quit()
        
    except Exception as e:
        print("发生错误", e)

if __name__ == "__main__":
    main()