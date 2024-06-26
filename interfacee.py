import PySimpleGUI as sg
import locale
from datetime import datetime
from data_manager import load_data, save_data

# Define a localidade para formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def validate_input(value):
    """Valida a entrada para garantir que é um valor monetário."""
    if value == '':
        return True
    try:
        # Remove o símbolo de moeda e espaços antes de converter para float
        value = value.replace('R$', '').replace('.', '').replace(',', '.').strip()
        float(value)
        return True
    except ValueError:
        return False

def format_currency(value):
    """Formata um valor como moeda."""
    try:
        if isinstance(value, str):
            value = float(value.replace('R$', '').replace('.', '').replace(',', '.').strip())
        return locale.currency(value, grouping=True)
    except ValueError:
        return ""

def calculate_total(expenses):
    """Calcula a soma dos valores das despesas."""
    total = 0.0
    for expense in expenses:
        try:
            # Converte o valor da despesa para float antes de somar
            value = float(expense[2].replace('R$', '').replace('.', '').replace(',', '.').strip())
            total += value
        except ValueError:
            pass  # Ignora despesas com valores inválidos
    return total

# Carregar os dados existentes se houver
expenses = load_data()

# Layout da interface
layout = [
    [sg.Text("Descrição"), sg.Input(key='-DESC-')],
    [sg.CalendarButton("Data", target='-DATE-', format='%d/%m/%Y'), sg.Input(key='-DATE-', enable_events=True)],
    [sg.Text("Valor"), sg.Input(key='-VALUE-', enable_events=True, tooltip='Insira o valor no formato R$ 3000,00')],
    [sg.Button("Adicionar", key='-ADD-'), sg.Button("Sair")],
    [sg.Text("Despesas Pessoais", size=(40, 1))],
    [sg.Table(
        headings=["Descrição", "Data", "Valor", "Valor total"],
        values=expenses,
        key='-TABLE-',
        col_widths=[20, 20, 10, 15],
        auto_size_columns=False,
        display_row_numbers=False,
        justification='center',
        num_rows=10
    )]
]

# Criação da janela
window = sg.Window("Planilha de Despesas Pessoais", layout)

# Loop de eventos
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Sair":
        break
    if event == '-VALUE-':
        value = values['-VALUE-']
        if validate_input(value):
            window['-VALUE-'].update(value)
        else:
            window['-VALUE-'].update(value[:-1])
            sg.popup("Valor inválido. Por favor, insira um valor monetário válido.")
    if event == "-ADD-":
        desc = values['-DESC-']
        date = values['-DATE-']
        value = values['-VALUE-']

        try:
            date = datetime.strptime(date, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            sg.popup("Data inválida. Use o formato dd/mm/aaaa ou selecione usando o calendário.")
            continue

        if not validate_input(value):
            sg.popup("Valor inválido. Por favor, insira um valor monetário válido.")
            continue

        formatted_value = format_currency(value)
        if formatted_value == "":
            sg.popup("Valor inválido. Por favor, insira um valor monetário válido.")
            continue

        # Adiciona a despesa à lista
        new_expense = [desc, date, formatted_value, ""]
        expenses.append(new_expense)  # Inclui espaço para o "Valor total"

        # Atualiza o "Valor total" para cada linha na tabela
        last_total = calculate_total(expenses)
        new_expense[3] = format_currency(last_total)

        # Atualiza a tabela na interface
        window['-TABLE-'].update(values=expenses)

        # Limpa os campos de entrada
        window['-DESC-'].update('')
        window['-DATE-'].update('')
        window['-VALUE-'].update('')

# Salva os dados antes de fechar
save_data(expenses)

window.close()
