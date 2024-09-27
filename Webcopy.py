import requests
from bs4 import BeautifulSoup
from docx import Document
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import streamlit as st
import time
multiplier=0.8
##selenium
s=Service()
chromeOptions=Options()
chromeOptions.headless=False
chromeOptions.page_load_strategy = 'normal'
chromeOptions.add_argument("--disable-search-engine-choice-screen")
driver=webdriver.Chrome(service=s, options=chromeOptions)
##
if "tim" not in st.session_state:
    st.session_state["tim"]=30
@st.cache_resource
def timer():
    with st.empty():
        while st.session_state["tim"]:
            st.title(st.session_state["tim"])
            st.session_state["tim"]-=1
            time.sleep(1)
if "poeni" not in st.session_state:
    st.session_state["poeni"]=0
if "rjecdat" not in st.session_state:
    rjecnik=open("Dotjerano.txt","r",encoding="utf-8")
    st.session_state["rjecdat"]=[]
    for i in rjecnik.readlines():
        st.session_state["rjecdat"].append(i.rstrip("\n"))
if "randoms" not in st.session_state:
    global trigger
    trigger=0
    driver.get("https://kalkulator.com.hr/generator-rijeci")
    driver.implicitly_wait(2)
    click=driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]/p")
    click.click()
    click=driver.find_element(By.XPATH, "//input[@name='ctl00$htmlSelection1$ctl00$Button1']")
    click.click()
    driver.implicitly_wait(2)
    rici=driver.find_elements(By.XPATH,"//span[@id='htmlSelection1_ctl00_Label1']")
    for i in rici:
        st.session_state["randoms"]=i.text.split("\n")
    print(st.session_state["randoms"])
#streamlit
st.header(st.session_state["randoms"][0])
st.session_state.nig=""
#
def check_exists_by_xpath(xpath):
    try:
        laler=driver.find_element(By.XPATH, "//div[@class='rhyme']")
        laler.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True
def check_exists(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True
def rima(prva,druga,mu=0.8):
    if druga in st.session_state["rjecdat"]:
            if prva!=druga:  
                for i in range(len(prva),1,-1):
                    for d in range(len(prva)-1):
                        print(prva[d:i+d])
                        if prva[d:i+d] in druga and ("a" in prva[d:i+d] or "e" in prva[d:i+d] or "i" in prva[d:i+d] or "o" in prva[d:i+d] or "u" in prva[d:i+d] or "r" in prva[d:i+d]):
                            if len(druga)<=len(prva):
                                return((len(prva[d:i+d])**mu/((len(prva)-1+(abs(len(druga)-len(prva))/len(prva))/10)**mu)*10))
                            else: #                                                              duže rijeci preferirane preko kratkih
                                return((len(prva[d:i+d])**mu/((len(prva)-1+(abs(len(druga)-len(prva))/len(druga))/11)**mu)*10))
                        if i+d==len(prva):
                            break
            else:
                return "Ne može se koristiti ista riječ"
    else:
        return "Nema te riječi"
def r():
    x=rima(st.session_state["randoms"][0],st.session_state.nig,multiplier)
    if isinstance(x, float):
        st.session_state["poeni"]+=x
        st.markdown(st.session_state["poeni"])
    else:
        st.markdown(x)
pogod=st.text_input("Rima:",key="nig",on_change=r)
timer()
    #py -m streamlit run Webcopy.py
#rjecnik da ubrza umjesto hjp, bolji rhyme algoritam