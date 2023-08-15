from pytesseract import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller
import re
import os
from selenium.webdriver.chrome.options import Options

def check(code, session):
    culture_code = code
    base = {"result": None, "code": None, "amount": None, "msg": None}
    options = Options()
    prefs = {'profile.default_content_setting_values': 
    {
    'plugins'                   : 2, 'popups': 2, 'geolocation': 2,
    'notifications'             : 2, 'auto_select_certificate': 2,
    'fullscreen'                : 2,
    'mouselock'                 : 2, 'mixed_script': 2,
    'media_stream'              : 2,
    'media_stream_mic'          : 2, 'media_stream_camera': 2,
    'protocol_handlers'         : 2,
    'ppapi_broker'              : 2, 'automatic_downloads': 2,
    'midi_sysex'                : 2,
    'push_messaging'            : 2, 'ssl_cert_decisions': 2,
    'metro_switch_to_desktop'   : 2,
    'protected_media_identifier': 2, 'app_banner': 2,
    'site_engagement'           : 2,
    'durable_storage'           : 2
    }}
    options.add_experimental_option('prefs', prefs)
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options)
    driver.get("https://m.cultureland.co.kr/csh/cshGiftCard.do")
    driver.add_cookie({'name' : 'SESSION', 'value' : session})
    driver.refresh()
    driver.get("https://m.cultureland.co.kr/csh/cshGiftCard.do")
    print("문화상품권 충전 시작")
    start = time.time()
    try:{driver.execute_script("closeLayers();")}
    except:{}
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/form[2]/div[2]/div[2]/input[1]").send_keys(culture_code.split("-")[0])
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/form[2]/div[2]/div[2]/input[2]").send_keys(culture_code.split("-")[1])
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/form[2]/div[2]/div[2]/input[3]").send_keys(culture_code.split("-")[2])
    xpath1 = list()
    xpath2 = list()
    xpath3 = list()

    default_path = os.getcwd() + "/images/"
    for j in range(3):
        for i in range(4):
            driver.find_element(By.XPATH, f"/html/body/div[2]/div[{j + 2}]/a[{i + 1}]").screenshot(default_path + f"{j + 1}-{i + 1}" + ".png")
    Image_start = time.time()
    for i in range(4):
        xpath1.insert(i,  re.sub(r'[^0-9]', '', pytesseract.image_to_string(image=default_path + f'1-{i + 1}.png', config='--psm 6')))
    for i in range(4):
        xpath2.insert(i,  re.sub(r'[^0-9]', '', pytesseract.image_to_string(image=default_path + f'2-{i + 1}.png', config='--psm 6')))
    for i in range(4):
        xpath3.insert(i,  re.sub(r'[^0-9]', '', pytesseract.image_to_string(image=default_path + f'3-{i + 1}.png', config='--psm 6')))
    Image_end = time.time()
    code = culture_code.split("-")[3]
    for i in range(4):
        for j in range(4):
            if(xpath1[j] == code[i]):
                driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/a[{j + 1}]").click()
        for j in range(4):
            if(xpath2[j] == code[i]):
                driver.find_element(By.XPATH, f"/html/body/div[2]/div[3]/a[{j + 1}]").click()
        for j in range(4):
            if(xpath3[j] == code[i]):
                driver.find_element(By.XPATH, f"/html/body/div[2]/div[4]/a[{j + 1}]").click()
    
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/form[2]/div[3]/input").click()
    result = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[8]/div/table/tbody/tr/td[3]/b").text
    amount = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[8]/div/table/tbody/tr/td[4]").text
    resultcode = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[8]/div/table/tbody/tr/td[2]").text
    end = time.time()
    driver.quit()
    print(f"{end - start:.5f} 초 걸림(크롬 실행 시간 제외)")
    if(resultcode == culture_code):
        base["result"] = True
        base["msg"] = result
        base["amount"] = ''.join(filter(str.isdigit, amount))
        return base
        print(f"{resultcode}의 결과:\n{result}\n금액:{amount}")
        print(f"이미지 인식 걸린 시간:{Image_end - Image_start:.5f}초")
    else:
        base["result"] = False # 입금내역에 존재하지 않음
        base["msg"] = "서버 오류"
        return base
        print("테서렉트 이미지 인식 오류")