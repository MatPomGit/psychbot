# AGENTS.md — wytyczne dla agentów pracujących nad projektem

Ten dokument opisuje zasady dla agentów AI i programistów modyfikujących projekt **psych-bot**.

Projekt jest edukacyjnym symulatorem wywiadu klinicznego. Nie jest narzędziem diagnostycznym ani medycznym.

---

## 1. Cel projektu

Budujemy terminalową aplikację edukacyjną dla:
- psychologów;
- psychoterapeutów w szkoleniu;
- studentów psychologii.

Aplikacja symuluje fikcyjnych dorosłych pacjentów i pozwala ćwiczyć:
- prowadzenie wywiadu;
- rozumowanie diagnostyczne;
- diagnostykę różnicową;
- ocenę ryzyka;
- formułowanie hipotezy klinicznej.

---

## 2. Ograniczenia kliniczne i bezpieczeństwo

Każda zmiana w projekcie musi zachowywać następujące zasady:

1. Aplikacja nie diagnozuje realnych pacjentów.
2. Aplikacja generuje wyłącznie fikcyjne przypadki treningowe.
3. Aplikacja nie zastępuje superwizji klinicznej.
4. Aplikacja nie zastępuje konsultacji psychiatrycznej.
5. Aplikacja nie zastępuje procedur kryzysowych obowiązujących w Polsce.
6. Pacjent symulowany nie może ujawniać diagnozy w trakcie wywiadu.
7. Pacjent symulowany nie może ujawniać kodu ICD-11 ani ICD-10 w trakcie wywiadu.
8. Feedback może odnosić się do ICD-11 i przybliżonego mapowania ICD-10, ale musi zaznaczać edukacyjny charakter symulacji.
9. W przypadkach dotyczących samobójczości, psychozy, przemocy, substancji lub poważnego ryzyka somatycznego feedback musi sprawdzać, czy użytkownik zbadał czerwone flagi.

---

## 3. Standard kodu

### 3.1. Type hints są obowiązkowe

Każda funkcja musi mieć adnotacje typów dla:
- wszystkich parametrów;
- wartości zwracanej.

Poprawnie:

```python
def choose_question_limit(available_limits: list[int]) -> int:
    """Return a validated question limit selected by the user."""
    ...
```

Niepoprawnie:

```python
def choose_question_limit(available_limits):
    ...
```

### 3.2. Docstringi są obowiązkowe

Każda funkcja musi mieć docstring.

Docstring powinien krótko opisywać:
- co funkcja robi;
- jakie przyjmuje dane;
- co zwraca;
- ważne założenia lub efekty uboczne.

Przykład:

```python
def build_patient_prompt(case: Case, question_limit: int, difficulty_mode: str) -> str:
    """Build the system prompt used to simulate a fictional adult patient.

    Args:
        case: Training case containing ICD metadata and clinical facts.
        question_limit: Maximum number of psychologist questions allowed.
        difficulty_mode: Conversation difficulty mode: student, standard, or egzamin.

    Returns:
        A system prompt for the patient-simulation model.
    """
    ...
```

### 3.3. Unikać funkcji bezpośrednio zależnych od input/output

Tam, gdzie to możliwe, oddzielać:
- logikę biznesową;
- wejście terminalowe;
- drukowanie wyniku;
- wywołania API.

Lepszy wzorzec:

```python
def format_case_label(case: Case) -> str:
    """Return a human-readable label for a case selection menu."""
    return f"{case.title} [ICD-11: {case.icd11_code}; ICD-10: {case.icd10_code}]"
```

Gorszy wzorzec:

```python
def print_case(case):
    print(case.title)
```

### 3.4. Preferować małe funkcje

Funkcje powinny mieć pojedynczą odpowiedzialność.

Jeśli funkcja:
- wybiera przypadek,
- pyta użytkownika,
- losuje,
- buduje prompt,
- wywołuje API,
- drukuje feedback,

to znaczy, że powinna zostać rozbita na mniejsze funkcje.

---

## 4. Losowość i replikowalność

Każde użycie losowości musi być replikowalne.

### 4.1. Nie używać globalnego random bez seeda

Niepoprawnie:

```python
import random

case = random.choice(cases)
```

Poprawnie:

```python
import random

def choose_random_case(cases: list[Case], seed: int) -> Case:
    """Choose a case deterministically using an explicit random seed.

    Args:
        cases: Non-empty list of available training cases.
        seed: Seed used to initialize a local random generator.

    Returns:
        One selected case.

    Raises:
        ValueError: If the cases list is empty.
    """
    if not cases:
        raise ValueError("Cannot choose a case from an empty list.")

    rng = random.Random(seed)
    return rng.choice(cases)
```

### 4.2. Seed powinien być jawny

Każda funkcja, która losuje, powinna przyjmować `seed: int`.

Dopuszczalne:
- domyślny seed w konfiguracji, np. `DEFAULT_RANDOM_SEED = 42`;
- użytkownik podaje seed w terminalu;
- seed zapisywany jest w transkrypcie ćwiczenia.

Niedopuszczalne:
- ukryte losowanie zależne od czasu;
- brak możliwości odtworzenia tego samego przypadku;
- mieszanie globalnego stanu `random`.

### 4.3. Transkrypt powinien zapisywać seed

Przy eksporcie transkryptu zapisać:
- id przypadku;
- seed;
- limit pytań;
- tryb trudności;
- datę wykonania;
- wersję aplikacji.

---

## 5. Zasady pracy z ICD-11 i ICD-10

### 5.1. ICD-11 jest klasyfikacją główną

Przypadki powinny być opisywane według ICD-11.

Wymagane pola:
- `icd11_code`;
- `icd11_name`.

### 5.2. ICD-10 jest starszym odpowiednikiem edukacyjnym

Dla każdego przypadku dodać:
- `icd10_code`;
- `icd10_name`;
- `icd_mapping_note`.

Mapowanie ICD-11 ↔ ICD-10 nie zawsze jest 1:1.

Dlatego w polu `icd_mapping_note` zaznaczać, czy:
- kod ICD-10 jest tylko przybliżony;
- szczegółowy kod zależy od epizodu, nasilenia lub specyfikatora;
- przypadek ma niejednoznaczne mapowanie.

### 5.3. Nie wymyślać kodów bez weryfikacji

Przy dodawaniu nowych przypadków:
- sprawdzić kod w oficjalnych lub wiarygodnych źródłach;
- nie polegać wyłącznie na pamięci modelu;
- dodać notatkę o mapowaniu.

---

## 6. Zasady promptów

### 6.1. Prompt pacjenta

Prompt pacjenta musi zawierać zasady:

- przypadek jest fikcyjny;
- pacjent nie ujawnia diagnozy;
- pacjent nie ujawnia kodów ICD;
- pacjent nie mówi językiem podręcznikowym;
- pacjent odpowiada zgodnie z trybem trudności;
- pacjent ujawnia informacje stopniowo;
- pacjent nie ocenia pytań psychologa w trakcie rozmowy;
- pacjent nie udziela porad terapeutycznych;
- pacjent nie diagnozuje użytkownika.

### 6.2. Prompt feedbacku

Prompt feedbacku musi oceniać:

- trafność hipotezy;
- dane kliniczne;
- pokrycie checklisty;
- diagnostykę różnicową;
- ocenę ryzyka;
- jakość rozmowy;
- pytania, które warto było zadać;
- ocenę końcową.

Feedback musi uwzględniać:
- limit pytań;
- liczbę wykorzystanych pytań;
- tryb trudności;
- poziom użytkownika, w tym studentów;
- ICD-11;
- przybliżony odpowiednik ICD-10.

---

## 7. Tryby trudności

Projekt używa trzech trybów:

### student

Pacjent ujawnia trochę więcej.

Zasady:
- odpowiedzi nieco pełniejsze;
- po trafnym pytaniu pacjent może dodać 1–2 powiązane szczegóły;
- nadal nie ujawnia diagnozy;
- nadal nie podaje kodów ICD;
- nie daje gotowych etykiet diagnostycznych.

### standard

Pacjent ujawnia informacje dopiero po dobrych pytaniach.

Zasady:
- realistyczna, umiarkowana szczegółowość;
- pytania ogólne dają ogólne odpowiedzi;
- pytania precyzyjne ujawniają fakty kliniczne;
- pacjent nie podpowiada, o co pytać.

### egzamin

Pacjent nie pomaga, odpowiada realistycznie i oszczędnie.

Zasady:
- krótkie odpowiedzi;
- brak spontanicznego rozwijania;
- niejasne pytania dają niejasne odpowiedzi;
- kluczowe informacje tylko po adekwatnym pytaniu;
- możliwe bagatelizowanie lub wstyd zgodnie z profilem.

---

## 8. Testy wymagane przy nowych zmianach

Przy modyfikacji logiki dodać lub zaktualizować testy dla:

1. ładowania przypadków;
2. walidacji wymaganych pól;
3. deterministycznego losowania z seedem;
4. generowania promptu pacjenta;
5. generowania promptu feedbacku;
6. zachowania limitu pytań;
7. obsługi trybów trudności;
8. formatowania ICD-11 i ICD-10.

---

## 9. Styl komunikatów terminalowych

Komunikaty powinny być:
- jasne;
- po polsku;
- krótkie;
- edukacyjne;
- nieoceniające.

Unikać:
- tonu medycznej pewności;
- sugerowania, że wynik jest diagnozą;
- alarmistycznego tonu poza sytuacjami związanymi z ryzykiem.

---

## 10. Zakazane wzorce

Nie dodawać kodu, który:

1. Diagnozuje realnego użytkownika.
2. Zachęca do używania aplikacji zamiast superwizji.
3. Pozwala pacjentowi ujawnić diagnozę w trakcie rozmowy.
4. Losuje przypadki bez jawnego seeda.
5. Dodaje funkcje bez type hints.
6. Dodaje funkcje bez docstringów.
7. Miesza logikę kliniczno-edukacyjną z I/O terminalowym bez potrzeby.
8. Przechowuje klucze API w kodzie.
9. Publikuje transkrypty zawierające dane realnych osób.
10. Udaje formalną dokumentację medyczną.

