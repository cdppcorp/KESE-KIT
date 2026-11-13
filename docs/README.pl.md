🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Wtyczka Claude Code do analizy i oceny podatnosci Krytycznej Infrastruktury Informacyjnej (CII), oceny bezpieczenstwa AI, bezpieczenstwa robotow, bezpieczenstwa kosmicznego, bezpiecznego kodowania, oceny Zero Trust oraz Bezpieczenstwa lancucha dostaw SW (SBOM) zgodnie z wytycznymi KISA (Koreanska Agencja Internetu i Bezpieczenstwa).

---

## Przegląd

KESE (KISA Enhanced Security Evaluation Kit) to wtyczka Claude Code zapewniająca kompleksowe możliwości oceny podatności bezpieczeństwa w oparciu o wytyczne KISA (Koreańska Agencja Internetu i Bezpieczeństwa). Obsługuje ocenę Krytycznej Infrastruktury Informacyjnej (CII), Bezpieczeństwa AI, Bezpieczeństwa Robotów, Bezpieczeństwa Kosmicznego, Bezpiecznego Kodowania oraz ocenę Zero Trust.

## Funkcje

| Umiejętność | Opis |
|-------------|------|
| `/kesekit-start` | Uruchomienie pełnej oceny podatności bezpieczeństwa (CII 560+ / AI / Roboty / Kosmos / Bezpieczne kodowanie / Zero Trust / Łańcuch dostaw SW) |
| `/kesekit-check` | Lista kontrolna zgodności bezpieczeństwa przed wdrożeniem (CII / AI / Roboty / Kosmos / Bezpieczne kodowanie / Zero Trust / Łańcuch dostaw SW) |
| `/kesekit-fix` | Automatyczne generowanie skryptów utwardzających i poprawek bezpieczeństwa (CII / AI / Roboty / Kosmos / Bezpieczne kodowanie / Zero Trust / Łańcuch dostaw SW) |
| `/kesekit-guide` | Generowanie promptów bezpiecznego kodowania dla narzędzi AI (CII / AI / Roboty / Kosmos / JS·Python·Ogólny / Zero Trust / Łańcuch dostaw SW) |

## Obsługiwane wytyczne

### 1. Krytyczna Infrastruktura Informacyjna (CII) — 560+ pozycji

**Ocena techniczna**
| System | Kod | Liczba pozycji |
|--------|-----|:-------------:|
| Serwer Unix/Linux | U-01~U-67 | 67 |
| Serwer Windows | W-01~W-64 | 64 |
| Usługi webowe | WEB-01~WEB-26 | 26 |
| Urządzenia bezpieczeństwa | S-01~S-23 | 23 |
| Urządzenia sieciowe | N-01~N-38 | 38 |
| Systemy sterowania | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Urządzenia mobilne | M-01~M-04 | 4 |
| Web Application | 21 kodów | 21 |
| Wirtualizacja | HV-01~HV-25 | 25 |
| Chmura | CA-01~CA-19 | 19 |

**Ocena administracyjna**: A-1~A-127 (127 pozycji, 14 domen)
**Ocena fizyczna**: P-1~P-18 (18 pozycji)

### 2. Przewodnik bezpieczeństwa AI — 54+ pozycji

| Grupa docelowa | Liczba pozycji | Cykl życia |
|----------------|:-------------:|------------|
| Programiści AI | 54 | 6 etapów (Planowanie→Dane→Rozwój modelu→Wdrożenie→Monitoring→Wycofanie) |
| Dostawcy usług AI | ~43 | 6 etapów (Planowanie→Rozwój→Eksploatacja→Utrzymanie→Informacja zwrotna→Wycofanie) |
| Użytkownicy AI | 7 | Najlepsze praktyki bezpieczeństwa |

### 3. Bezpieczeństwo robotów — ~103 pozycji

| Kategoria | Kod | Liczba pozycji | Standard referencyjny |
|-----------|-----|:-------------:|----------------------|
| Bezpieczne tworzenie oprogramowania (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Bezpieczeństwo łańcucha dostaw | SC-01~07 | 7 | NIST SP 800-161 |
| Identyfikacja i uwierzytelnianie | IA-01~11 | 11 | IEC 62443 |
| Kontrola użytkowania | UC-01~11 | 11 | IEC 62443 |
| Integralność systemu | SI-01~11 | 11 | IEC 62443 |
| Ochrona danych | DP-01~04 | 4 | IEC 62443 |
| Ograniczenie przepływu danych | DFR-01~02 | 2 | IEC 62443 |
| Reagowanie na zdarzenia | ER-01~03 | 3 | IEC 62443 |
| Dostępność zasobów | RA-01~08 | 8 | IEC 62443 |
| Odporność cybernetyczna | CR-01~13 | 13 | EU CRA |
| Bezpieczeństwo bezprzewodowe | WS-01~14 | 14 | EU RED |

Cel: Roboty przemysłowe / Roboty usługowe / Roboty medyczne (ISO 8373)

### 4. Bezpieczeństwo kosmiczne — 53 pozycji

| Dziedzina | Kod | Liczba pozycji | Standard referencyjny |
|-----------|-----|:-------------:|----------------------|
| Kontrola dostępu | AC-01~12 | 12 | CMMC, K-RMF |
| Identyfikacja i uwierzytelnianie | IA-01~02 | 2 | CMMC, NIS2 |
| Bezpieczeństwo systemu i komunikacji | SC-01~07 | 7 | NIST IR 8401 |
| Integralność systemu i informacji | SI-01~04 | 4 | NIST CSF |
| Zarządzanie operacjami systemu/usług | SO-01~09 | 9 | ISMS-P |
| Reagowanie na incydenty | IR-01~02 | 2 | NIS2 |
| Bezpieczeństwo personelu | PS-01~02 | 2 | CMMC |
| Bezpieczeństwo fizyczne | PE-01~03 | 3 | K-RMF |
| Ocena ryzyka i bezpieczeństwa | RA-01~02 | 2 | NIST CSF |
| Zarządzanie bezpieczeństwem | SG-01~04 | 4 | ISMS-P |
| Plan awaryjny | CP-01~02 | 2 | NIST IR 8270 |
| Zarządzanie łańcuchem dostaw | SM-01~04 | 4 | CMMC, NIS2 |

Cel: Operatorzy satelitów, Dostawcy GSaaS, Operatorzy stacji naziemnych, Firmy w łańcuchu dostaw kosmicznego

### 5. Przewodnik bezpiecznego kodowania — 46 pozycji

| Kategoria | Liczba pozycji | Liczba CWE | Standard referencyjny |
|-----------|:-------------:|:--------:|----------------------|
| Walidacja i reprezentacja danych wejściowych | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| Funkcje bezpieczeństwa | 16 | 16 | CWE/SANS Top 25 |
| Czas i stan | 2 | 3 | CWE |
| Obsługa błędów | 3 | 3 | CWE |
| Błędy kodu | 3 | 3 | CWE |
| Enkapsulacja | 4 | 5 | CWE |
| Nadużycie API | 2 | 1 | CWE |

**Obsługiwane języki:**
| Język | Liczba pozycji | Framework |
|-------|:-------------:|-----------|
| Pseudo Code (Ogólny) | 46 | Wzorce niezależne od języka |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

Cel: Programiści webowi JavaScript/Python, Użytkownicy narzędzi AI (Claude, Cursor, Copilot), Programiści Vibe Coding

### 6. Bezpieczeństwo Zero Trust — ~421 pozycji

| Element podstawowy | Kod | Liczba pozycji | Dojrzałość |
|-------------------|-----|:-------------:|-----------|
| Tożsamość | ZT-ID-01~53 | 53 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |
| Urządzenia i punkty końcowe | ZT-DV-01~36 | 36 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |
| Sieć | ZT-NW-01~54 | 54 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |
| System | ZT-SY-01~49 | 49 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |
| Aplikacja i obciążenie robocze | ZT-AP-01~60 | 60 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |
| Dane | ZT-DA-01~58 | 58 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |
| Widoczność i analityka | ZT-VA-01~43 | 43 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |
| Automatyzacja i orkiestracja | ZT-AU-01~43 | 43 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |
| Specyficzny dla OT/ICS | ZT-OT-01~25 | 25 | Tradycyjny/Początkowy/Zaawansowany/Optymalny |

**4 poziomy dojrzałości**: Tradycyjny (Traditional) → Początkowy (Initial) → Zaawansowany (Advanced) → Optymalny (Optimal)
**Standardy referencyjne**: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

Cel: Organizacje wdrażające Zero Trust, Środowiska OT/ICS, Organizacje migrujące do chmury, Osoby odpowiedzialne za ocenę dojrzałości bezpieczeństwa

### 7. Bezpieczeństwo łańcucha dostaw SW (SBOM) — 29 pozycji

| Faza | Kod | Liczba pozycji | Standard |
|------|-----|:-------------:|----------|
| Projektowanie | SC-01~05 | 5 | NIST SP 800-161r1 |
| Rozwój | SC-06~16 | 11 | NIST SP 800-218 |
| Dostawa/Dystrybucja | SC-17~19 | 3 | NTIA SBOM |
| Wdrożenie i eksploatacja | SC-20~26 | 7 | NIS-SBOM |
| Utrzymanie | SC-27~29 | 3 | NIS-SBOM |

## Instalacja

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

## Użycie

```bash
# Rozpoczęcie pełnej oceny bezpieczeństwa
/kesekit-start

# Uruchomienie listy kontrolnej przed wdrożeniem
/kesekit-check

# Generowanie skryptów utwardzających
/kesekit-fix

# Uzyskanie promptów bezpiecznego kodowania
/kesekit-guide
```

---

## Struktura projektu

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Metadane wtyczki
├── skills/                            ← Umiejętności angielskie
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 linii)
│   │   ├── references/               ← Dokumenty opisowe/kryteria
│   │   │   ├── ai-security/          ← Przegląd, dostawcy usług, przewodnik użytkownika
│   │   │   └── space-security/       ← Przegląd, scenariusze zagrożeń łańcucha dostaw
│   │   ├── templates/                ← Formularze, tabele list kontrolnych
│   │   │   ├── cii/                  ← 14 tabel kontrolnych CII
│   │   │   ├── ai-security/          ← Listy kontrolne programistów AI, użytkowników
│   │   │   ├── robot-security/       ← 6 list kontrolnych bezpieczeństwa robotów
│   │   │   ├── space-security/       ← 4 tabele kontrolne kosmiczne
│   │   │   └── zero-trust/           ← Tabele list kontrolnych Zero Trust
│   │   └── scripts/                  ← Skrypty kontrolne/naprawcze
│   │       ├── cii/                  ← bash, PowerShell, SQL
│   │       └── robot-security/       ← Firewall, SBOM, certyfikaty
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Umiejętności koreańskie (ta sama struktura)
├── 문서/                              ← Oryginalne pliki PDF
├── authorkit/                         ← Dokumenty źródłowe i wyniki prac
├── docs/                              ← README w 20 językach
└── README.md
```

---

## Historia zmian

### v4.0.0 (2026-04-03)

**Nowe wytyczne: Bezpieczeństwo Zero Trust — ~421 pozycji**
- Źródło: KISA Zero Trust Guideline 2.0 (245 str.) + Przewodnik modelu dojrzałości (182 str.) + Przewodnik wdrożenia OT (67 str.)
- 9 elementów podstawowych, ~421 pozycji list kontrolnych, 4 poziomy dojrzałości
- Standardy: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

### v3.2.0 (2026-04-02)

**Nowe wytyczne: Bezpieczne kodowanie**
- Źródło: KISA Javascript Secure Coding Guide 159 str. + Python Secure Coding Guide 176 str. (rewizja 2023)
- 7 kategorii, 46 pozycji, 49 CWE
- JavaScript / Python / Pseudo Code (ogólny)

### v3.0.0 (2026-04-02)

**Breaking Change: Zmiana formatu poleceń**
- Wszystkie umiejętności połączone w jedną przestrzeń nazw `kesekit`
- Format poleceń: `/start` → `/kesekit-start`

**Nowe wytyczne: Bezpieczeństwo kosmiczne**
- Źródło: Space Security Model Part1 134 str. + Part2 223 str. + Przewodnik objaśniający 218 str.
- 12 dziedzin, 53 pozycji list kontrolnych

### v2.0.0 (2026-03-30)

**Refaktoryzacja struktury — zastosowanie wzorca Progressive Disclosure**

| Zmiana | Przed (v1.0) | Po (v2.0) |
|--------|-------------|-----------|
| SKILL.md | Cała wiedza inline (270~465 linii) | Tylko router (~50~80 linii) |
| Wytyczne | Obsługa wyłącznie CII | Obsługa CII + Bezpieczeństwo AI |
| Przechowywanie wiedzy | Zakodowane na stałe w SKILL.md | Wydzielone do `references/` (18 plików) |
| Kody pozycji | Tylko część pozycji | Wszystkie pozycje na podstawie przewodnika 2026 |
| Skalowalność | Nowe wytyczne = więcej umiejętności | 4 umiejętności na stałe, dodawanie tylko references |

**Nowe wytyczne: Przewodnik bezpieczeństwa AI**
- Źródło: Ministerstwo Nauki i ICT / KISA 「Przewodnik bezpieczeństwa sztucznej inteligencji (AI)」
- 54 pozycje weryfikacyjne dla programistów AI (cykl życia 6 etapów)
- Wymagania bezpieczeństwa dla dostawców usług AI
- 7 zasad bezpieczeństwa dla użytkowników AI

**Aktualizacja wytycznych CII**
- Ponowna ekstrakcja wszystkich pozycji na podstawie szczegółowego przewodnika 2026
- Uwzględnienie systemu kodów pozycji (nowe kody: WEB, HV, CA)

### v1.0.0 (2026-03-29)

- Pierwsze wydanie
- 4 umiejętności oceny podatności CII (koreański/angielski)
- Pozycje techniczne (424) + administracyjne (127) + fizyczne (9)

---

## Podstawy prawne

- **Ustawa o ochronie infrastruktury informacyjnej i komunikacyjnej** (Act on Protection of Information and Communications Infrastructure)
- **Ustawa o e-administracji** (e-Government Act)
- **Ustawa o ochronie danych osobowych** (Personal Information Protection Act)
- **Ustawa o podstawach sztucznej inteligencji** (AI Basic Act, obowiązuje od 22.01.2026)

---

## Powiązane materiały

- [Szczegółowy przewodnik KISA dotyczący analizy i oceny podatności technicznych](https://www.kisa.or.kr)
- [Przewodnik bezpieczeństwa sztucznej inteligencji (AI)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Zbudowano z użyciem

| Wtyczka | Opis |
|---------|------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Umiejętność wspomagania pisania książek - analiza PDF, ekstrakcja struktury, korekta/przepisywanie |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Kompatybilność hooków wtyczek Claude Code dla środowiska Windows |

---

## Licencja

MIT License

## Autor

CDPP Corp (https://github.com/cdppcorp)
