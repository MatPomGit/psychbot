import os
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from icd_dictionary import get_icd11_entry_by_code
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# KONFIGURACJA APLIKACJI
# ============================================================

APP_CONTEXT = """
Aplikacja działa w Polsce.
Użytkownikami są psychologowie, psychoterapeuci w szkoleniu oraz studenci psychologii.
Symulacje dotyczą wyłącznie dorosłych pacjentów.
W przyszłości aplikacja może zostać rozszerzona o dzieci i młodzież, ale obecnie nie generuj przypadków osób poniżej 18 r.ż.

Klasyfikacja edukacyjna: ICD-11.
Uwaga: aplikacja nie zastępuje diagnozy klinicznej, superwizji, konsultacji psychiatrycznej,
lokalnych procedur kryzysowych ani aktualnych regulacji prawnych.
"""


AVAILABLE_QUESTION_LIMITS = [12, 24, 48]

DIFFICULTY_MODES = {
    "student": {
        "label": "student",
        "description": "Pacjent ujawnia trochę więcej i odpowiada nieco bardziej edukacyjnie.",
        "prompt_rules": """
TRYB STUDENT:
- Użytkownik może być studentem psychologii.
- Pacjent nadal nie ujawnia diagnozy ani kodów ICD.
- Pacjent odpowiada trochę pełniej niż w realnym, trudnym wywiadzie.
- Jeżeli pytanie użytkownika jest trafne, pacjent może spontanicznie dodać 1–2 powiązane szczegóły.
- Pacjent nie powinien być przesadnie enigmatyczny.
- Nie dawaj jednak gotowych etykiet diagnostycznych.
- Nie mów: „to brzmi jak depresja/OCD/panika/ChAD”.
"""
    },
    "standard": {
        "label": "standard",
        "description": "Pacjent ujawnia informacje dopiero po dobrych pytaniach.",
        "prompt_rules": """
TRYB STANDARD:
- Pacjent odpowiada realistycznie i umiarkowanie szczegółowo.
- Kluczowe informacje ujawnia dopiero wtedy, gdy użytkownik zada adekwatne pytania.
- Przy pytaniach ogólnych pacjent mówi głównie o problemie zgłaszanym.
- Przy pytaniach precyzyjnych pacjent ujawnia fakty kliniczne zgodne z kartą.
- Nie podpowiada użytkownikowi, o co powinien zapytać.
"""
    },
    "egzamin": {
        "label": "egzamin",
        "description": "Pacjent nie pomaga, odpowiada realistycznie i oszczędnie.",
        "prompt_rules": """
TRYB EGZAMIN:
- Pacjent odpowiada oszczędnie, realistycznie i bez pomagania użytkownikowi.
- Nie rozwija odpowiedzi ponad to, o co został zapytany.
- Przy pytaniach zamkniętych odpowiada krótko: tak/nie/nie wiem + ewentualnie jedno zdanie.
- Przy pytaniach niejasnych odpowiada niejasno.
- Nie ujawnia kluczowych informacji, jeśli użytkownik o nie nie zapyta.
- Może minimalizować, bagatelizować lub wstydzić się objawów, zgodnie z profilem pacjenta.
- Nie daje edukacyjnych wskazówek w trakcie wywiadu.
"""
    }
}

# ============================================================
# MODEL DANYCH PRZYPADKU
# ============================================================

@dataclass
@dataclass
class Case:
    """Model danych przypadku edukacyjnego do symulacji wywiadu klinicznego.

    Atrybuty:
        id: Unikalny identyfikator przypadku.
        title: Tytuł przypadku.
        icd11_code: Kod ICD-11.
        icd10_code: Kod ICD-10 (przybliżony odpowiednik).
        icd_mapping_note: Notatka o mapowaniu ICD-11 ↔ ICD-10.
        hidden_diagnosis: Ukryta diagnoza treningowa.
        category: Kategoria dydaktyczna.
        difficulty: Poziom trudności.
        adult_only: Czy przypadek dotyczy wyłącznie dorosłych.
        suitable_for_students: Czy przypadek nadaje się dla studentów.
        patient_profile: Profil pacjenta (opis).
        presenting_problem: Problem zgłaszany przez pacjenta.
        clinical_facts: Fakty kliniczne do stopniowego ujawniania.
        differential: Diagnostyka różnicowa.
        safety_notes: Notatki dotyczące bezpieczeństwa.
        required_topics: Lista wymaganych obszarów wywiadu.
        red_flags: Lista czerwonych flag.
    """
    id: str
    title: str
    icd11_code: str
    icd10_code: str
    icd_mapping_note: str
    hidden_diagnosis: str
    category: str
    difficulty: str
    adult_only: bool = True
    suitable_for_students: bool = True
    patient_profile: str = ""
    presenting_problem: str = ""
    clinical_facts: str = ""
    differential: str = ""
    safety_notes: str = ""
    required_topics: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)

    @property
    def icd11_name(self) -> str:
        """Zwraca angielską nazwę jednostki ICD-11 na podstawie kodu."""
        entry = get_icd11_entry_by_code(self.icd11_code)
        return entry["name_en"] if entry else "(nieznany kod)"

    @property
    def icd11_name_pl(self) -> str:
        """Zwraca polską nazwę jednostki ICD-11 na podstawie kodu."""
        entry = get_icd11_entry_by_code(self.icd11_code)
        return entry["name_pl"] if entry else "(nieznany kod)"


# ============================================================
# BAZA PRZYPADKÓW
# W przyszłości najlepiej przenieść ją do osobnego pliku cases.py
# albo do plików JSON/YAML.
# ============================================================

CASES = [
    # depressive_episode_01: Obniżony nastrój i wycofanie — przypadek treningowy ICD-11 6A70
    Case(
        id="icd11_6a70_depressive_episode_01",
        title="Obniżony nastrój i wycofanie",
        icd11_code="6A70",
        icd10_code="F32",
        icd_mapping_note="Przybliżony odpowiednik edukacyjny. Szczegółowy kod ICD-10 zależy od nasilenia i obecności objawów psychotycznych, np. F32.0–F32.3.",
        icd_mapping_note="Przybliżony odpowiednik edukacyjny. Szczegółowy kod ICD-10 zależy od nasilenia i obecności objawów psychotycznych, np. F32.0–F32.3.",
        hidden_diagnosis="Epizod depresyjny według logiki ICD-11 — przypadek treningowy",
        category="zaburzenia nastroju",
        difficulty="łatwy",
        patient_profile="""
            Imię: Marta
            Wiek: 34 lata
            Miejsce: duże miasto w Polsce
            Sytuacja: pracuje w księgowości, mieszka sama, ma kontakt z siostrą.
            Styl rozmowy: cicha, spowolniała, odpowiada raczej krótko, często mówi „nie wiem”.
            Nie używa terminów klinicznych. Nie mówi sama z siebie: „mam depresję”.
            """,
        presenting_problem="""
            Pacjentka zgłasza się, bo „od dłuższego czasu nie daje rady normalnie funkcjonować”.
            Na początku mówi głównie o zmęczeniu, problemach w pracy i izolowaniu się.
            """,
        clinical_facts="""
            Fakty do stopniowego ujawniania:
            - obniżony nastrój prawie codziennie od około 8 tygodni,
            - wyraźna utrata zainteresowań i przyjemności,
            - przestała biegać i spotykać się ze znajomymi,
            - trudności ze snem, szczególnie wczesne budzenie,
            - spadek apetytu,
            - poczucie winy i bezwartościowości,
            - pogorszenie koncentracji,
            - obniżona energia,
            - spowolnienie,
            - pogorszenie funkcjonowania zawodowego,
            - bierne myśli rezygnacyjne: „chciałabym zasnąć i się nie obudzić”,
            - brak konkretnego planu samobójczego, ale wymaga to dalszej oceny.
            Brak epizodów hipomaniakalnych lub maniakalnych.
            Brak objawów psychotycznych.
            Brak aktualnego nadużywania alkoholu lub innych substancji.
            """,
        differential="""
            Do różnicowania:
            - zaburzenie adaptacyjne,
            - żałoba,
            - zaburzenie afektywne dwubiegunowe,
            - zaburzenia lękowe,
            - zaburzenia związane z używaniem substancji,
            - przyczyny somatyczne, np. niedoczynność tarczycy, anemia, choroby przewlekłe.
            """,
        safety_notes="""
            Należy ocenić:
            - myśli samobójcze,
            - zamiar,
            - plan,
            - dostęp do środków,
            - wcześniejsze próby,
            - czynniki ochronne,
            - wsparcie społeczne,
            - konieczność pilnej konsultacji psychiatrycznej lub procedur kryzysowych.
            """,
        required_topics=[
            "czas trwania objawów",
            "nastrój",
            "anhedonia",
            "sen",
            "apetyt i masa ciała",
            "energia",
            "koncentracja",
            "poczucie winy lub bezwartościowości",
            "funkcjonowanie zawodowe i społeczne",
            "myśli samobójcze",
            "mania lub hipomania w wywiadzie",
            "substancje",
            "czynniki somatyczne"
        ],
        red_flags=[
            "bierne myśli rezygnacyjne",
            "możliwe ryzyko samobójcze",
            "znaczne pogorszenie funkcjonowania"
        ]
    ),

    # panic_disorder_01: Napady silnego lęku i objawy z ciała — przypadek treningowy ICD-11 6B01
    Case(
        id="icd11_6b01_panic_disorder_01",
        title="Napady silnego lęku i objawy z ciała",
        icd11_code="6B01",
        icd10_code="F41.0",
        icd_mapping_note="Przybliżony odpowiednik edukacyjny ICD-10 dla zaburzenia panicznego.",
        icd_mapping_note="Przybliżony odpowiednik edukacyjny ICD-10 dla zaburzenia panicznego.",
        hidden_diagnosis="Zaburzenie paniczne według logiki ICD-11 — przypadek treningowy",
        category="zaburzenia lękowe",
        difficulty="łatwy/średni",
        patient_profile="""
            Imię: Kamil
            Wiek: 28 lat
            Miejsce: Polska, miasto wojewódzkie
            Sytuacja: pracuje jako informatyk, mieszka z partnerką.
            Styl rozmowy: napięty, skupiony na objawach somatycznych, boi się choroby serca.
            Nie mówi: „mam ataki paniki”. Mówi raczej: „chyba coś jest nie tak z sercem”.
            """,
        presenting_problem="""
            Pacjent zgłasza nagłe epizody kołatania serca, duszności i przerażenia.
            Najbardziej martwi go możliwość choroby somatycznej.
            """,
        clinical_facts="""
            Fakty do stopniowego ujawniania:
            - powtarzające się nagłe epizody intensywnego lęku,
            - kołatanie serca, drżenie, pocenie, duszność, ucisk w klatce,
            - strach przed śmiercią lub utratą kontroli,
            - objawy osiągają szczyt w ciągu kilku minut,
            - po napadach stale martwi się kolejnym napadem,
            - unika metra, galerii handlowych i intensywnego wysiłku,
            - był u lekarza, podstawowe badania według relacji nie wykazały poważnej choroby,
            - kawa i stres nasilają problem.
            Brak objawów psychotycznych.
            Brak epizodów maniakalnych.
            Brak regularnego używania narkotyków.
            """,
        differential="""
            Do różnicowania:
            - choroby serca,
            - nadczynność tarczycy,
            - działania kofeiny lub stymulantów,
            - zaburzenie lękowe uogólnione,
            - agorafobia,
            - PTSD,
            - fobia społeczna.
            """,
        safety_notes="""
            Należy dopytać o:
            - myśli samobójcze,
            - używanie substancji,
            - objawy somatyczne wymagające konsultacji lekarskiej,
            - zakres unikania,
            - wpływ na funkcjonowanie.
            """,
        required_topics=[
            "opis napadów",
            "czas narastania i szczyt objawów",
            "objawy somatyczne",
            "lęk przed śmiercią lub utratą kontroli",
            "lęk antycypacyjny",
            "unikanie",
            "badania somatyczne",
            "kofeina i substancje",
            "funkcjonowanie",
            "ryzyko samobójcze"
        ],
        red_flags=[
            "objawy somatyczne wymagające różnicowania medycznego",
            "postępujące unikanie"
        ]
    ),

    # ocd_01: Natrętne myśli i rytuały — przypadek treningowy ICD-11 6B20
    Case(
        id="icd11_6b20_ocd_01",
        title="Natrętne myśli i rytuały",
        icd11_code="6B20",
        icd10_code="F42",
        icd_mapping_note="Przybliżony odpowiednik edukacyjny. Szczegółowy kod ICD-10 może zależeć od dominacji myśli natrętnych, czynności natrętnych lub obrazu mieszanego.",
        icd_mapping_note="Przybliżony odpowiednik edukacyjny. Szczegółowy kod ICD-10 może zależeć od dominacji myśli natrętnych, czynności natrętnych lub obrazu mieszanego.",
        hidden_diagnosis="Zaburzenie obsesyjno-kompulsyjne według logiki ICD-11 — przypadek treningowy",
        category="zaburzenia obsesyjno-kompulsyjne i pokrewne",
        difficulty="średni",
        patient_profile="""
            Imię: Piotr
            Wiek: 40 lat
            Miejsce: Polska, mniejsze miasto
            Sytuacja: nauczyciel, żonaty, jedno dziecko.
            Styl rozmowy: zawstydzony, ostrożny, boi się oceny.
            Na początku mówi ogólnie o napięciu i spóźnianiu się, nie ujawnia od razu rytuałów.
            """,
        presenting_problem="""
            Pacjent mówi, że codzienne czynności zajmują mu coraz więcej czasu.
            Wstydzi się szczegółów, więc potrzebuje spokojnych, nieoceniających pytań.
            """,
        clinical_facts="""
            Fakty do stopniowego ujawniania:
            - natrętne, niechciane myśli o zabrudzeniu i zakażeniu,
            - wielokrotne mycie rąk,
            - sprawdzanie kuchenki, zamków i okien,
            - czynności zajmują 2–3 godziny dziennie,
            - pacjent uważa je za przesadne, ale czuje silny przymus,
            - unika dotykania poręczy, klamek i publicznych toalet,
            - spóźnia się do pracy,
            - konflikty w domu,
            - wgląd częściowo zachowany.
            Brak urojeń.
            Brak objawów manii.
            Brak substancji jako głównego wyjaśnienia.
            """,
        differential="""
            Do różnicowania:
            - zaburzenia psychotyczne,
            - osobowość anankastyczna,
            - zaburzenia lękowe,
            - zaburzenia tikowe,
            - zaburzenia ze spektrum autyzmu,
            - realne zagrożenia zdrowotne.
            """,
        safety_notes="""
            Należy dopytać o:
            - poziom wglądu,
            - czas zajmowany przez rytuały,
            - nasilenie unikania,
            - depresję wtórną,
            - myśli samobójcze,
            - wpływ na rodzinę i pracę.
            """,
        required_topics=[
            "obsesje",
            "kompulsje",
            "czas zajmowany przez objawy",
            "wgląd",
            "opór wobec rytuałów",
            "unikanie",
            "wpływ na funkcjonowanie",
            "różnicowanie z psychozą",
            "depresja wtórna",
            "ryzyko samobójcze"
        ],
        red_flags=[
            "znaczna utrata czasu",
            "pogorszenie funkcjonowania",
            "możliwa depresja wtórna"
        ]
    ),

    # bipolar_type_ii_01: Okresy dużej energii i późniejsze załamania — przypadek treningowy ICD-11 6A60/6A61
    Case(
        id="icd11_6a60_bipolar_type_ii_01",
        title="Okresy dużej energii i późniejsze załamania",
        icd11_code="6A61",
        icd11_name="Bipolar type II disorder",
        icd10_code="F31",
        icd10_name="Zaburzenie afektywne dwubiegunowe",
        icd_mapping_note="Przybliżony odpowiednik edukacyjny. W ICD-10 szczegółowe kodowanie F31 zależy od aktualnego epizodu i jego nasilenia.",
        hidden_diagnosis="Zaburzenie afektywne dwubiegunowe typu II — przypadek treningowy według logiki ICD-11",
        category="zaburzenia nastroju",
        difficulty="średni/trudny",
        patient_profile="""
            Imię: Natalia
            Wiek: 31 lat
            Miejsce: Warszawa
            Sytuacja: pracuje kreatywnie, zgłasza się z powodu „huśtawek nastroju”.
            Styl rozmowy: inteligentna, szybka, trochę bagatelizuje okresy wzmożonej energii.
            Okresy pobudzenia uważa raczej za produktywne, nie za objaw.
            """,
        presenting_problem="""
            Pacjentka mówi, że ma okresy spadku nastroju, ale też momenty, gdy działa „na najwyższych obrotach”.
            Nie uważa tych lepszych okresów za problem, chyba że psycholog dopyta o konsekwencje.
            """,
        clinical_facts="""
            Fakty do stopniowego ujawniania:
            - okresy depresyjne: spadek energii, anhedonia, poczucie winy, problemy ze snem,
            - okresy po 4–6 dni ze znacznie zwiększoną energią,
            - mniejsza potrzeba snu: 3–4 godziny i nadal dużo energii,
            - większa gadatliwość,
            - gonitwa pomysłów,
            - wzrost pewności siebie,
            - impulsywne zakupy,
            - większa aktywność społeczna i zawodowa,
            - inni zauważali, że jest „nakręcona”,
            - brak hospitalizacji,
            - brak objawów psychotycznych,
            - brak pełnego epizodu maniakalnego.
            """,
        differential="""
            Do różnicowania:
            - zaburzenie depresyjne nawracające,
            - ADHD,
            - cyklotymia,
            - zaburzenia osobowości,
            - używanie substancji,
            - reakcje na stres.
            """,
        safety_notes="""
            Należy dopytać o:
            - samobójczość w depresji,
            - ryzykowne zachowania w okresach pobudzenia,
            - substancje,
            - historię rodzinną chorób afektywnych,
            - hospitalizacje,
            - objawy psychotyczne,
            - konsekwencje zawodowe i interpersonalne.
            """,
        required_topics=[
            "epizody depresyjne",
            "okresy zwiększonej energii",
            "zmniejszona potrzeba snu",
            "gadatliwość",
            "gonitwa myśli",
            "impulsywność",
            "ryzykowne zachowania",
            "objawy psychotyczne",
            "hospitalizacje",
            "substancje",
            "historia rodzinna",
            "ryzyko samobójcze"
        ],
        red_flags=[
            "możliwe ryzykowne zachowania",
            "ryzyko błędnego rozpoznania samej depresji",
            "konieczność oceny samobójczości w fazach depresyjnych"
        ]
    ),
]


# ============================================================
# WYBÓR TRYBU I LIMITU PYTAŃ
# ============================================================

def choose_question_limit() -> int:
    """Pozwala użytkownikowi wybrać limit pytań psychologa.

    Returns:
        int: Wybrany limit pytań.
    """
    print("\nWybierz limit pytań psychologa:")
    for idx, limit in enumerate(AVAILABLE_QUESTION_LIMITS, start=1):
        print(f"{idx}. {limit} pytań")

    while True:
        raw = input("> ").strip()

        if raw.isdigit():
            number = int(raw)

            if number in AVAILABLE_QUESTION_LIMITS:
                return number

            if 1 <= number <= len(AVAILABLE_QUESTION_LIMITS):
                return AVAILABLE_QUESTION_LIMITS[number - 1]

        print("Wybierz 12, 24 albo 48 — lub wpisz numer opcji 1, 2 albo 3.")

def choose_difficulty_mode() -> str:
    """Pozwala użytkownikowi wybrać tryb trudności rozmowy.

    Returns:
        str: Wybrany tryb trudności ('student', 'standard', 'egzamin').
    """
    print("\nWybierz tryb trudności rozmowy:")
    print("1. student  — pacjent ujawnia trochę więcej")
    print("2. standard — pacjent ujawnia informacje dopiero po dobrych pytaniach")
    print("3. egzamin  — pacjent nie pomaga, odpowiada realistycznie i oszczędnie")

    options = ["student", "standard", "egzamin"]

    while True:
        raw = input("> ").strip().lower()

        if raw in options:
            return raw

        if raw.isdigit():
            number = int(raw)
            if 1 <= number <= len(options):
                return options[number - 1]

        print("Wybierz 1, 2, 3 albo wpisz: student, standard, egzamin.")

def choose_case() -> Case:
    """Pozwala użytkownikowi wybrać przypadek lub losuje przypadek.

    Returns:
        Case: Wybrany przypadek.
    """
    print("\nWybierz tryb:")
    print("1. Sam wybieram przypadek")
    print("2. Bot losuje przypadek")

    choice = input("> ").strip()

    adult_cases = [case for case in CASES if case.adult_only]

    if choice == "1":
        print("\nDostępne przypadki dorosłych:")
        for idx, case in enumerate(adult_cases, start=1):
            print(
                f"{idx}. {case.title} "
                f"[ICD-11: {case.icd11_code}; ICD-10: {case.icd10_code}; "
                f"{case.category}; poziom przypadku: {case.difficulty}]"
            )

        while True:
            raw = input("Numer przypadku: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(adult_cases):
                return adult_cases[int(raw) - 1]
            print("Podaj poprawny numer.")
    else:
        return random.choice(adult_cases)


# ============================================================
# PROMPTY
# ============================================================

def build_patient_prompt(case: Case, question_limit: int, difficulty_mode: str) -> str:
    difficulty_config = DIFFICULTY_MODES[difficulty_mode]

    return f"""
        Jesteś symulowanym pacjentem w edukacyjnym ćwiczeniu wywiadu klinicznego.

        KONTEKST APLIKACJI:
        {APP_CONTEXT}

        TRYB ĆWICZENIA:
        - Limit pytań psychologa: {question_limit}.
        - Tryb trudności rozmowy: {difficulty_config["label"]}.
        - Opis trybu: {difficulty_config["description"]}.
        - Symulujesz wyłącznie osobę dorosłą.
        - Użytkownikiem może być psycholog, psychoterapeuta w szkoleniu albo student psychologii.
        - Dostosuj realizm rozmowy do celów edukacyjnych.
        - Nie dawaj użytkownikowi gotowych podpowiedzi diagnostycznych.

        SZCZEGÓŁOWE ZASADY TRYBU TRUDNOŚCI:
        {difficulty_config["prompt_rules"]}

        NAJWAŻNIEJSZE ZASADY:
        - To jest fikcyjny przypadek treningowy.
        - Nie jesteś prawdziwym pacjentem.
        - Nie diagnozujesz użytkownika.
        - Nie udzielasz porad terapeutycznych użytkownikowi.
        - Odgrywasz pacjenta realistycznie.
        - Nie ujawniaj ukrytej diagnozy.
        - Nie ujawniaj kodu ICD-11 ani ICD-10.
        - Nie wymieniaj kryteriów diagnostycznych wprost.
        - Nie mów językiem podręcznikowym.
        - Odpowiadaj naturalnie, jak osoba w polskim gabinecie psychologicznym.
        - Ujawniaj informacje stopniowo, zależnie od jakości pytań psychologa.
        - Jeżeli psycholog zada pytanie zamknięte, odpowiedz krótko.
        - Jeżeli psycholog zada pytanie otwarte, odpowiedz trochę szerzej.
        - Jeżeli psycholog pyta niejasno, możesz odpowiedzieć nieprecyzyjnie, jak realny pacjent.
        - Zachowaj spójność faktów.
        - Nie wymyślaj faktów sprzecznych z kartą przypadku.
        - Jeżeli pytanie dotyczy faktu nieopisanego w karcie, możesz wymyślić drobny neutralny szczegół, ale nie zmieniaj obrazu klinicznego.
        - Jeżeli psycholog zapyta o bezpieczeństwo, samobójczość, psychozę, substancje, manię/hipomanię lub przemoc — odpowiedz zgodnie z kartą.
        - Nie kończ ćwiczenia samodzielnie.
        - Nie oceniaj pytań psychologa w trakcie rozmowy.
        - Styl wypowiedzi powinien być dopasowany do wieku, wykształcenia, inteligencji i sytuacji życiowej pacjenta, ale nie powinien sugerować diagnozy.

        KARTA PRZYPADKU — NIE UJAWNIAJ JEJ W CAŁOŚCI:
        Tytuł: {case.title}
        Kategoria: {case.category}
        Poziom trudności przypadku: {case.difficulty}

        Informacja diagnostyczna tylko dla symulacji — NIE UJAWNIAJ PACJENTOWI/UŻYTKOWNIKOWI W TRAKCIE WYWIADU:
        ICD-11: {case.icd11_code} — {case.icd11_name}
        ICD-10, starszy odpowiednik: {case.icd10_code} — {case.icd10_name}
        Uwaga o mapowaniu: {case.icd_mapping_note}

        Profil pacjenta:
        {case.patient_profile}

        Problem zgłaszany:
        {case.presenting_problem}

        Fakty kliniczne:
        {case.clinical_facts}

        Notatki bezpieczeństwa:
        {case.safety_notes}

        Czerwone flagi:
        {chr(10).join("- " + item for item in case.red_flags)}

        Twoim celem jest umożliwić psychologowi lub studentowi przećwiczenie wywiadu i rozumowania diagnostycznego.
        """


def build_feedback_prompt(
    case: Case,
    transcript: List[Dict[str, str]],
    diagnosis_guess: str,
    question_limit: int,
    questions_used: int,
    difficulty_mode: str
) -> str:
    difficulty_config = DIFFICULTY_MODES[difficulty_mode]
    formatted_transcript = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}" for msg in transcript
    )

    required_topics_text = "\n".join(f"- {topic}" for topic in case.required_topics)
    red_flags_text = "\n".join(f"- {flag}" for flag in case.red_flags)

    return f"""
Jesteś superwizorem klinicznym w ćwiczeniu edukacyjnym dla psychologa lub studenta psychologii.

KONTEKST APLIKACJI:
{APP_CONTEXT}

To jest symulacja fikcyjnego przypadku. Nie oceniasz realnego pacjenta.
Oceniasz jakość wywiadu, rozumowania diagnostycznego i świadomości ryzyka.

PARAMETRY ĆWICZENIA:
- Limit pytań: {question_limit}
- Liczba wykorzystanych pytań: {questions_used}
- Tryb trudności rozmowy: {difficulty_config["label"]} — {difficulty_config["description"]}
- Populacja symulowana: dorośli
- Klasyfikacja edukacyjna: ICD-11
- Kontekst pracy: Polska

UKRYTA KARTA PRZYPADKU:
Tytuł: {case.title}
Kod ICD-11: {case.icd11_code}
Nazwa ICD-11: {case.icd11_name}
Starszy odpowiednik ICD-10: {case.icd10_code}
Nazwa ICD-10: {case.icd10_name}
Uwaga o mapowaniu ICD-11 ↔ ICD-10: {case.icd_mapping_note}
Ukryta diagnoza treningowa: {case.hidden_diagnosis}
Kategoria: {case.category}
Poziom trudności: {case.difficulty}

Profil:
{case.patient_profile}

Problem zgłaszany:
{case.presenting_problem}

Fakty kliniczne:
{case.clinical_facts}

Diagnostyka różnicowa:
{case.differential}

Bezpieczeństwo:
{case.safety_notes}

Wymagane obszary wywiadu:
{required_topics_text}

Czerwone flagi:
{red_flags_text}

TRANSKRYPT ROZMOWY:
{formatted_transcript}

FORMUŁOWANIE / HIPOTEZA UŻYTKOWNIKA:
{diagnosis_guess}

Udziel feedbacku po polsku w tym formacie:

1. Trafność hipotezy
- Oceń, czy hipoteza była trafna, częściowo trafna czy nietrafna.
- Odnieś się do ICD-11 oraz pokaż starszy przybliżony odpowiednik ICD-10.
- Nie udawaj, że to pełna formalna diagnoza realnej osoby.
- Jeżeli mapowanie ICD-11 ↔ ICD-10 nie jest idealne, zaznacz to.

2. Najważniejsze dane kliniczne
- Wypisz objawy i informacje, które najbardziej wspierały rozpoznanie.

3. Pokrycie checklisty wywiadu
- Wskaż, które wymagane obszary użytkownik zbadał.
- Wskaż, które ważne obszary pominął.

4. Diagnostyka różnicowa
- Podaj najważniejsze alternatywne wyjaśnienia.
- Napisz, jakie pytania pomogłyby je odróżnić.

5. Ocena ryzyka i bezpieczeństwa
- Oceń, czy użytkownik wystarczająco zbadał czerwone flagi.
- Uwzględnij samobójczość, samouszkodzenia, psychozę, substancje, manię/hipomanię lub inne ryzyka właściwe dla przypadku.
- Jeżeli pominął kluczowe ryzyko, zaznacz to wyraźnie.

6. Jakość rozmowy
- Oceń pytania otwarte, empatię, strukturę, tempo i adekwatność dopytywania.
- Uwzględnij, że użytkownikiem może być student.

7. Lepsze pytania na przyszłość
- Podaj 5 konkretnych pytań, które użytkownik mógłby zadać.

8. Ocena końcowa
- Daj ocenę 0–10.
- Osobno oceń:
  a) rozpoznanie,
  b) wywiad,
  c) ocenę ryzyka,
  d) diagnostykę różnicową.
- Dodaj krótkie uzasadnienie.

Nie podawaj zaleceń leczenia dla realnego pacjenta.
Nie twórz pewnej diagnozy klinicznej realnej osoby.
"""


# ============================================================
# MODEL
# ============================================================

def ask_model(input_messages):
    response = client.responses.create(
        model="gpt-5.5",
        input=input_messages
    )
    return response.output_text


# ============================================================
# WYWIAD
# ============================================================

def collect_case_formulation() -> str:
    print("\nPodaj swoje sformułowanie przypadku.")
    print("Możesz pisać krótko, ale im pełniejsza odpowiedź, tym lepszy feedback.\n")

    main_hypothesis = input("1. Główna hipoteza diagnostyczna: ").strip()
    differentials = input("2. Diagnozy różnicowe: ").strip()
    supporting_data = input("3. Dane wspierające hipotezę: ").strip()
    missing_data = input("4. Czego jeszcze trzeba dopytać: ").strip()
    risk = input("5. Ocena ryzyka / czerwone flagi: ").strip()

    return f"""
Główna hipoteza diagnostyczna:
{main_hypothesis}

Diagnozy różnicowe:
{differentials}

Dane wspierające:
{supporting_data}

Braki w danych:
{missing_data}

Ocena ryzyka / czerwone flagi:
{risk}
"""


def run_interview(case: Case, question_limit: int, difficulty_mode: str):
    patient_system_prompt = build_patient_prompt(case, question_limit, difficulty_mode)

    messages = [
        {"role": "system", "content": patient_system_prompt}
    ]

    transcript = []
    questions_used = 0

    print("\n" + "=" * 72)
    print("ĆWICZENIE ROZPOCZĘTE")
    print("=" * 72)
    print("Rozmawiasz z fikcyjnym dorosłym pacjentem.")
    print(f"Limit pytań psychologa: {question_limit}")
    print(f"Tryb trudności rozmowy: {difficulty_mode}")
    print("Klasyfikacja edukacyjna: ICD-11")
    print("Kontekst: praca psychologiczna w Polsce")
    print("Wpisz /diagnoza, kiedy chcesz zakończyć rozmowę i podać hipotezę.")
    print("Wpisz /status, żeby zobaczyć liczbę wykorzystanych pytań.")
    print("Wpisz /exit, żeby zakończyć program.")
    print("=" * 72 + "\n")

    opening = ask_model(messages + [
        {
            "role": "user",
            "content": "Rozpocznij rozmowę jako pacjent jednym naturalnym zdaniem. Nie ujawniaj diagnozy ani kodu ICD-11/ICD-10."
        }
    ])

    print(f"Pacjent: {opening}\n")
    transcript.append({"role": "patient", "content": opening})
    messages.append({"role": "assistant", "content": opening})

    while True:
        user_text = input(f"Psycholog [{questions_used}/{question_limit}]: ").strip()

        if not user_text:
            continue

        command = user_text.lower()

        if command == "/exit":
            print("Zakończono ćwiczenie.")
            return

        if command == "/status":
            remaining = question_limit - questions_used
            print(f"\nWykorzystano pytań: {questions_used}. Pozostało: {remaining}.\n")
            continue

        if command == "/diagnoza":
            break

        if questions_used >= question_limit:
            print("\nLimit pytań został już wykorzystany. Przejdź do sformułowania przypadku.")
            break

        questions_used += 1

        transcript.append({"role": "psychologist", "content": user_text})
        messages.append({"role": "user", "content": user_text})

        patient_answer = ask_model(messages)
        print(f"\nPacjent: {patient_answer}\n")

        transcript.append({"role": "patient", "content": patient_answer})
        messages.append({"role": "assistant", "content": patient_answer})

        if questions_used >= question_limit:
            print("=" * 72)
            print(f"Osiągnięto limit {question_limit} pytań.")
            print("Przejdź teraz do sformułowania przypadku.")
            print("=" * 72)
            break

    diagnosis_guess = collect_case_formulation()

    print("\n" + "=" * 72)
    print("FEEDBACK SUPERVISORA")
    print("=" * 72 + "\n")

    feedback_prompt = build_feedback_prompt(
        case=case,
        transcript=transcript,
        diagnosis_guess=diagnosis_guess,
        question_limit=question_limit,
        questions_used=questions_used,
        difficulty_mode=difficulty_mode
    )

    feedback = ask_model([
        {"role": "system", "content": feedback_prompt},
        {"role": "user", "content": "Wygeneruj feedback superwizyjny."}
    ])

    print(feedback)


# ============================================================
# MAIN
# ============================================================

def main():
    print("""
    SYMULATOR WYWIADU KLINICZNEGO — WERSJA EDUKACYJNA

    Ten program generuje fikcyjne przypadki do ćwiczenia rozmowy klinicznej.
    Nie służy do diagnozowania realnych pacjentów.
    Nie zastępuje superwizji, dokumentacji ICD-11, konsultacji psychiatrycznej
    ani procedur kryzysowych obowiązujących w Polsce.

    Aktualna populacja przypadków:
    - wyłącznie dorośli

    Planowana rozbudowa:
    - więcej przypadków dorosłych
    - osobny moduł dzieci i młodzieży
    - większa baza przypadków według ICD-11
    """)

    question_limit = choose_question_limit()
    difficulty_mode = choose_difficulty_mode()
    case = choose_case()

    run_interview(case, question_limit, difficulty_mode)


if __name__ == "__main__":
    main()
