import time
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


url = "http://163.50.34.40:8080/prass/jsp/monitor/ProgressDisplayViewer.jsp?dsn=orMesPRASS&Referer=http://163.50.34.40:8080/prass/jsp/shintyoku/index.jsp"

chrome_options = Options()
chrome_options.add_experimental_option('detach',True)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

time.sleep(10)