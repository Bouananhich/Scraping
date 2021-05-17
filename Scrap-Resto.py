from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from openpyxl import Workbook
from selenium.webdriver.common.by import By
from docx import Document
import pandas as pd 


option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--start-maximised")

browser = webdriver.Chrome("./chromedriver", options=option)
URL = 'https://www.tripadvisor.com/Restaurant_Review-g528745-d1988506-Reviews-El_Pollito_Pescador-San_Juan_del_Sur_Rivas_Department.html'
browser.get(URL)
time.sleep(3)
browser.maximize_window()
button_cookies = browser.find_element_by_id('_evidon-accept-button')
button_cookies.click()
time.sleep(3)
Texte_total = ''

pages = browser.find_element_by_xpath("//div[@class='pageNumbers']")
nbr_pages = int(pages.text[-1])
time.sleep(1)


for i in range (nbr_pages - 1):
    Button_more = browser.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']")
    Button_more.click()
    time.sleep(3)
    Texte = browser.find_element_by_xpath("//div[@class='listContainer hide-more-mobile']").text
    Texte_total += Texte
    button_page = browser.find_element_by_xpath("//a[@class='nav next ui_button primary']")
    button_page.click()
    time.sleep(3)

Button_more = browser.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']")
Button_more.click()
time.sleep(3)
Texte = browser.find_element_by_xpath("//div[@class='listContainer hide-more-mobile']").text
Texte_total += Texte

def delete(Liste,Expression):
    while True :
        try : 
            Liste.remove(Expression)
        except:
            break


Liste = Texte_total.split('\n')

delete(Liste,"Show less")
delete(Liste,"This review is the subjective opinion of a TripAdvisor member and not of TripAdvisor LLC.")
delete(Liste,'123456…9')
delete(Liste,'Next')
delete(Liste,'Previous')
delete(Liste,'via mobile')

n = len(Liste)
separateur = 'Reviewed'
m = len(separateur)

Dates = []
Titres = []
Avis = []

for i in range(n):
    if Liste[i][:m] == separateur : 
        Dates.append(Liste[i].replace(separateur,''))
        Titres.append(Liste[i+1])
        Avis.append(Liste[i+2])
Df = pd.DataFrame()
Df['Dates'] = Dates
Df['Titres'] = Titres
Df['Avis'] = Avis

word_sentiment = pd.read_csv('word_sentiment-1.csv',delimiter=';',names=['score'])

Score = []
for i in range(len(Df)):
    S = 0
    avis = Df['Avis'][i].split(' ')
    for mot in avis :
        try :
            S += word_sentiment['score'][mot]
        except :
            pass
    Score.append(S)

Df['Scores'] = Score

Df.to_csv('Scores.csv')