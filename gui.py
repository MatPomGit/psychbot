
import os
from nicegui import ui
from icd_dictionary import ICD_11_DICTIONARY, get_icd11_entry_by_code
from dotenv import load_dotenv


def get_icd11_options():
    """Zwraca listę opcji (kod + polska nazwa) do wyboru w GUI."""
    return [
        (f"{entry['code']} — {entry['name_pl']}", entry['code'])
        for entry in ICD_11_DICTIONARY
    ]


def show_icd11_details(code: str):
    entry = get_icd11_entry_by_code(code)
    if entry:
        ui.markdown(f"**Kod ICD-11:** {entry['code']}")
        ui.markdown(f"**Nazwa angielska:** {entry['name_en']}")
        ui.markdown(f"**Nazwa polska:** {entry['name_pl']}")
    else:
        ui.markdown('Nie znaleziono wpisu dla podanego kodu.')



def save_api_key_to_env(api_key: str) -> None:
    """Zapisuje klucz API do pliku .env."""
    lines = []
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith('OPENAI_API_KEY='):
            lines[i] = f'OPENAI_API_KEY={api_key}\n'
            found = True
    if not found:
        lines.append(f'OPENAI_API_KEY={api_key}\n')
    with open('.env', 'w', encoding='utf-8') as f:
        f.writelines(lines)

def get_api_key_from_env() -> str:
    """Pobiera klucz API z pliku .env lub zmiennych środowiskowych."""
    load_dotenv()
    return os.getenv('OPENAI_API_KEY', '').strip()

def main():


    api_key = get_api_key_from_env()
    api_state = {'key': api_key}

    with ui.row():
        ui.label('Przeglądarka kodów ICD-11').classes('text-h4 q-mb-md')
        ui.label('Symulowana rozmowa z pacjentem').classes('text-h4 q-mb-md q-ml-xl')
        # Panel do wpisania klucza API
        with ui.column().classes('q-ml-xl'):
            ui.markdown('**Ustawienia API**')
            api_input = ui.input(label='OpenAI API Key', value=api_key, password=True)
            save_btn = ui.button('Zapisz klucz API', icon='save')
            api_info = ui.label('')

            def handle_save_api():
                key = api_input.value.strip()
                save_api_key_to_env(key)
                api_state['key'] = key
                api_info.text = 'Klucz zapisany. Uruchom ponownie aplikację, aby użyć nowego klucza.'

            save_btn.on('click', handle_save_api)


    with ui.row():
        # Lewa kolumna: ICD-11
        with ui.column():
            ui.markdown('Wybierz kod ICD-11, aby zobaczyć szczegóły (nazwy, tłumaczenia).')
            options = get_icd11_options()
            selected = ui.select(options, label='Kod ICD-11').classes('q-mb-md')

            @selected.on('change')
            def on_change(e):
                ui.clear()
                main()
                if e.value:
                    show_icd11_details(e.value)

            # Pokaż szczegóły pierwszego kodu na starcie
            if options:
                show_icd11_details(options[0][1])

        # Prawa kolumna: Rozmowa z pacjentem
        with ui.column().classes('q-ml-xl'):
            ui.markdown('**Symulowana rozmowa z pacjentem**')
            conversation = ui.chat(height=400)
            user_input = ui.input(label='Twoje pytanie do pacjenta...').props('autofocus')
            send_btn = ui.button('Wyślij', icon='send')

            # Przechowuj historię rozmowy w stanie
            state = {'history': []}

            def add_message(sender: str, text: str) -> None:
                """Dodaje wiadomość do historii i wyświetla ją w oknie rozmowy."""
                state['history'].append({'sender': sender, 'text': text})
                conversation.clear()
                for msg in state['history']:
                    if msg['sender'] == 'user':
                        conversation.message(msg['text'], sent=True, name='Ty')
                    else:
                        conversation.message(msg['text'], sent=False, name='Pacjent')

            def handle_send() -> None:
                pytanie = user_input.value.strip()
                if not pytanie:
                    return
                add_message('user', pytanie)
                # Tryb offline: jeśli nie ma klucza API, generuj lokalną odpowiedź
                if not api_state['key']:
                    odpowiedz = f"(tryb offline) {pytanie[::-1]}"
                else:
                    # Tu można podpiąć wywołanie API (placeholder)
                    odpowiedz = f"(API placeholder) {pytanie[::-1]}"
                add_message('bot', odpowiedz)
                user_input.value = ''

            send_btn.on('click', handle_send)
            user_input.on('keydown.enter', handle_send)

if __name__ in ('__main__', '__mp_main__'):
    ui.run(title='ICD-11 Browser', reload=False)
