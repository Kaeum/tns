from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import date

# https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559249
# https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559345
# https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559346
# https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559349
BASE_URL = "https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F10%2Fbizes%2F210031%2Fitems"
START_TIME = '6:00' #6:00 -> 오후 6시
END_TIME = '8:00' #8:00 -> 오후 8시
DATE = '2022-10-26'
BANK_NAME = '신한'

user = {
    "address": "고양시 덕양구 행신동"
}

def clipboard_input(user_xpath, user_input):
    temp_user_input = pyperclip.paste()
    pyperclip.copy(user_input)
    driver.find_element(By.XPATH, user_xpath).click()
    ActionChains(driver) \
        .key_down(Keys.COMMAND) \
        .send_keys('v') \
        .key_up(Keys.COMMAND) \
        .perform()
    pyperclip.copy(temp_user_input)

#https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F210031%2Fitems%2F4444654%3FstartDate%3D2022%2D09%2D26%26endDate%3D2022%2D09%2D26
#https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F10%2Fbizes%2F210031%2Fitems%2F444654
def makeCourtUrl(court_id):
    return f'{BASE_URL}%2F{court_id}'

driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
wait = WebDriverWait(driver, 10)

while True:
    user["id"] = input("NAVER 아이디를 입력하세요. \n")
    user["pw"] = input("비밀번호를 입력하세요. \n")
    user["target_court_id"] = input("코트 ID를 입력하세요. \n")
    is_confirmed = input("입력하신 아이디는 %s, 비밀번호는 %s입니다. 진행하시겠습니까? [Y] or [N] \n" % (user.get("id"), user.get("pw")))

    if is_confirmed.lower() == "Y".lower():
        break;

print(makeCourtUrl(user.get("target_court_id")))
driver.get(makeCourtUrl(user.get("target_court_id")))

#로그인
clipboard_input('//*[@id="id"]', user.get("id"))
clipboard_input('//*[@id="pw"]', user.get("pw"))
driver.find_element(By.XPATH, '//*[@id="log.login"]').click()

##일정선택(날짜,시간)
#날짜
element = wait.until(ec.element_to_be_clickable((By.XPATH, '//div[@id="calendar"]/div/strong/span[preceding-sibling::span]')))

if int(element.text) == date.today().month:
    driver.find_element(By.XPATH, '//a[@title="다음달"]').click()

wait.until(ec.element_to_be_clickable((By.XPATH, ('//td[@data-tst_cal_datetext="%s"]' % DATE)))).click()

#회차선택
wait.until(ec.element_to_be_clickable((By.XPATH, ('//ul[preceding-sibling::span[contains(., "오후")]]/li/a/span/span[contains(., "%s")]' % START_TIME)))).click()
wait.until(ec.element_to_be_clickable((By.XPATH, ('//ul[preceding-sibling::span[contains(., "오후")]]/li/a/span/span[contains(., "%s")]' % END_TIME)))).click()

#예약시간 선택 클릭
driver.find_element(By.XPATH, '//button[@data-tst_search_time_click="1"]').click()

#다음단계
wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@data-tst_next_step_click="0"]'))).click()

#결제하기 버튼
driver.find_element(By.XPATH, '//button[@data-tst_submit_click="0"]').click()

##주문/결제

#일반결제 클릭
wait.until(ec.element_to_be_clickable((By.XPATH, '//span[contains(@class, "radio-checked")]')))

wait.until(ec.element_to_be_clickable((By.XPATH, '//li[contains(@class, "_generalPaymentsTab")]/div/span[following-sibling::span]'))).click()

#나중에 결제
ActionChains(driver).send_keys(Keys.TAB) \
    .send_keys(Keys.TAB) \
    .send_keys(Keys.ARROW_DOWN) \
    .perform()

#환불 방법 - 환불정산액 적립
ActionChains(driver).send_keys(Keys.TAB) \
    .send_keys(Keys.TAB) \
    .send_keys(Keys.ARROW_DOWN) \
    .perform()

#입금은행
driver.find_element(By.XPATH, '//div[@id="bankCodeList"]').click()

driver.find_element(By.XPATH, '//li[contains(., "%s")]' % BANK_NAME).click()

#주문하기
driver.find_element(By.XPATH, '//button[contains(., "주문하기")]').click()


#%%
