import time
import bs4
from playwright.sync_api import sync_playwright



#Proyecto dedicado al scraping web de la pagina transmilenio.gov.co
#Se usara la libreria playwright para interactuar con la pagina web


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.transmilenio.gov.co/buscador_de_rutas")
    print(page.title())
    page.pause()
    browser.close()
    
print("hello world")