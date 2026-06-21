from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import customtkinter as ctk

g1_url= 'https://g1.globo.com/ultimas-noticias/'

driver = webdriver.Chrome()
wait = WebDriverWait(driver,10)

filters = set()
verified_links = set()
selected_sites = set()

def add_filter():
    text_filter = filter_entry.get().strip().lower()
    filters.add(text_filter)


def scroll_page():
    return driver.execute_script("window.scrollBy(0, 250);")


def read_more():
    try:
        more_news = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,"a[aria-label='Mostrar mais conteúdos']")
            )
        )

        driver.execute_script("arguments[0].click();",more_news)
        time.sleep(2)
        return True
    except:
        False


ctk.set_appearance_mode('dark')

app = ctk.CTk()
app.title('News Bot')
app.geometry('600x650')


def bot_config(site):
    
    driver.get(site)
    driver.maximize_window()

    while True:

        cards = driver.find_elements(By.CSS_SELECTOR,'div.feed-post')
        
        for card in cards:
            time.sleep(5)
            
            link = card.find_element(
                By.CSS_SELECTOR,'a'
                ).get_attribute('href')
            
            if link in verified_links:
                continue

            verified_links.add(link)
            
            news_headline = card.find_element(
                By.CSS_SELECTOR,'h2'
                ).text
            
            scroll_page()

            if filters:
                if not any(_filter in news_headline.lower() for _filter in filters):
                    continue

            print(30 * "-")
            print(news_headline)
            print(link)
            
            
            clicou = read_more()
            if not clicou:
                break


def run_bot():
    for i in selected_sites:
        return bot_config(i)
    

ctk.CTkLabel(app,text='Digite Palavras específicas para encontrar na machete das notícias de hoje').pack(pady='10')

filter_entry = ctk.CTkEntry(app,placeholder_text='Digite os filtros')
filter_entry.pack(pady=10)
ctk.CTkButton(app,text='adicionar filtro',command= add_filter).pack(pady=10)

g1_button = ctk.CTkButton(app,text='g1',command= selected_sites.add(g1_url)).pack(pady=10)


ctk.CTkButton(app,text='Iniciar Bot', command=run_bot).pack(pady=10)
app.mainloop()