from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()
wait = WebDriverWait(driver,10)
verified_links = set()

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


def pesquisar_noticias(site,filtro):
    
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
            
            print(30 * "-")
            print(news_headline)
            print(link)
            
            scroll_page()
            
            clicou = read_more()
            if not clicou:
                break

print(pesquisar_noticias('https://g1.globo.com/ultimas-noticias',''))