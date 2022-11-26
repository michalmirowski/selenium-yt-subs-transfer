import pandas as pd
import logging

from selenium import webdriver
from selenium.common import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

#  *** LOGGER SETUP ***

# create logger
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)

# create console handler and file handler
ch = logging.StreamHandler()
fh = logging.FileHandler('import.log', mode='w')

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)

# *** SELENIUM SETUP ***

# connect selenium driver to 9222 port
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# *** IMPORT ***

# read exported subscriptions
my_csv = pd.read_csv('subscriptions.csv')
links = my_csv['Channel URL']


# check if subscriptions button is available
def check_if_subscribed():
    wait = WebDriverWait(driver, 10)
    subscribe_button = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR,
                                          '#subscribe-button > ytd-subscribe-button-renderer > yt-button-shape > button > div > span')))
    if subscribe_button.text == 'Subscribed':
        return True


# main function
def import_subscriptions():
    warning_counter = 0
    for link in links:
        try:
            driver.get(link)
            name = driver.title
            if check_if_subscribed():
                logger.info('%s already subscribed', name)
            else:
                logger.info('%s subscribing..', name)
                driver.find_element(By.CSS_SELECTOR,
                                    '#subscribe-button > ytd-subscribe-button-renderer > yt-button-shape > button > yt-touch-feedback-shape > div > div.yt-spec-touch-feedback-shape__fill').click()
        except TimeoutException:
            warning_counter += 1
            logger.warning('%s Something went wrong.. next channel', link)
            continue

    print('Import completed')
    if warning_counter > 0:
        print(str(warning_counter) + ' subscription(s) couldn\'t be imported. Check import.log file')
    driver.close()


if __name__ == "__main__":
    import_subscriptions()
