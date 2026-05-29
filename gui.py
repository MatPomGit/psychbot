import os
import socket
from collections.abc import MutableMapping
from typing import Any

from dotenv import load_dotenv
from icd_dictionary import ICD_11_DICTIONARY, get_icd11_entry_by_code
from nicegui import ui


DEFAULT_GUI_PORT = 8080
MAX_PORT_ATTEMPTS = 20


def find_available_port(start_port: int = DEFAULT_GUI_PORT) -> int:
    """Zwraca pierwszy wolny port lokalny zaczynając od podanej wartości.

    Args:
        start_port: Pierwszy port sprawdzany przy uruchamianiu GUI.

    Returns:
        Numer wolnego portu, którego może użyć serwer NiceGUI.

    Raises:
        RuntimeError: Gdy nie znaleziono wolnego portu w badanym zakresie.
    """
    for port in range(start_port, start_port + MAX_PORT_ATTEMPTS):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port

    raise RuntimeError("Nie znaleziono wolnego portu dla GUI.")


def get_gui_port() -> int:
    """Pobiera port GUI ze zmiennej środowiskowej albo wybiera wolny port.

    Returns:
        Numer portu dla serwera NiceGUI.

    Raises:
        ValueError: Gdy zmienna PSYCHBOT_GUI_PORT nie jest liczbą.
    """
    raw_port = os.getenv("PSYCHBOT_GUI_PORT", "").strip()
    if raw_port:
        return int(raw_port)

    return find_available_port()


def get_icd11_options() -> dict[str, str]:
    """Zwraca opcje kodów ICD-11 do pola wyboru w GUI.

    Returns:
        Słownik mapujący kod ICD-11 na etykietę widoczną w interfejsie.
    """
    return {
        entry["code"]: f"{entry['code']} - {entry['name_pl']}"
        for entry in ICD_11_DICTIONARY
    }


def show_icd11_details(code: str) -> None:
    """Wyświetla szczegóły wybranego kodu ICD-11 w aktualnym kontenerze.

    Args:
        code: Kod ICD-11 wybrany przez użytkownika.

    Returns:
        None.
    """
    entry = get_icd11_entry_by_code(code)
    if entry:
        ui.markdown(f"**Kod ICD-11:** {entry['code']}")
        ui.markdown(f"**Nazwa angielska:** {entry['name_en']}")
        ui.markdown(f"**Nazwa polska:** {entry['name_pl']}")
    else:
        ui.markdown("Nie znaleziono wpisu dla podanego kodu.")


def save_api_key_to_env(api_key: str) -> None:
    """Zapisuje klucz API do pliku .env.

    Args:
        api_key: Klucz API wpisany przez użytkownika.

    Returns:
        None.
    """
    lines: list[str] = []
    if os.path.exists(".env"):
        with open(".env", encoding="utf-8") as file:
            lines = file.readlines()

    found = False
    for index, line in enumerate(lines):
        if line.startswith("OPENAI_API_KEY="):
            lines[index] = f"OPENAI_API_KEY={api_key}\n"
            found = True

    if not found:
        lines.append(f"OPENAI_API_KEY={api_key}\n")

    with open(".env", "w", encoding="utf-8") as file:
        file.writelines(lines)


def get_api_key_from_env() -> str:
    """Pobiera klucz API z pliku .env lub zmiennych środowiskowych.

    Returns:
        Klucz API bez białych znaków albo pusty tekst.
    """
    load_dotenv()
    return os.getenv("OPENAI_API_KEY", "").strip()


def render_chat_history(messages: list[dict[str, str]]) -> None:
    """Renderuje historię rozmowy w aktualnym kontenerze NiceGUI.

    Args:
        messages: Lista wiadomości z nadawcą i tekstem.

    Returns:
        None.
    """
    for message in messages:
        is_user = message["sender"] == "user"
        ui.chat_message(
            text=message["text"],
            name="Ty" if is_user else "Pacjent",
            sent=is_user,
        )


def add_message(
    messages: list[dict[str, str]],
    messages_container: ui.element,
    sender: str,
    text: str,
) -> None:
    """Dodaje wiadomość do historii i odświeża widok rozmowy.

    Args:
        messages: Aktualna historia rozmowy.
        messages_container: Kontener NiceGUI z wiadomościami.
        sender: Nadawca wiadomości: user albo bot.
        text: Treść wiadomości.

    Returns:
        None.
    """
    messages.append({"sender": sender, "text": text})
    messages_container.clear()
    with messages_container:
        render_chat_history(messages)


def build_gui() -> None:
    """Buduje główny interfejs aplikacji NiceGUI.

    Returns:
        None.
    """
    api_key = get_api_key_from_env()
    api_state: MutableMapping[str, str] = {"key": api_key}

    ui.label("Psych Bot").classes("text-h4 q-mb-md")

    with ui.row().classes("items-start q-gutter-xl"):
        with ui.column().classes("q-gutter-md"):
            ui.label("Przeglądarka kodów ICD-11").classes("text-h5")
            ui.markdown("Wybierz kod ICD-11, aby zobaczyć szczegóły.")

            options = get_icd11_options()
            first_code = next(iter(options), None)
            selected = ui.select(
                options=options,
                value=first_code,
                label="Kod ICD-11",
            ).classes("q-mb-md")

            details_container = ui.column().classes("q-gutter-xs")

            def refresh_icd11_details(code: str | None) -> None:
                """Odświeża panel szczegółów ICD-11 dla wybranego kodu.

                Args:
                    code: Aktualnie wybrany kod ICD-11.

                Returns:
                    None.
                """
                details_container.clear()
                with details_container:
                    if code:
                        show_icd11_details(code)

            def handle_icd11_change(event: Any) -> None:
                """Obsługuje zmianę wyboru kodu ICD-11.

                Args:
                    event: Zdarzenie NiceGUI zawierające nową wartość pola wyboru.

                Returns:
                    None.
                """
                refresh_icd11_details(event.value)

            selected.on("change", handle_icd11_change)
            refresh_icd11_details(first_code)

        with ui.column().classes("q-gutter-md"):
            ui.label("Symulowana rozmowa z pacjentem").classes("text-h5")

            with ui.column().classes("q-gutter-sm"):
                ui.markdown("**Ustawienia API**")
                api_input = ui.input(
                    label="OpenAI API Key",
                    value=api_key,
                    password=True,
                )
                api_info = ui.label("")

                def handle_save_api() -> None:
                    """Zapisuje klucz API podany w formularzu.

                    Returns:
                        None.
                    """
                    key = str(api_input.value or "").strip()
                    save_api_key_to_env(key)
                    api_state["key"] = key
                    api_info.text = "Klucz zapisany. Nowe rozmowy użyją tej wartości."

                ui.button("Zapisz klucz API", icon="save", on_click=handle_save_api)

            messages: list[dict[str, str]] = []
            messages_container = ui.column().classes("q-gutter-sm w-full")
            user_input = ui.input(label="Twoje pytanie do pacjenta...").props("autofocus")

            def handle_send() -> None:
                """Dodaje pytanie użytkownika i lokalną odpowiedź testową.

                Returns:
                    None.
                """
                question = str(user_input.value or "").strip()
                if not question:
                    return

                add_message(messages, messages_container, "user", question)
                if not api_state["key"]:
                    answer = f"(tryb offline) {question[::-1]}"
                else:
                    answer = f"(API placeholder) {question[::-1]}"

                add_message(messages, messages_container, "bot", answer)
                user_input.value = ""

            ui.button("Wyślij", icon="send", on_click=handle_send)
            user_input.on("keydown.enter", handle_send)


if __name__ in ("__main__", "__mp_main__"):
    build_gui()
    port = get_gui_port()
    ui.run(title="Psych Bot", port=port, reload=False)
