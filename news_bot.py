from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import customtkinter as ctk
import google.generativeai as genai
from telegram import Bot
import asyncio

TOKEN = ""
CHAT_ID = ...  
async def send_telegram(manchete, resumo, link):
    bot = Bot(TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"{manchete}\n\n{resumo}\n\n{link}"
    )

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


def ai(article_text_,news_headline,link):

    try:    
        genai.configure(api_key="")
        model = genai.GenerativeModel("gemini-2.5-flash")

        article_text = article_text_
        time.sleep(3)

        prompt = f"""
            Resuma a notícia abaixo no seguinte formato:

            

            📌 RESUMO:
            - 3 a 5 tópicos em bullet points
            - linguagem clara e objetiva

            🚨 DETALHES IMPORTANTES:
            - apenas fatos relevantes

            Texto:
            {article_text}
            """
        
        response = model.generate_content(
                prompt
                )


        
        print(f'resumo: {response.text}')

        asyncio.run(send_telegram(news_headline,response.text,link))

    except Exception as e:
        print(f"Error: {e}")

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



def collect_infos(site):

    global running

    if 'bbc' in site :
        card_config = 'div.promo-text'
        news_headline_config = 'h3'
        article_content = 'main div p'


    elif 'g1' in site:
        card_config = 'div.feed-post'
        news_headline_config = 'h2'
        article_content = '.mc-article-body p'

    elif 'cnn' in site:
        card_config = 'figure.h-full'
        news_headline_config = 'h2'
        article_content = 'div.text-lg p' 


    cards = driver.find_elements(By.CSS_SELECTOR,card_config)
    
    for card in cards:
            time.sleep(5)
            
            if not running:
                return

            if len(verified_links) >=4:
                running = False
                return
            
            scroll_page()
            
            news_headline = card.find_element(
                By.CSS_SELECTOR,news_headline_config
                ).text
            
        
            if filters:
                if not any(_filter in news_headline.lower() for _filter in filters):
                    continue
            
            link = card.find_element(
                By.CSS_SELECTOR,'a'
                ).get_attribute('href')
            
            if link in verified_links:
                continue

            verified_links.add(link)

            print(30 * "-")
            print(news_headline)
            print(link)            
            print()
            time.sleep(5)

            driver.execute_script(
                "window.open(arguments[0], '_blank');",
                link
                )

            driver.switch_to.window(driver.window_handles[-1])

                
            wait.until(
            EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, article_content)
                )
            )
            
            paragraphs = driver.find_elements(By.CSS_SELECTOR, article_content)
            
            article_text = "\n".join(
            paragraph.text.strip()
            for paragraph in paragraphs
            if paragraph.text.strip()
        )

            driver.close()

            driver.switch_to.window(driver.window_handles[0])
            
            ai(article_text,news_headline,link)

            
            
            cliked = read_more()
            if not cliked:
                break

ctk.set_appearance_mode('dark')

app = ctk.CTk()
app.title('News Bot')
app.geometry('600x650')

def bot_config(site):
    global running

    running = True
    verified_links.clear()

    driver.get(site)
    driver.maximize_window()

    while running:
        collect_infos(site)


def run_bot():
    if selected_sites:
        for _site in selected_sites:
            bot_config(_site)
        driver.quit() 
        app.quit()   
    else:
        return

ctk.CTkLabel(
    app,
    text='Digite Palavras específicas para encontrar na machete das notícias de hoje'
).pack(pady='10')

filter_entry = ctk.CTkEntry(
    app,
    placeholder_text='Digite os filtros'
)

filter_entry.pack(pady=10)

ctk.CTkButton(
    app,
    text='adicionar filtro',
    command= add_filter
).pack(pady=10)

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

ctk.CTkButton(
    app,
    text='Iniciar Bot',
    command=run_bot
).pack(pady=10)

app.mainloop()
