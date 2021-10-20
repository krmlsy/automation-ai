from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from  utilities import utilityOperations
from  lib import webelement,robot
import time

try:
    
    driver = robot.getDriver()

    # set implicit wait time
    driver.implicitly_wait(3) # seconds

    driver.get("https://isube.findeks.com/ers/login.xhtml")
    time.sleep(1)
    robot.sendKeys(robot.findElementById("tckn"), "13067462414")
    robot.sendKeys(robot.findElementById("parola"), utilityOperations.getPassword())
    robot.click(robot.findElementById("normalGirisBtn"))

    time.sleep(3)

    robot.testSuccess()
    driver.close()

    print("------ Test Success ! ------")

except Exception as e:
    print("------ Test Failed ! ------")
    print(e)
    driver.close()