from nicegui import ui
from icd_dictionary import ICD_11_DICTIONARY, get_icd11_entry_by_code


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


def main():
    ui.label('Przeglądarka kodów ICD-11').classes('text-h4 q-mb-md')
    ui.markdown('Wybierz kod ICD-11, aby zobaczyć szczegóły (nazwy, tłumaczenia).')

    with ui.row():
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

if __name__ in ('__main__', '__mp_main__'):
    ui.run(title='ICD-11 Browser', reload=False)
