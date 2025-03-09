from tkinter import END
from bs4 import BeautifulSoup
import requests

# Função para realizar o web scraping
def scrape_website(url_entry, raspar_entry, result_text):
    url = url_entry.get()
    raspar = raspar_entry.get()
    
    if not url:
        result_text.delete(1.0, END)
        result_text.insert(END, "Por favor, insira uma URL válida.")
        return
    
    if not raspar:
        result_text.delete(1.0, END)
        result_text.insert(END, "Por favor, insira um elemento HTML para raspar.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        raspagem = [dado.text for dado in soup.find_all(raspar)]
        
        result_text.delete(1.0, END)
        for dado in raspagem:
            result_text.insert(END, dado + "\n")
        
        global scraped_data
        scraped_data = raspagem
    except Exception as e:
        result_text.delete(1.0, END)
        result_text.insert(END, f"Erro ao acessar a URL: {e}")