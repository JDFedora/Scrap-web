import time
import bs4
import pandas as pd

from playwright.sync_api import sync_playwright



#Proyecto dedicado al scraping web de la pagina transmilenio.gov.co
#Se usara la libreria playwright para interactuar con la pagina web


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Cambia a False si quieres ver el navegador
    page = browser.new_page()
    page.goto("https://www.transmilenio.gov.co/buscador_de_rutas")
    
    #busqueda horizontal
    page.get_by_role("link", name= "2",exact=True).click()
    page.wait_for_timeout(1200)
    soup= bs4.BeautifulSoup(page.content(), "html.parser")
    
    tabla=soup.find_all("tbody")
    #txt prueba
    

    datos_tabla=[]
    Nombres_rutas=[]
    for a in tabla[0].find_all("tr"):
        for row in a.find_all("td"):
            Nombres_rutas.append(row.text.strip())

    Indice_rutas=[]
    for a in Nombres_rutas:
        Indice_rutas.append(a.split()[0]) #añade el indice de la ruta (ej F14,1,B16...etc)
    for a in range(0,len(Nombres_rutas)):
        Nombres_rutas[a]=Nombres_rutas[a].replace("\n","")
    

    df = pd.DataFrame({"Ruta":Indice_rutas,"Nombres":Nombres_rutas},index=None)
    df.to_csv('tabla.csv')
    
    """ with open("tabla.csv","w") as f:
        f.write(Nombres_rutas) """

    
   
    browser.close()
    
print("hello world")