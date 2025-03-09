from tkinter import END, BOTH, WORD, Scrollbar, RIGHT, filedialog
from ttkbootstrap import Style, Button, Label, Entry, Text, Frame
from ttkbootstrap.constants import SUCCESS, DANGER
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Variável global para armazenar os dados raspados
scraped_data = []
url = 0
raspar = 0
data = 0
hora = 0

def data_hora():
    global data, hora
    data_hora_atual = datetime.now()
    data = data_hora_atual.strftime("%d/%m/%Y")
    hora = data_hora_atual.strftime("%H:%M:%S")

# Função para realizar o web scraping
def scrape_website(url_entry, raspar_entry, result_text):
    global scraped_data, url, raspar

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
        
        scraped_data = raspagem

    except Exception as e:
        result_text.delete(1.0, END)
        result_text.insert(END, f"Erro ao acessar a URL: {e}")

# Função para salvar os resultados em um arquivo TXT
def save_to_txt(result_text):
    data_hora() # Atualiza sempre a data e a hora
    global scraped_data, url, raspar, data, hora

    if not scraped_data:
        result_text.insert(END, "\nNenhum dado para salvar.", "red")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"URL: {url}\n")
                file.write(f"Raspagem: {raspar}\n")
                file.write(f"Data: {data}\n")
                file.write(f"Hora: {hora}\n\n")
                for dado in scraped_data:
                    file.write(dado + "\n")
            result_text.insert(END, f"\nDados salvos em: {file_path}", "green")
        except Exception as e:
            result_text.insert(END, f"\nErro ao salvar o arquivo: {e}", "red")

# Função para limpar os resultados
def clear_results():
    global scraped_data
    url_entry.delete(0, END)
    raspar_entry.delete(0, END)
    result_text.delete(1.0, END)
    scraped_data = []

# Configuração inicial da interface gráfica
def setup_gui():
    global url_entry, result_text, raspar_entry

    # Configuração do tema Cyborg
    style = Style(theme="cyborg")
    root = style.master
    root.title("Web Scraping com Tkinter e TTKBootstrap")
    root.geometry("800x600")

    # Frame principal
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Entrada de URL
    url_label = Label(main_frame, text="URL:")
    url_label.grid(row=0, column=0, sticky="w", pady=5)
    url_entry = Entry(main_frame, width=50)
    url_entry.grid(row=0, column=1, sticky="ew", pady=5)

    # Entrada de elemento HTML para raspar
    raspagem_label = Label(main_frame, text="Raspar:")
    raspagem_label.grid(row=1, column=0, sticky="w", pady=5)
    raspar_entry = Entry(main_frame, width=50)
    raspar_entry.grid(row=1, column=1, sticky="ew", pady=5)

    # Botão de scraping
    scrape_button = Button(
        main_frame,
        text="Raspar Dados",
        command=lambda: scrape_website(url_entry, raspar_entry, result_text),
        bootstyle=SUCCESS
    )
    scrape_button.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="nsew")

    # Área de resultados
    result_label = Label(main_frame, text="Resultados:")
    result_label.grid(row=2, column=0, sticky="nw", pady=5)
    result_text = Text(main_frame, wrap=WORD, height=15)
    result_text.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=5)

    # Configuração das tags de estilo
    result_text.tag_config("green", foreground="green")
    result_text.tag_config("red", foreground="red")

    # Barra de rolagem para a área de resultados
    scrollbar = Scrollbar(main_frame, command=result_text.yview)
    scrollbar.grid(row=2, column=3, sticky="ns", pady=5)
    result_text.config(yscrollcommand=scrollbar.set)

    # Botões de ação
    action_frame = Frame(main_frame)
    action_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

    save_button = Button(
        action_frame,
        text="Salvar em Excel",
        command=lambda: save_to_txt(result_text),
        bootstyle=SUCCESS
    )
    save_button.pack(side=RIGHT, padx=5)
    
    clear_button = Button(
        action_frame,
        text="Limpar Resultados",
        command=clear_results,
        bootstyle=DANGER
    )
    clear_button.pack(side=RIGHT, padx=5)

    # Configuração de redimensionamento
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)

    root.mainloop()

# Execução do programa
if __name__ == "__main__":
    setup_gui()