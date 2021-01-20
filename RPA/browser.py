from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options


def browser(DL_DIR:str):
    prefs = {"download.default_directory": DL_DIR}
    # 各種オプション追加
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    # chromeOptions.add_argument('--headless')
    # chromeOptions.add_argument(f'--user-data-dir=./{DL_DIR}/user')
    chromeOptions.add_argument('--lang=ja-JP')
    return webdriver.Chrome(chrome_options=chromeOptions)