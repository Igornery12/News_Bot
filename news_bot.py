from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import customtkinter as ctk

g1_url= 'https://g1.globo.com/ultimas-noticias/'
cnn_url = 'https://www.cnnbrasil.com.br/ultimas-noticias/'
bbc_url = 'https://www.bbc.com/portuguese'


driver = webdriver.Chrome()
wait = WebDriverWait(driver,10)

filters = set()
verified_links = set()
selected_sites = set()


def update_filters_display():
    filters_box.delete("1.0", "end")

    for item in filters:
        filters_box.insert("end", f"{item}\n")


def add_filter():
    text_filter = filter_entry.get().strip().lower()

    if text_filter:
        filters.add(text_filter)
        update_filters_display()
        filter_entry.delete(0, "end")


def remove_filter():
    selected = remove_entry.get().strip().lower()

    if selected in filters:
        filters.remove(selected)
        update_filters_display()

    remove_entry.delete(0, "end")

def toggle_site(site, button):

    if site in selected_sites:
        selected_sites.remove(site)

        button.configure(
            fg_color="red",
            hover_color="#aa0000"
        )

    else:
        selected_sites.add(site)

        button.configure(
            fg_color="green",
            hover_color="#006600"
        )


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
        return False


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
        bot_config(i)
    

ctk.CTkLabel(app,text='Digite Palavras específicas para encontrar na machete das notícias de hoje').pack(pady='10')

filter_entry = ctk.CTkEntry(app,placeholder_text='Digite os filtros')
filter_entry.pack(pady=10)
ctk.CTkButton(app,text='adicionar filtro',command= add_filter).pack(pady=10)

ctk.CTkLabel(
    app,
    text="Filtros adicionados"
).pack(pady=(5))

filters_box = ctk.CTkTextbox(
    app,
    width=300,
    height=120
)

filters_box.pack(pady=5)

ctk.CTkLabel(
    app,
    text="Remover filtro"
).pack(pady=(10))

remove_entry = ctk.CTkEntry(
    app,
    placeholder_text="Digite o filtro para remover"
)
remove_entry.pack(pady=5)

ctk.CTkButton(
    app,
    text="Remover",
    command=remove_filter
).pack(pady=5)


g1_button = ctk.CTkButton(
    app,
    text="G1",
    fg_color="red",
    command=lambda: toggle_site(g1_url, g1_button)
)
g1_button.pack(pady=10)


cnn_button = ctk.CTkButton(
    app,
    text="CNN",
    fg_color="red",
    command=lambda: toggle_site(cnn_url, cnn_button)
)
cnn_button.pack(pady=10)


bbc_button = ctk.CTkButton(
    app,
    text="BBC",
    fg_color="red",
    command=lambda: toggle_site(bbc_url, bbc_button)
)
bbc_button.pack(pady=10)



ctk.CTkButton(app,text='Iniciar Bot', command=run_bot).pack(pady=10)
app.mainloop()