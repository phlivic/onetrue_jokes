from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
    
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    # 设置 WebDriver 服务和启动时的选项
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 5)
    actions = ActionChains(driver)
    
    try:
        driver.get(onetrue_lrportal)
        input("请手动登录后，按 Enter 继续...")
        time.sleep(5)

        if isFan:
            # 这里要点击页面的背包按钮，重复点击里面的荧光棒直到送完所有
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".BackpackButton"))).click()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Backpack-propContainer")))
            backpack = driver.find_element(By.CSS_SELECTOR, ".Backpack-propContainer")
            # 检查背包中是否有道具
            props = backpack.find_elements(By.CSS_SELECTOR, ".gift-pack.prop-item")
            if props:
                # 查找荧光棒道具
                glow_sticks = []
                for item in props:
                    text = item.text.strip()
                    if "荧光棒" in text:
                        glow_sticks.append(item)
                # 循环赠送荧光棒（用户未提供赠送逻辑，这里预留占位）
                for stick in glow_sticks:
                    try:
                        # 假设道具项内有赠送按钮
                        send_button = stick.find_element(By.CSS_SELECTOR, ".gift-send-btn")
                        while True:
                            send_button.click()
                            time.sleep(1)  # 等待赠送请求处理
                            # 判断是否继续赠送（此处简化，直接退出循环）
                            break
                    except Exception as e:
                        print(f"赠送过程中遇到异常: {e}")
            else:
                print("背包中没有道具.")

        if isLevelup:
            driver.get(level_portal)
            time.sleep(5)
            # 进行斗鱼的关注和发送一条弹幕
            follow_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Title-followText")))
            follow_btn.click()
            # 

            #发送弹幕
            chat_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ChatSend-txt"))
            )
            chat_input.clear()
            chat_input.send_keys(message)
            chat_input.send_keys(Keys.RETURN)
            print(f"已发送: {message}")
            time.sleep(5)

            # 领取经验值
            avatar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.Avatar-img")))
            actions.move_to_element(avatar).perform()
            # <span class="HeaderUserLevel-bar-num">3.5%</span>
            # <a href="/member/mylevel"><i class="u_nav_mylevel"></i>我的等级</a>
            user_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/member/mylevel"]')))
            user_link.click()

            today_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.today")))
            today_text = today_div.text.strip()

            match = re.search(r'\d+', today_text)
            if match:
                exp_value = match.group(0)
                print(f"今日经验增加: {exp_value}")
            time.sleep(10)
            # 取消关注逻辑：悬停在“已关注”图标上，然后点击取消
            unfollow_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='已关注']")))
            actions.move_to_element(unfollow_elem).perform()
            cancel_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".CustomGroupMenu-cancel")))
            cancel_btn.click()
            # 点击弹窗确认的第一个按钮
            confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dy-Modal-footer .dy-btn")))
            confirm_btn.click()
            # 等待 30 分钟后自动退出
            time.sleep(1800)
        

    except Exception as e:
        print("发生错误", e)

if __name__ == "__main__":
    main()