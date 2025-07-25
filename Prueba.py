import time
import bs4
import pandas as pd
import numpy as np

from playwright.sync_api import sync_playwright



#Proyecto dedicado al scraping web de la pagina transmilenio.gov.co
#Se usara la libreria playwright para interactuar con la pagina web


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Cambia a False si quieres ver el navegador
    page = browser.new_page()
    page.goto("https://www.transmilenio.gov.co/buscador_de_rutas")
    page.expect_request_finished()
    page.wait_for_timeout(2000)

    #busqueda horizontal
    soup= bs4.BeautifulSoup(page.content(), "html.parser")
    Num_paginas=soup.find_all("li",class_="paginate_button")
    Nombres_rutas=[]
    Indice_rutas=[]
    Href_rutas=[]
    with open("texto.html","w", encoding="utf-8") as f:
        f.write(str(soup))
    
    for i in range(2,len(Num_paginas)):# bucle para pasar por todas las paginas
        soup= bs4.BeautifulSoup(page.content(), "html.parser")     
        tabla=soup.find_all("tbody")
        
        for a in tabla[0].find_all("tr"):
            for row in a.find_all("td"):
                Nombres_rutas.append(row.text.strip())
                Href_rutas.append(row.find("a")["href"])  # Extrae el href de cada ruta
        try:
            page.get_by_role("link", name= f'{i}',exact=True).click()
        except:
            print("No se pudo hacer click en la pagina",i)
        page.expect_request_finished()
        page.wait_for_timeout(1200)
        
  
    for a in Nombres_rutas:
        Indice_rutas.append(a.split()[0]) #añade el indice de la ruta (ej F14,1,B16...etc)
    for a in range(0,len(Nombres_rutas)):
        Nombres_rutas[a]=Nombres_rutas[a].replace("\n","")        
    #escritura de los datos en un archivo csv
    df = pd.DataFrame({"Ruta":Indice_rutas,"Nombres":Nombres_rutas},index=None)
    df.to_csv('tabla.csv')
    df = pd.DataFrame({"Href:":Href_rutas})
    df.to_csv('Href rutas.csv')
     # Extracción de las rutas y los nombres de cada una de las rutas
    contador=0
    for rutas in Href_rutas:
        Estacion= []
        page.goto(rutas)  # Navega a cada ruta
        page.wait_for_timeout(2000)
        page.expect_request_finished()
        page.locator(".SearchResults > footer > div").first.scroll_into_view_if_needed()
        page.wait_for_timeout(2000)
        soup = bs4.BeautifulSoup(page.content(), "html.parser")
        Estaciones = soup.find_all("div",class_ = "infoParada")
        for a in Estaciones:
            try:
                Estacion.append(a.find("a").text.strip())  # Extrae el nombre de la estación
            except Exception as e:
                print("error de tipo: ",e)
        #Estacion= np.unique(Estacion).tolist()  # Elimina duplicados
        index=[]
        for abc in Estacion:
            index.append(Indice_rutas[contador])
        contador+=1
        df = pd.DataFrame({"Ruta":index,"Nombres":Estacion},index=None)
        try:
            df.to_csv(f'./Rutas/Rutas de:{index[0]}.csv')
        except Exception as e:
            df.to_csv(f'Rutas de:{contador}_error.csv')

    browser.close()
    
print("Finalizado")