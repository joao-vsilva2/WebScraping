import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, Button, Label, Entry, Text, Frame
from ttkbootstrap.constants import SUCCESS, DANGER
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para realizar o web scraping
def scrape_website():
    url = url_entry.get()
    if not url:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Por favor, insira uma URL válida.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [title.text for title in soup.find_all('h1')]  # Exemplo: raspagem de títulos <h1>
        
        result_text.delete(1.0, tk.END)
        for title in titles:
            result_text.insert(tk.END, title + "\n")
        
        global scraped_data
        scraped_data = titles
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Erro ao acessar a URL: {e}")

# Função para limpar os resultados
def clear_results():
    url_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    global scraped_data
    scraped_data = []

# Função para salvar os resultados em um arquivo Excel
def save_to_excel():
    if not scraped_data:
        result_text.insert(tk.END, "\nNenhum dado para salvar.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df = pd.DataFrame(scraped_data, columns=["Títulos"])
        df.to_excel(file_path, index=False)
        result_text.insert(tk.END, f"\nDados salvos em: {file_path}", "green")

# Configuração inicial da interface gráfica
def setup_gui():
    global url_entry, result_text, scraped_data
    scraped_data = []

    # Configuração do tema Cyborg
    style = Style(theme="cyborg")
    root = style.master
    root.title("Web Scraping com Tkinter e TTKBootstrap")
    root.geometry("800x600")

    # Frame principal
    main_frame = Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Entrada de URL
    url_label = Label(main_frame, text="URL:")
    url_label.grid(row=0, column=0, sticky="w", pady=5)
    url_entry = Entry(main_frame, width=50)
    url_entry.grid(row=0, column=1, sticky="ew", pady=5)

    # Botão de scraping
    scrape_button = Button(main_frame, text="Raspar Dados", command=scrape_website)
    scrape_button.grid(row=0, column=2, padx=10, pady=5)

    # Área de resultados
    result_label = Label(main_frame, text="Resultados:")
    result_label.grid(row=1, column=0, sticky="nw", pady=5)
    result_text = Text(main_frame, wrap=tk.WORD, height=15)
    result_text.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=5)

    # Configuração da tag "green"
    result_text.tag_config("green", foreground="green")

    # Barra de rolagem para a área de resultados
    scrollbar = tk.Scrollbar(main_frame, command=result_text.yview)
    scrollbar.grid(row=1, column=3, sticky="ns", pady=5)
    result_text.config(yscrollcommand=scrollbar.set)

    # Botões de ação
    action_frame = Frame(main_frame)
    action_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

    save_button = Button(action_frame, text="Salvar em Excel", command=save_to_excel, bootstyle=SUCCESS)
    save_button.pack(side=tk.RIGHT, padx=5)
    
    clear_button = Button(action_frame, text="Limpar Resultados", command=clear_results, bootstyle=DANGER)
    clear_button.pack(side=tk.RIGHT, padx=5)

    # Configuração de redimensionamento
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)

    root.mainloop()

# Melhorias sugeridas para o projeto
def suggested_improvements():
    """
    1. **Validação de URL**: Implementar uma validação mais robusta para garantir que a URL inserida seja válida.
    2. **Escolha de Elementos**: Permitir que o usuário escolha quais elementos HTML deseja raspar (ex.: h1, p, div).
    3. **Progresso Visual**: Adicionar uma barra de progresso ou indicador de status durante o processo de scraping.
    4. **Tratamento de Erros**: Melhorar o tratamento de erros para diferentes tipos de falhas (ex.: timeout, conexão recusada).
    5. **Interface Responsiva**: Usar layouts mais avançados para garantir que a interface seja totalmente responsiva.
    6. **Exportação em Múltiplos Formatos**: Permitir exportação em outros formatos além do Excel, como CSV ou JSON.
    7. **Cache de Dados**: Implementar um cache para evitar múltiplas requisições à mesma URL em curtos intervalos.
    8. **Autenticação**: Adicionar suporte para sites que exigem autenticação (ex.: login via POST).
    9. **Documentação**: Incluir uma documentação detalhada para facilitar o uso e manutenção do programa.
    10. **Testes Automatizados**: Criar testes automatizados para verificar a funcionalidade do programa em diferentes cenários.
    """

# Execução do programa
if __name__ == "__main__":
    setup_gui()