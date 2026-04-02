🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Wtyczka Claude Code do analizy i oceny podatnosci Krytycznej Infrastruktury Informacyjnej (CII) oraz oceny bezpieczenstwa AI zgodnie z wytycznymi KISA (Koreanska Agencja Internetu i Bezpieczenstwa).

---

## Przegląd

KESE (KISA Enhanced Security Evaluation Kit) to wtyczka Claude Code zapewniająca kompleksowe możliwości oceny podatności bezpieczeństwa w oparciu o wytyczne KISA (Koreańska Agencja Internetu i Bezpieczeństwa). Obsługuje zarówno ocenę Krytycznej Infrastruktury Informacyjnej (CII), jak i ocenę Bezpieczeństwa AI.

## Funkcje

| Umiejętność | Opis |
|-------------|------|
| `/kesekit-start` | Uruchomienie pełnej oceny podatności bezpieczeństwa (CII 560+ pozycji lub AI Security) |
| `/kesekit-check` | Lista kontrolna zgodności bezpieczeństwa przed wdrożeniem |
| `/kesekit-fix` | Automatyczne generowanie skryptów utwardzających i poprawek bezpieczeństwa |
| `/kesekit-guide` | Generowanie promptów bezpiecznego kodowania dla narzędzi AI |

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

## Instalacja

```bash
claude plugins install kesekit
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
├── skills/                            ← Umiejętności angielskie (router)
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 linii)
│   │   └── references/               ← Baza wiedzy według wytycznych
│   │       ├── cii/                  ← 14 referencji CII
│   │       └── ai-security/          ← 4 referencje bezpieczeństwa AI
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Umiejętności koreańskie (ta sama struktura)
├── authorkit/                         ← Dokumenty źródłowe i wyniki prac
│   ├── converted/
│   │   ├── ref-001/                  ← Przewodnik administracyjny i fizyczny (full.md)
│   │   ├── ref-002/                  ← Przewodnik techniczny (full.md)
│   │   └── ref-003/                  ← Przewodnik bezpieczeństwa AI (full.md)
│   └── ...
├── 문서/                              ← Oryginalne pliki PDF
└── README.md
```

---

## Historia zmian

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
