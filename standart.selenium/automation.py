from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from  utilities import utilityOperations
import time

try:
    ROOT_DIR = utilityOperations.getProjectRootDir()
    
    driver = webdriver.Chrome(r"driver/chromedriver")

    # set implicit wait time
    driver.implicitly_wait(3) # seconds


    driver.get("https://isube.findeks.com/ers/login.xhtml")
    time.sleep(1)
    driver.find_element_by_id("tckn").send_keys("13067462414")
    driver.find_element_by_id("parola").send_keys(utilityOperations.getPassword())
    driver.find_element_by_id("normalGirisBtn").click()
    time.sleep(3)


    driver.close()
    print("------ Test Success ! ------")

except Exception as e:
    print("------ Test Failed ! ------")
    print(e)
    driver.close()