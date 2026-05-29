# icd_dictionary.py
"""
Słownik kodów i nazw ICD-11 oraz ICD-10 z polskimi i angielskimi odpowiednikami.

Każdy wpis zawiera:
- kod ICD,
- nazwę angielską,
- nazwę polską,
- klasyfikację (ICD-11 lub ICD-10).
- kryteria diagnostyczne (rozbudować w przyszłości).
- ewentualnie dodatkowe informacje (np. objawy, leczenie) — rozbudować w przyszłości.
- różnicowanie z innymi zaburzeniami (rozbudować w przyszłości).
"""


# Słownik kodów ICD-11
ICD_11_DICTIONARY = [
    {
        "code": "6A70",
        "name_en": "Single episode depressive disorder / Depressive episode",
        "name_pl": "Epizod depresyjny (pojedynczy epizod)"
    },
    {
        "code": "6B01",
        "name_en": "Panic disorder",
        "name_pl": "Zaburzenie paniczne"
    },
    {
        "code": "6B20",
        "name_en": "Obsessive-compulsive disorder",
        "name_pl": "Zaburzenie obsesyjno-kompulsyjne"
    },
    {
        "code": "6A61",
        "name_en": "Bipolar type II disorder",
        "name_pl": "Zaburzenie afektywne dwubiegunowe typu II"
    },
    {
        "code": "6A20",
        "name_en": "Schizophrenia",
        "name_pl": "Schizofrenia"
    },
    {
        "code": "6B00",
        "name_en": "Generalized anxiety disorder",
        "name_pl": "Zaburzenie lękowe uogólnione"
    },
    {
        "code": "6B40",
        "name_en": "Post-traumatic stress disorder (PTSD)",
        "name_pl": "Zespół stresu pourazowego (PTSD)"
    },
    {
        "code": "6B80",
        "name_en": "Anorexia nervosa",
        "name_pl": "Jadłowstręt psychiczny (anoreksja)"
    },
    {
        "code": "6C40",
        "name_en": "Alcohol dependence",
        "name_pl": "Zależność od alkoholu"
    },
    {
        "code": "6D10",
        "name_en": "Emotionally unstable personality disorder (Borderline type)",
        "name_pl": "Chwiejne emocjonalnie zaburzenie osobowości (typ borderline)"
    },
    {
        "code": "6A05",
        "name_en": "Attention deficit hyperactivity disorder (ADHD)",
        "name_pl": "Zespół nadpobudliwości psychoruchowej z deficytem uwagi (ADHD)"
    },
    {
        "code": "6A02",
        "name_en": "Autism spectrum disorder",
        "name_pl": "Zaburzenie ze spektrum autyzmu"
    },
    {
        "code": "6B43",
        "name_en": "Prolonged grief disorder",
        "name_pl": "Zaburzenie żałoby przedłużonej"
    },
    {
        "code": "7A00",
        "name_en": "Insomnia disorder",
        "name_pl": "Bezsenność przewlekła"
    },
    {
        "code": "8A05",
        "name_en": "Tic disorders",
        "name_pl": "Zaburzenia tikowe"
    },
    {
        "code": "6C23",
        "name_en": "Opioid dependence",
        "name_pl": "Zależność od opioidów"
    },
    {
        "code": "6B23",
        "name_en": "Somatization disorder",
        "name_pl": "Zaburzenie somatyzacyjne"
    },
    {
        "code": "6B04",
        "name_en": "Social anxiety disorder",
        "name_pl": "Fobia społeczna"
    },
    {
        "code": "6A72",
        "name_en": "Persistent depressive disorder (dysthymia)",
        "name_pl": "Dystymia (przewlekłe zaburzenie depresyjne)"
    },
    {
        "code": "6B81",
        "name_en": "Bulimia nervosa",
        "name_pl": "Żarłoczność psychiczna (bulimia)"
    },
    {
        "code": "6B21",
        "name_en": "Obsessive-compulsive disorder, predominantly obsessions",
        "name_pl": "Zaburzenie obsesyjno-kompulsyjne z przewagą myśli natrętnych"
    },
    {
        "code": "6D30",
        "name_en": "Anankastic personality disorder",
        "name_pl": "Osobowość anankastyczna (obsesyjno-kompulsyjna)"
    },
    {
        "code": "6B06",
        "name_en": "Separation anxiety disorder",
        "name_pl": "Zaburzenie lękowe separacyjne"
    },
    {
        "code": "6B05",
        "name_en": "Selective mutism",
        "name_pl": "Mutyzm wybiórczy"
    },
    {
        "code": "6B60",
        "name_en": "Dissociative disorders",
        "name_pl": "Zaburzenia dysocjacyjne"
    },
    {
        "code": "6B61",
        "name_en": "Conversion disorder",
        "name_pl": "Zaburzenie konwersyjne"
    },
    {
        "code": "6A24",
        "name_en": "Delusional disorder",
        "name_pl": "Zaburzenie urojeniowe"
    },
    {
        "code": "6A73",
        "name_en": "Seasonal affective disorder",
        "name_pl": "Sezonowe zaburzenie afektywne"
    },
    {
        "code": "6B03",
        "name_en": "Mixed anxiety and depressive disorder",
        "name_pl": "Zaburzenie lękowo-depresyjne mieszane"
    },
    {
        "code": "6C90",
        "name_en": "Conduct disorder",
        "name_pl": "Zaburzenie zachowania"
    },
    {
        "code": "6C91",
        "name_en": "Oppositional defiant disorder",
        "name_pl": "Zaburzenie opozycyjno-buntownicze"
    },
    {
        "code": "6B44",
        "name_en": "Adjustment disorder with depressed mood",
        "name_pl": "Zaburzenie adaptacyjne z przewagą depresji"
    },
    {
        "code": "6B45",
        "name_en": "Adjustment disorder with anxiety",
        "name_pl": "Zaburzenie adaptacyjne z przewagą lęku"
    },
    {
        "code": "6B46",
        "name_en": "Adjustment disorder with mixed anxiety and depressed mood",
        "name_pl": "Zaburzenie adaptacyjne mieszane (lękowo-depresyjne)"
    },
]

# Słownik kodów ICD-10
ICD_10_DICTIONARY = [

def get_icd11_entry_by_code(code: str) -> Optional[dict]:
    """Zwraca słownik z nazwą angielską i polską dla danego kodu ICD-11.

    Args:
        code: Kod ICD-11 (np. "6A70").

    Returns:
        Słownik z polami 'code', 'name_en', 'name_pl' lub None jeśli nie znaleziono.
    """
    for entry in ICD_11_DICTIONARY:
        if entry["code"] == code:
            return entry
    return None
    {
        "code": "F32",
        "name_en": "Depressive episode",
        "name_pl": "Epizod depresyjny"
    },
    {
        "code": "F41.0",
        "name_en": "Panic disorder (episodic paroxysmal anxiety)",
        "name_pl": "Zaburzenie paniczne / lęk napadowy"
    },
    {
        "code": "F42",
        "name_en": "Obsessive-compulsive disorder",
        "name_pl": "Zaburzenie obsesyjno-kompulsyjne"
    },
    {
        "code": "F31",
        "name_en": "Bipolar affective disorder",
        "name_pl": "Zaburzenie afektywne dwubiegunowe"
    },
    {
        "code": "F20",
        "name_en": "Schizophrenia",
        "name_pl": "Schizofrenia"
    },
    {
        "code": "F41.1",
        "name_en": "Generalized anxiety disorder",
        "name_pl": "Zaburzenie lękowe uogólnione"
    },
    {
        "code": "F43.1",
        "name_en": "Post-traumatic stress disorder (PTSD)",
        "name_pl": "Zespół stresu pourazowego (PTSD)"
    },
    {
        "code": "F50.0",
        "name_en": "Anorexia nervosa",
        "name_pl": "Jadłowstręt psychiczny (anoreksja)"
    },
    {
        "code": "F10.2",
        "name_en": "Alcohol dependence syndrome",
        "name_pl": "Zespół uzależnienia od alkoholu"
    },
    {
        "code": "F60.3",
        "name_en": "Emotionally unstable personality disorder (Borderline type)",
        "name_pl": "Chwiejne emocjonalnie zaburzenie osobowości (typ borderline)"
    },
    {
        "code": "F90.0",
        "name_en": "Attention deficit hyperactivity disorder (ADHD)",
        "name_pl": "Zespół nadpobudliwości psychoruchowej z deficytem uwagi (ADHD)"
    },
    {
        "code": "F84.0",
        "name_en": "Childhood autism",
        "name_pl": "Autyzm dziecięcy"
    },
    {
        "code": "F43.2",
        "name_en": "Adjustment disorders",
        "name_pl": "Zaburzenia adaptacyjne"
    },
    {
        "code": "F51.0",
        "name_en": "Nonorganic insomnia",
        "name_pl": "Bezsenność nieorganiczna"
    },
    {
        "code": "F95.2",
        "name_en": "Chronic motor or vocal tic disorder",
        "name_pl": "Przewlekłe zaburzenie tikowe ruchowe lub głosowe"
    },
    {
        "code": "F11.2",
        "name_en": "Opioid dependence syndrome",
        "name_pl": "Zespół uzależnienia od opioidów"
    },
    {
        "code": "F45.0",
        "name_en": "Somatization disorder",
        "name_pl": "Zaburzenie somatyzacyjne"
    },
    {
        "code": "F40.1",
        "name_en": "Social phobias",
        "name_pl": "Fobia społeczna"
    },
    {
        "code": "F34.1",
        "name_en": "Dysthymia",
        "name_pl": "Dystymia"
    },
    {
        "code": "F50.2",
        "name_en": "Bulimia nervosa",
        "name_pl": "Żarłoczność psychiczna (bulimia)"
    },
    {
        "code": "F42.0",
        "name_en": "Predominantly obsessional thoughts or ruminations",
        "name_pl": "Zaburzenie obsesyjno-kompulsyjne z przewagą myśli natrętnych"
    },
    {
        "code": "F60.5",
        "name_en": "Anankastic personality disorder",
        "name_pl": "Osobowość anankastyczna (obsesyjno-kompulsyjna)"
    },
    {
        "code": "F93.0",
        "name_en": "Separation anxiety disorder of childhood",
        "name_pl": "Zaburzenie lękowe separacyjne u dzieci"
    },
    {
        "code": "F94.0",
        "name_en": "Selective mutism",
        "name_pl": "Mutyzm wybiórczy"
    },
    {
        "code": "F44",
        "name_en": "Dissociative [conversion] disorders",
        "name_pl": "Zaburzenia dysocjacyjne (konwersyjne)"
    },
    {
        "code": "F22",
        "name_en": "Delusional disorder",
        "name_pl": "Zaburzenie urojeniowe"
    },
    {
        "code": "F33.0",
        "name_en": "Recurrent depressive disorder, current episode mild",
        "name_pl": "Nawracające zaburzenie depresyjne, epizod łagodny"
    },
    {
        "code": "F41.2",
        "name_en": "Mixed anxiety and depressive disorder",
        "name_pl": "Zaburzenie lękowo-depresyjne mieszane"
    },
    {
        "code": "F91",
        "name_en": "Conduct disorders",
        "name_pl": "Zaburzenia zachowania"
    },
    {
        "code": "F91.3",
        "name_en": "Oppositional defiant disorder",
        "name_pl": "Zaburzenie opozycyjno-buntownicze"
    },
    {
        "code": "F43.21",
        "name_en": "Adjustment disorder with depressed mood",
        "name_pl": "Zaburzenie adaptacyjne z przewagą depresji"
    },
    {
        "code": "F43.22",
        "name_en": "Adjustment disorder with anxiety",
        "name_pl": "Zaburzenie adaptacyjne z przewagą lęku"
    },
    {
        "code": "F43.23",
        "name_en": "Adjustment disorder with mixed anxiety and depressed mood",
        "name_pl": "Zaburzenie adaptacyjne mieszane (lękowo-depresyjne)"
    },
]
