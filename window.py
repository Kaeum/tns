from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559249
# https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559345
# https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559346
# https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559349
COURT_URL = "https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fbooking.naver.com%2Fbooking%2F12%2Fbizes%2F714379%2Fitems%2F4559249"
TIME = '14:00'
DATE = '"2022-09-29"'
BANK_NAME = '신한'

user = {
    "id": "oror2930",
    "pw": "skrkdma1",
    "address": "고양시 덕양구 행신동"
}

def clipboard_input(user_xpath, user_input):
    temp_user_input = pyperclip.paste()

    pyperclip.copy(user_input)
    driver.find_element(By.XPATH, user_xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    pyperclip.copy(temp_user_input)

driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
driver.get(COURT_URL)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

#로그인
clipboard_input('//*[@id="id"]', user.get("id"))
clipboard_input('//*[@id="pw"]', user.get("pw"))
driver.find_element(By.XPATH, '//*[@id="log.login"]').click()

##일정선택(날짜,시간)

#날짜
wait.until(ec.element_to_be_clickable((By.XPATH, ('//*[@data-tst_cal_datetext=%s]' % DATE)))).click()

#시간
wait.until(ec.element_to_be_clickable((By.XPATH, ('//span[contains(., "%s")]' % TIME)))).click()

wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@data-tst_next_step_click="0"]'))).click()

##예약하기

#고양시민 수량 증가시키기
wait.until(ec.element_to_be_clickable((By.XPATH, '//div[contains(., "고양시민") and following-sibling::div[contains(., "관외자")]]/div/div/a[@title="더하기"]'))).click()

#주소 입력
clipboard_input('//input[@id="extra0"]', user.get("address"))

#셀렉박스(동의합니다)
wait.until(ec.element_to_be_clickable((By.XPATH, '//div[@class="wrap_select"]'))).click()
ActionChains(driver).send_keys(Keys.TAB) \
    .send_keys(Keys.TAB) \
    .send_keys(Keys.ENTER) \
    .perform()

#결제하기 버튼
driver.find_element(By.XPATH, '//button[@data-tst_submit_click="0"]').click()

##주문/결제

#일반결제 클릭
wait.until(ec.element_to_be_clickable((By.XPATH, '//li[contains(@class, "_generalPaymentsTab")]/div/span[following-sibling::span]'))).click()

#나중에 결제
ActionChains(driver).send_keys(Keys.TAB) \
    .send_keys(Keys.TAB) \
    .send_keys(Keys.ARROW_DOWN) \
    .perform()

#환불 방법 - 환불정산액 적립
ActionChains(driver).send_keys(Keys.TAB) \
    .send_keys(Keys.TAB) \
    .send_keys(Keys.TAB) \
    .send_keys(Keys.ARROW_DOWN) \
    .perform()

#입금은행
driver.find_element(By.XPATH, '//div[@id="bankCodeList"]').click()
driver.find_element(By.XPATH, '//li[contains(., "%s")]' % BANK_NAME).click()

#주문하기
driver.find_element(By.XPATH, '//button[contains(., "주문하기")]').click()

#%%
