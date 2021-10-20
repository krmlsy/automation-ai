from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os,time
import pandas as pd
import shutil

CURRENT_ALL_ELEMENTS_DIR = 'selenium.with.ai/data/current_page_elements.csv'
TEST_RUN_ELEMENTS_DIR = 'selenium.with.ai/data/test_run_page_elements.csv'
TEST_LAST_SUCCESS_ELEMENTS_DIR = 'selenium.with.ai/data/last_success_run_page_elements.csv'

def disableTurkish(text):
    translationTable = str.maketrans("ğĞıİöÖüÜşŞçÇ","gGiIoOuUsScC")
    text =  text.translate(translationTable)
    return text


def saveAllPageElements(driver):
    time.sleep(1)

    buttons = driver.find_elements_by_tag_name("button")
    inputs = driver.find_elements_by_tag_name("input")
    allElements = buttons + inputs

    elementsData = []

    for element in allElements:
        elementData = []

        if element.get_attribute("type") != 'hidden':
            elementData = getElementAttributes(element)
            elementsData.append(elementData)
    

    dframe = pd.DataFrame(elementsData, columns=["element", "tag","id","type","class","name","aria-autocomplete","title","href","text","placeholder"])
    dframe.to_csv(CURRENT_ALL_ELEMENTS_DIR, index=False)


def getElementAttributes(element):
    elementData = []
        # this for element idetification
    elementData.append(element.get_attribute("name") if element.get_attribute("name") != None  and len(element.get_attribute("name"))>0 else 'None')

    elementData.append(element.tag_name)
    elementData.append(element.get_attribute("id") if element.get_attribute("id") != None and len(element.get_attribute("id"))>0 else 'None')
    elementData.append(element.get_attribute("type") if element.get_attribute("type") != None and len(element.get_attribute("type"))>0   else 'None')
    elementData.append(element.get_attribute("class") if element.get_attribute("class") != None and len(element.get_attribute("class"))>0 else 'None')
    elementData.append(element.get_attribute("name") if element.get_attribute("name") != None  and len(element.get_attribute("name"))>0 else 'None')
    elementData.append(element.get_attribute("aria-autocomplete") if element.get_attribute("aria-autocomplete") != None and len(element.get_attribute("aria-autocomplete"))>0 else 'None')
    elementData.append(element.get_attribute("title") if element.get_attribute("title") != None and len(element.get_attribute("title"))>0  else 'None')
    elementData.append(element.get_attribute("href") if element.get_attribute("href") != None and len(element.get_attribute("href"))>0 else 'None')
    elementData.append(disableTurkish(element.text)if len(element.text) > 0  else 'None')
    elementData.append(disableTurkish(element.get_attribute("placeholder"))if element.get_attribute("placeholder")!= None and len(element.get_attribute("placeholder"))>0 else 'None')
    
    return elementData


def appendWorkingElement(element):
    answ=os.path.exists(TEST_RUN_ELEMENTS_DIR)
    with open(TEST_RUN_ELEMENTS_DIR, "a" if answ else "w") as f:
        elementData = getElementAttributes(element)
        if(answ):
            dframe = pd.DataFrame([elementData], columns=["element", "tag","id","type","class","name","aria-autocomplete","title","href","text","placeholder"])
            dframe.to_csv(f, index=False, mode='a' ,  header=False)
        else:
            dframe = pd.DataFrame([elementData], columns=["element", "tag","id","type","class","name","aria-autocomplete","title","href","text","placeholder"])
            dframe.to_csv(f, index=False)


def copySuccessElements():
    newPath = shutil.copy(TEST_RUN_ELEMENTS_DIR, TEST_LAST_SUCCESS_ELEMENTS_DIR)
    os.remove(TEST_RUN_ELEMENTS_DIR)


def findNextElementFromLastSuccessElements():
    # mevcut çalıştırmada en son başarılı yapılan işleme ait element bulunur
    df_test_run = pd.read_csv(TEST_RUN_ELEMENTS_DIR)
    last_success_element_in_test_run = df_test_run.iloc[-1]["element"]

    # en son başarılı çalışmada, bu elementten sonra hangi element geldiği bulunur (hata alınan tahmin edilmesi gereken element)
    df_last_success = pd.read_csv(TEST_LAST_SUCCESS_ELEMENTS_DIR)

    df_last_success.reset_index(inplace = True)
    most_recent_match = df_last_success.query("element == '"+ last_success_element_in_test_run + "'")
    next_element_index = most_recent_match['index']+1   
    dfn = df_last_success.iloc[[int(next_element_index)]]
    dfn.drop("index", axis="columns", inplace=True)
    print("burada en son başarılı olan elementten sonraki element ve değerleri alınır")
    print(dfn['element'])

    return dfn



def findMostPossibleWebElement(element_name):
    df = pd.read_csv(CURRENT_ALL_ELEMENTS_DIR , encoding="UTF-8")
    most_recent_match = df.query("element == '"+ element_name + "'")

    if len(str(most_recent_match["id"][0])) > 0:
        return str(most_recent_match["id"][0])


    else:
        return 'None'
    print("mevcut sayfanın tüm elemanları arasında sorun olan element AI ile tahmin edilir.")