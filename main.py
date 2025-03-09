from tkinter import END, BOTH, WORD, Scrollbar, RIGHT
from ttkbootstrap import Style, Button, Label, Entry, Text, Frame
from ttkbootstrap.constants import SUCCESS, DANGER
from salvar_dados import *
from raspagem_dados import *

# Função para limpar os resultados
def clear_results():
    url_entry.delete(0, END)
    raspar_entry.delete(0, END)
    result_text.delete(1.0, END)
    global scraped_data
    scraped_data = []

# Configuração inicial da interface gráfica
def setup_gui():
    global url_entry, result_text, scraped_data, raspar_entry
    scraped_data = []

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
    scrape_button = Button(main_frame, text="Raspar Dados", command=lambda:scrape_website(url_entry, raspar_entry, result_text), bootstyle=SUCCESS)
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

    save_button = Button(action_frame, text="Salvar em Excel", command=lambda:save_to_excel(scraped_data, result_text), bootstyle=SUCCESS)
    save_button.pack(side=RIGHT, padx=5)
    
    clear_button = Button(action_frame, text="Limpar Resultados", command=clear_results, bootstyle=DANGER)
    clear_button.pack(side=RIGHT, padx=5)

    # Configuração de redimensionamento
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)

    root.mainloop()

# Execução do programa
if __name__ == "__main__":
    setup_gui()

"""
MELHORIAS:

1. **Validação de URL**: Implementar uma validação mais robusta para garantir que a URL inserida seja válida. 
2. **Escolha de Elementos**: Permitir que o usuário escolha quais elementos HTML deseja raspar (ex.: h1, p, div). V
3. **Progresso Visual**: Adicionar uma barra de progresso ou indicador de status durante o processo de scraping.
4. **Tratamento de Erros**: Melhorar o tratamento de erros para diferentes tipos de falhas (ex.: timeout, conexão recusada).
5. **Interface Responsiva**: Usar layouts mais avançados para garantir que a interface seja totalmente responsiva.
6. **Exportação em Múltiplos Formatos**: Permitir exportação em outros formatos além do Excel, como CSV ou JSON.
7. **Cache de Dados**: Implementar um cache para evitar múltiplas requisições à mesma URL em curtos intervalos.
8. **Autenticação**: Adicionar suporte para sites que exigem autenticação (ex.: login via POST).
9. **Documentação**: Incluir uma documentação detalhada para facilitar o uso e manutenção do programa.
10. **Testes Automatizados**: Criar testes automatizados para verificar a funcionalidade do programa em diferentes cenários.
"""