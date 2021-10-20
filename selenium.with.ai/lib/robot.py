from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from  lib import webelement
from ai import ai

success_elements = []
webdriver = webdriver.Chrome(r"driver/chromedriver")

def getDriver():
    return webdriver


def findElementById(id):
    try:
        webelement = webdriver.find_element_by_id(id)
        return webelement
    except Exception as e:
        print("Element Find Error, Running AI algorithm")
        print(e)
        return runAI()

def click(element):
    element.click()
    webelement.appendWorkingElement(element)
    success_elements.append(element.get_attribute("name"))

def sendKeys(element, text):
    element.send_keys(text)
    webelement.appendWorkingElement(element)
    success_elements.append(element.get_attribute("name"))
 

def testSuccess():
    webelement.copySuccessElements()

def runAI():
    webelement.saveAllPageElements(webdriver)
    dfn = webelement.findNextElementFromLastSuccessElements()
    # Calling the predict_elements method to return
    scores, element_name, test_df = ai.predict_elements(dfn)
    print(scores)
    print(element_name)
    new_id = webelement.findMostPossibleWebElement(element_name)
    return webdriver.find_element_by_id(new_id)