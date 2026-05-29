# Backlog — Symulator wywiadu klinicznego

## Status projektu

Aplikacja terminalowa do edukacyjnej symulacji wywiadu klinicznego dla psychologów, psychoterapeutów w szkoleniu oraz studentów psychologii.

Aktualne założenia:
- przypadki fikcyjne, edukacyjne;
- praca w kontekście Polski;
- klasyfikacja edukacyjna według ICD-11;
- dodatkowo pokazywany przybliżony odpowiednik ICD-10;
- tylko osoby dorosłe;
- w przyszłości osobny moduł dzieci i młodzieży;
- tryby limitu pytań: 12, 24, 48;
- tryby trudności: student, standard, egzamin;
- aplikacja nie służy do diagnozowania realnych pacjentów.

---

## Priorytet P0 — fundamenty techniczne

### 1. Uporządkowanie struktury projektu

Docelowa struktura:

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
├── pyproject.toml
├── backlog.md
├── agents.md
└── README.md
```

### 2. Przeniesienie przypadków z kodu Pythona do JSON

Cel:
- łatwa rozbudowa do kilkudziesięciu przypadków;
- separacja logiki aplikacji od danych kliniczno-edukacyjnych;
- możliwość walidacji przypadków testami.

### 3. Walidacja przypadków

Każdy przypadek powinien mieć wymagane pola:
- id;
- title;
- icd11_code;
- icd11_name;
- icd10_code;
- icd10_name;
- icd_mapping_note;
- hidden_diagnosis;
- category;
- case_difficulty;
- age_group;
- patient_profile;
- presenting_problem;
- clinical_facts;
- differential;
- safety_notes;
- required_topics;
- red_flags.

### 4. Deterministyczne losowanie przypadków

Wszystkie funkcje używające losowości muszą przyjmować jawny `seed`.

Przykład:

```python
def choose_random_case(cases: list[Case], seed: int) -> Case:
    rng = random.Random(seed)
    return rng.choice(cases)
```

Nie używać bezpośrednio globalnego `random.choice()` w logice aplikacji.

---

## Priorytet P1 — dydaktyka i scoring

### 1. Checklisty kompetencji

Dodać punktację dla:
- jakości pytań otwartych;
- zebrania objawów osiowych;
- oceny czasu trwania;
- oceny wpływu na funkcjonowanie;
- oceny ryzyka;
- diagnostyki różnicowej;
- rozpoznania ograniczeń własnej hipotezy.

### 2. Tryb feedbacku dla studentów

Feedback powinien być bardziej edukacyjny:
- wyjaśniać znaczenie pominiętych pytań;
- tłumaczyć diagnostykę różnicową;
- sugerować lepszą strukturę wywiadu;
- nie zawstydzać użytkownika.

### 3. Tryb egzaminacyjny

Feedback bardziej zwięzły:
- wynik liczbowy;
- lista pominiętych krytycznych obszarów;
- najważniejsze błędy;
- rekomendacje do poprawy.

---

## Priorytet P2 — baza przypadków

### 1. Rozbudowa dorosłych przypadków ICD-11

Planowane kategorie:
- zaburzenia nastroju;
- zaburzenia lękowe;
- OCD i pokrewne;
- zaburzenia związane ze stresem;
- zaburzenia psychotyczne;
- zaburzenia osobowości;
- zaburzenia związane z używaniem substancji;
- zaburzenia odżywiania;
- zaburzenia neurorozwojowe u dorosłych, np. ADHD.

### 2. Warianty trudności przypadków

Rozróżnić:
- trudność samego przypadku;
- tryb zachowania pacjenta;
- limit pytań.

### 3. Przypadki mieszane

Dodać przypadki, gdzie główna trudność dotyczy różnicowania:
- depresja jednobiegunowa vs ChAD;
- OCD vs psychoza;
- panika vs problem somatyczny;
- ADHD vs hipomania;
- PTSD vs zaburzenie lękowe;
- osobowość borderline vs ChAD II.

---

## Priorytet P3 — przyszły moduł dzieci i młodzieży

Na razie nie implementować w rozmowie z pacjentem.

Przygotować model danych pod przyszłość:
- age_group: adult / adolescent / child;
- min_age;
- max_age;
- guardian_context;
- school_context;
- developmental_notes;
- consent_notes;
- family_interview_notes.

---

## Priorytet P4 — jakość i testy

### 1. Testy jednostkowe

Dodać testy:
- ładowania przypadków;
- walidacji wymaganych pól;
- deterministycznego losowania z seedem;
- generowania promptów;
- formatowania feedbacku.

### 2. Kontrola prompt leakage

Testować, czy prompt pacjenta zawiera zasady:
- nie ujawniaj diagnozy;
- nie ujawniaj kodów ICD;
- nie dawaj podpowiedzi diagnostycznych;
- odpowiadaj zgodnie z trybem trudności.

### 3. Testy statyczne

Docelowo dodać:
- ruff;
- mypy;
- pytest.

---

## Priorytet P5 — UX terminalowy

Dodać:
- `/help`;
- `/status`;
- `/diagnoza`;
- `/exit`;
- `/restart`;
- `/seed`;
- zapisywanie transkryptu do pliku;
- eksport feedbacku do Markdown;
- powtórzenie tego samego przypadku z tym samym seedem.

---

## Priorytet P6 — bezpieczeństwo

W każdej wersji utrzymać jasne ograniczenia:
- fikcyjne przypadki;
- brak diagnozowania realnych osób;
- brak zastępowania superwizji;
- brak zastępowania procedur kryzysowych;
- ostrożność przy samobójczości, psychozie, przemocy, substancjach i ryzyku medycznym.

