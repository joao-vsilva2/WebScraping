from tkinter import END, filedialog
import pandas as pd

# Função para salvar os resultados em um arquivo Excel
def save_to_excel(scraped_data, result_text):
    if not scraped_data:
        result_text.insert(END, "\nNenhum dado para salvar.", "red")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df = pd.DataFrame(scraped_data, columns=["Dados"])
        df.to_excel(file_path, index=False)
        result_text.insert(END, f"\nDados salvos em: {file_path}", "green")