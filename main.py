from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Firefox(executable_path='geckodriver.exe')

driver.implicitly_wait(30)

driver.get('https://zen.yandex.ru/?clid=101&country_code=ru')

input('Waiting for login...')
print('Process started')

cards = driver.find_elements_by_class_name('card-image-view__clickable')

for card in cards:
    if not (card.get_attribute('href').startswith('https://zen.yandex.ru/media')):
        continue
    card.click()
    sleep(3)
    driver.switch_to.window(driver.window_handles[-1])
    print(driver.window_handles)
    print(driver.current_url)
    print('Finding <textarea> ...')
    textarea = driver.find_element_by_xpath('//textarea[@class="comment-editor__editor"]')
    print('Sending keys...')
    textarea.send_keys('Неплохая статья)')
    print('Submitting comment...')
    driver.find_element_by_class_name('comment-editor__send-button').click()
    break
