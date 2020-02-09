from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
from datetime import datetime
from random import randint
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
fh = logging.FileHandler("logs.log", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

driver = webdriver.Firefox(executable_path='geckodriver.exe')

driver.implicitly_wait(30)

driver.get('https://zen.yandex.ru/?clid=101&country_code=ru')
input('Waiting for login...')


def get_cards(url=None):
    # Prevent infinite tabs loop
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])

    if url is None:
        driver.get('https://zen.yandex.ru/?clid=101&country_code=ru')
    else:
        driver.get(url)

    cards = driver.find_elements_by_class_name('card-image-view__clickable')
    log.info(f'Found {len(cards)}')

    return cards


def process_links(cards):
    comments = [
    ]
    comment_id = 0

    for card in cards:
        try:
            link = card.get_attribute('href')
            if not (link.startswith('https://zen.yandex.ru/media')):
                continue

            card.click()
            log.info(f'Opened {link}')
            sleep(3)
            driver.switch_to.window(driver.window_handles[-1])
            # sleep(randint(60, 420))
        except (StaleElementReferenceException, NoSuchElementException):
            return

        print('Finding <textarea> ...')
        try:
            textarea = driver.find_element_by_xpath('//textarea[@class="comment-editor__editor"]')
        except NoSuchElementException:
            log.info('Comments not permitted')
            continue
        pos = textarea.location
        print(pos)
        while driver.execute_script('return window.pageYOffset') <= pos['y']:
            driver.execute_script(f"window.scrollBy(0,{randint(5, 70)})")
            sleep(randint(0, 2))
            print(f"{datetime.now()} --- {driver.execute_script('return window.pageYOffset')}")
        sleep(randint(1, 3))
        scrollby = pos['y'] - driver.execute_script('return window.pageYOffset')
        print(f'{scrollby=}')
        driver.execute_script(f"window.scrollBy(0,{scrollby - 170})")

        sleep(randint(3, 10))

        print('Sending keys...')
        if comment_id == len(comments):
            comment_id = 0
        textarea.send_keys(comments[comment_id])
        log.info(f'Commented {comment_id + 1}')
        comment_id += 1
        sleep(randint(1, 3))

        print('Submitting comment...')
        driver.find_element_by_class_name('comment-editor__send-button').click()
        sleep(randint(3, 20))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(randint(5, 30))


if __name__ == '__main__':
    while True:
        process_links(get_cards())
