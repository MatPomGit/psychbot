# Psych Bot

**Psych Bot** to terminalowy, edukacyjny symulator wywiadu klinicznego dla psychologów, psychoterapeutów w szkoleniu oraz studentów psychologii.

Aplikacja pozwala ćwiczyć rozmowę z fikcyjnym dorosłym pacjentem, stawianie hipotez diagnostycznych, diagnostykę różnicową oraz ocenę ryzyka. Przypadki są projektowane według logiki **ICD-11**, z dodatkową informacją o przybliżonym starszym odpowiedniku w **ICD-10**.

> **Uwaga:** projekt służy wyłącznie do edukacyjnych symulacji. Nie jest narzędziem diagnostycznym, nie służy do oceny realnych pacjentów i nie zastępuje superwizji, konsultacji psychiatrycznej ani procedur kryzysowych obowiązujących w Polsce.

---

## Główne funkcje

Aktualnie projekt zakłada:

- terminalową rozmowę z symulowanym pacjentem;
- fikcyjne przypadki dorosłych pacjentów;
- wybór przypadku albo losowanie przypadku;
- limit pytań: **12**, **24** albo **48**;
- trzy tryby trudności rozmowy:
  - `student` — pacjent ujawnia trochę więcej;
  - `standard` — pacjent ujawnia informacje dopiero po dobrych pytaniach;
  - `egzamin` — pacjent nie pomaga, odpowiada realistycznie i oszczędnie;
- opis przypadków według ICD-11;
- przybliżone mapowanie do starszych kodów ICD-10;
- końcowe sformułowanie przypadku przez użytkownika;
- feedback superwizyjny obejmujący:
  - trafność hipotezy,
  - zebrane dane kliniczne,
  - pominięte obszary wywiadu,
  - diagnostykę różnicową,
  - ocenę ryzyka,
  - jakość rozmowy,
  - propozycje lepszych pytań.

---

## Dla kogo jest aplikacja

Projekt jest przeznaczony dla:

- psychologów;
- studentów psychologii;
- psychoterapeutów w szkoleniu;
- osób uczących się struktury wywiadu klinicznego;
- prowadzących zajęcia, którzy chcą tworzyć fikcyjne scenariusze treningowe.

Projekt **nie jest** przeznaczony do:

- diagnozowania realnych osób;
- zastępowania konsultacji klinicznej;
- zastępowania superwizji;
- prowadzenia terapii;
- oceny ryzyka w realnych sytuacjach kryzysowych.

---

## Aktualny zakres kliniczny

Aktualnie aplikacja zakłada wyłącznie **symulacje dorosłych pacjentów**.

Przykładowe początkowe obszary:

- epizod depresyjny;
- zaburzenie paniczne;
- zaburzenie obsesyjno-kompulsyjne;
- zaburzenie afektywne dwubiegunowe typu II / epizody hipomanii i depresji.

W przyszłości planowana jest rozbudowa do kilkudziesięciu przypadków oraz osobny moduł dla dzieci i młodzieży.

---

## Wymagania

- Python **3.11+**
- konto z dostępem do API modelu językowego;
- klucz API zapisany w zmiennej środowiskowej `OPENAI_API_KEY`.

Zależności runtime znajdują się w `requirements.txt`:

```txt
openai>=1.0.0
python-dotenv>=1.0.0
nicegui>=3.12.1
```

---

## Instalacja

Sklonuj albo utwórz katalog projektu:

```bash
mkdir psych-bot
cd psych-bot
```

### Automatycznie na Windows PowerShell

W katalogu projektu uruchom:

```powershell
.\setup_venv.ps1
```

Skrypt utworzy katalog `venv`, zaktualizuje `pip` i zainstaluje zależności z `requirements.txt`.

Jeśli chcesz odtworzyć środowisko od zera, użyj:

```powershell
.\setup_venv.ps1 -Force
```

Po zakończeniu aktywuj środowisko:

```powershell
.\venv\Scripts\Activate.ps1
```

### Ręcznie

Utwórz środowisko wirtualne:

```bash
python -m venv venv
```

Aktywuj środowisko:

```bash
# macOS / Linux
source venv/bin/activate
```

```bash
# Windows PowerShell
venv\Scripts\Activate.ps1
```

Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

---

## Konfiguracja zmiennych środowiskowych

Utwórz plik `.env` w katalogu głównym projektu:

```env
OPENAI_API_KEY=tu_wklej_swoj_klucz_api
```

Nie zapisuj klucza API bezpośrednio w kodzie i nie publikuj pliku `.env` w repozytorium.

Zalecany wpis w `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## Uruchomienie

W wersji jednoplikowej:

```bash
python psych_bot.py
```

GUI NiceGUI:

```powershell
.\run_gui.ps1
```

Skrypt uruchamia `gui.py` przez interpreter z `.\venv\Scripts\python.exe`, więc nie zależy od globalnego Pythona ani ustawień interpretera w edytorze.

Możesz też uruchomić GUI ręcznie po aktywacji środowiska:

```powershell
.\venv\Scripts\Activate.ps1
python gui.py
```

Jeśli port `8080` jest zajęty, aplikacja automatycznie wybierze kolejny wolny port. Możesz wymusić port:

```powershell
$env:PSYCHBOT_GUI_PORT = "8099"
.\run_gui.ps1
```

W docelowej wersji pakietowej:

```bash
python -m psych_bot.main
```

albo po instalacji pakietu:

```bash
psych-bot
```

---

## Przykładowy przebieg

```text
SYMULATOR WYWIADU KLINICZNEGO — WERSJA EDUKACYJNA

Wybierz limit pytań:
1. 12 pytań
2. 24 pytania
3. 48 pytań

> 1

Wybierz tryb trudności rozmowy:
1. student  — pacjent ujawnia trochę więcej
2. standard — pacjent ujawnia informacje dopiero po dobrych pytaniach
3. egzamin  — pacjent nie pomaga, odpowiada realistycznie i oszczędnie

> standard

Wybierz tryb:
1. Sam wybieram przypadek
2. Bot losuje przypadek

> 2

ĆWICZENIE ROZPOCZĘTE
Rozmawiasz z fikcyjnym dorosłym pacjentem.
Limit pytań psychologa: 12
Tryb trudności rozmowy: standard
Klasyfikacja edukacyjna: ICD-11
Kontekst: praca psychologiczna w Polsce

Pacjent: Nie wiem, od czego zacząć... ostatnio mam wrażenie, że wszystko mnie przerasta.

Psycholog [0/12]: Od jak dawna ma Pani takie poczucie?

Pacjent: Chyba od około dwóch miesięcy. Myślałam, że to przejdzie, ale jest coraz trudniej.
```

Po wpisaniu:

```text
/diagnoza
```

użytkownik podaje:

```text
1. Główna hipoteza diagnostyczna
2. Diagnozy różnicowe
3. Dane wspierające hipotezę
4. Czego jeszcze trzeba dopytać
5. Ocena ryzyka / czerwone flagi
```

Następnie aplikacja generuje feedback superwizyjny.

---

## Komendy w trakcie rozmowy

Planowane i/lub zalecane komendy terminalowe:

```text
/help      — pokaż dostępne komendy
/status    — pokaż liczbę wykorzystanych i pozostałych pytań
/diagnoza  — zakończ rozmowę i przejdź do sformułowania przypadku
/exit      — zakończ program
/restart   — rozpocznij nowe ćwiczenie
/seed      — pokaż albo ustaw seed dla replikowalnego losowania
```

---

## Limity pytań

Aplikacja obsługuje trzy limity:

| Limit | Zastosowanie |
|---:|---|
| 12 | tryb egzaminacyjny, szybki wywiad, presja priorytetyzacji |
| 24 | standardowe ćwiczenie wywiadu |
| 48 | dłuższy tryb treningowy i eksploracyjny |

Limit pytań ma uczyć selekcji informacji. Użytkownik powinien dążyć nie tylko do „zgadnięcia diagnozy”, ale do zebrania danych pozwalających uzasadnić hipotezę, różnicowanie i ocenę ryzyka.

---

## Tryby trudności

### `student`

Pacjent ujawnia trochę więcej.

Charakterystyka:

- odpowiedzi są trochę pełniejsze;
- po trafnym pytaniu pacjent może dodać 1–2 powiązane szczegóły;
- tryb dobry do nauki struktury wywiadu;
- pacjent nadal nie ujawnia diagnozy ani kodów ICD.

### `standard`

Pacjent ujawnia informacje dopiero po dobrych pytaniach.

Charakterystyka:

- odpowiedzi są realistyczne i umiarkowanie szczegółowe;
- pytania ogólne dają odpowiedzi ogólne;
- pytania precyzyjne ujawniają istotne fakty kliniczne;
- tryb dobry do regularnego treningu.

### `egzamin`

Pacjent nie pomaga, odpowiada realistycznie i oszczędnie.

Charakterystyka:

- odpowiedzi są krótkie;
- pacjent nie rozwija spontanicznie tematu;
- niejasne pytania dają niejasne odpowiedzi;
- kluczowe informacje pojawiają się tylko po adekwatnych pytaniach;
- tryb dobry do sprawdzania umiejętności.

---

## ICD-11 i ICD-10

Główną klasyfikacją edukacyjną projektu jest **ICD-11**.

Każdy przypadek powinien mieć:

```python
icd11_code: str
icd11_name: str
icd10_code: str
icd10_name: str
icd_mapping_note: str
```

Przykład:

```python
icd11_code = "6B20"
icd11_name = "Obsessive-compulsive disorder"
icd10_code = "F42"
icd10_name = "Zaburzenie obsesyjno-kompulsyjne"
icd_mapping_note = (
    "Przybliżony odpowiednik edukacyjny. Szczegółowy kod ICD-10 może zależeć "
    "od dominacji myśli natrętnych, czynności natrętnych lub obrazu mieszanego."
)
```

Mapowanie ICD-11 ↔ ICD-10 nie zawsze jest jednoznaczne. Dlatego projekt traktuje kod ICD-10 jako starszy, przybliżony odpowiednik edukacyjny, a nie jako automatyczne formalne kodowanie.

---

## Replikowalność i seed

Każda losowość w projekcie musi być replikowalna.

Nie używać:

```python
random.choice(cases)
```

Zamiast tego używać lokalnego generatora z jawnym seedem:

```python
import random

def choose_random_case(cases: list[Case], seed: int) -> Case:
    """Choose a case deterministically using an explicit random seed.

    Args:
        cases: Non-empty list of available cases.
        seed: Seed used to initialize a local random generator.

    Returns:
        A selected case.

    Raises:
        ValueError: If the case list is empty.
    """
    if not cases:
        raise ValueError("Cannot choose a case from an empty list.")

    rng = random.Random(seed)
    return rng.choice(cases)
```

Seed powinien być zapisywany razem z transkryptem ćwiczenia, aby można było odtworzyć ten sam scenariusz.

---

## Standard kodu

Zgodnie z `agents.md`:

- każda funkcja musi mieć **type hints**;
- każda funkcja musi mieć **docstring**;
- losowość musi mieć jawny `seed`;
- kod powinien rozdzielać:
  - logikę aplikacji,
  - wejście/wyjście terminalowe,
  - wywołania API,
  - dane przypadków,
  - scoring;
- nie należy przechowywać kluczy API w kodzie;
- nie należy mieszać realnych danych pacjentów z fikcyjnymi przypadkami.

Przykład dobrej funkcji:

```python
def format_case_label(case: Case) -> str:
    """Return a human-readable label for a case selection menu.

    Args:
        case: Case object containing ICD metadata and title.

    Returns:
        Formatted case label for terminal display.
    """
    return (
        f"{case.title} "
        f"[ICD-11: {case.icd11_code}; ICD-10: {case.icd10_code}]"
    )
```

---

## Docelowa struktura projektu

Docelowo projekt powinien zostać rozbity na moduły:

```text
psych-bot/
├── psych_bot/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── prompts.py
│   ├── openai_client.py
│   ├── case_loader.py
│   ├── scoring.py
│   └── config.py
├── cases/
│   ├── adult/
│   │   ├── icd11_6a70_depressive_episode_01.json
│   │   ├── icd11_6b01_panic_disorder_01.json
│   │   ├── icd11_6b20_ocd_01.json
│   │   └── icd11_6a61_bipolar_type_ii_01.json
├── tests/
│   ├── test_case_loader.py
│   ├── test_prompts.py
│   └── test_scoring.py
├── requirements.txt
├── run_gui.ps1
├── setup_venv.ps1
├── pyproject.toml
├── backlog.md
├── agents.md
└── README.md
```

---

## Pliki projektowe

### `requirements.txt`

Minimalne zależności runtime.

### `run_gui.ps1`

Skrypt PowerShell uruchamiający GUI przez lokalny interpreter z katalogu `venv`.

### `setup_venv.ps1`

Skrypt PowerShell tworzący lokalny katalog `venv` i instalujący zależności z `requirements.txt`.

### `pyproject.toml`

Konfiguracja projektu, narzędzi developerskich, `ruff`, `mypy` i `pytest`.

### `backlog.md`

Lista zadań i plan rozwoju projektu.

### `agents.md`

Wytyczne dla agentów AI i programistów pracujących nad kodem.

### `README.md`

Ten plik: opis projektu, instalacja, uruchomienie i zasady użycia.

---

## Plan rozwoju

Najbliższe kroki:

1. Przenieść przypadki z kodu Pythona do plików JSON.
2. Dodać walidację struktury przypadków.
3. Dodać deterministyczne losowanie z seedem.
4. Dodać eksport transkryptu do Markdown.
5. Dodać testy jednostkowe.
6. Dodać scoring checklisty.
7. Rozbudować bazę dorosłych przypadków do kilkudziesięciu.
8. Przygotować osobny model danych dla dzieci i młodzieży.
9. Dodać tryb egzaminacyjny z bardziej surową punktacją.
10. Dodać tryb dydaktyczny dla prowadzących zajęcia.

---

## Bezpieczeństwo i etyka

Projekt dotyczy obszaru zdrowia psychicznego, dlatego wymaga ostrożnego projektowania.

Stałe zasady:

- przypadki są fikcyjne;
- użytkownik nie powinien wprowadzać danych realnych pacjentów;
- aplikacja nie tworzy formalnej diagnozy;
- aplikacja nie zastępuje superwizji;
- aplikacja nie zastępuje dokumentacji ICD-11 ani ICD-10;
- aplikacja nie zastępuje lokalnych procedur reagowania kryzysowego;
- w feedbacku należy szczególnie oceniać pominięcie czerwonych flag.

W przypadku realnego zagrożenia życia, samobójczości, przemocy lub ostrego kryzysu psychicznego należy korzystać z właściwych procedur kryzysowych i profesjonalnej pomocy, a nie z tej aplikacji.

---

## Licencja

Na tym etapie projekt ma status roboczy. Licencja powinna zostać doprecyzowana przed publicznym udostępnieniem repozytorium.

---

## Status

Wersja: `0.1.0`

Status: prototyp edukacyjny / alpha.
