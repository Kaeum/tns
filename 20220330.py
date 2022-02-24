from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://goyangtennis.or.kr")
driver.maximize_window()

#로그인
driver.find_element(By.ID, "ol_id").send_keys('hanwool09')
driver.find_element(By.ID, "ol_pw").send_keys('488698')
driver.find_element(By.ID, "ol_submit").send_keys(Keys.ENTER)

#충장 예약
driver.get("https://goyangtennis.or.kr/bbs/board.php?bo_table=tennis_reservation&mode=step1&cp_code=jZEoNfK15864esqDTBRV")

# 코트 번호
driver.find_elements(By.ID, 'top-aligned-media')[0].click()

wait = WebDriverWait(driver, 10)

# 다음달
element = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="wrap-calendar"]/nav/ul/li[3]/a')))
element.click()

# 날짜
element = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '[data-date="2022-03-30"]')))
element.click()

# 시간대
element = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '[data-time="18:00"]')))
element.click()

# 동의
driver.find_element(By.XPATH, "//*[@id='wzfrm']/div[3]/div/div/button").click()
driver.find_element(By.ID, 'bk_payment_card').click()
driver.find_element(By.ID, 'agree1').click()
driver.find_element(By.ID, 'agree2').click()
driver.find_element(By.ID, 'submit_next').click()

#결제창
driver.switch_to.frame("nice_frame")
element = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="page_agree"]/div/div/ul/li[1]/p/label')))
element.click()
element = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="frontCardList"]/li[2]/label')))
element.click()
element = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '[nplang="MSG.NEXT"]')))
element.click()

#KB국민카드
api_frame = wait.until(ec.presence_of_element_located((By.ID, 'api_frame')))
driver.switch_to.frame(api_frame)

kb_frame = wait.until(ec.presence_of_element_located((By.ID, 'kbframe')))
driver.switch_to.frame(kb_frame)

element = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="btn-kbpay-exp"]/button')))
element.click()


