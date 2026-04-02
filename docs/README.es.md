🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin de Claude Code para el analisis y evaluacion de vulnerabilidades en Infraestructuras Criticas de Informacion (CII) y evaluacion de seguridad de IA.

---

## Descripcion general

KESE (KISA Enhanced Security Evaluation Kit) es un plugin de Claude Code que ofrece capacidades integrales de evaluacion de vulnerabilidades basadas en las directrices de KISA (Agencia de Internet y Seguridad de Corea). Soporta tanto la evaluacion de Infraestructuras Criticas de Informacion (CII) como la evaluacion de seguridad de IA.

## Funcionalidades

| Skill | Descripcion |
|-------|-------------|
| `/kesekit-start` | Ejecutar evaluacion completa de vulnerabilidades de seguridad (CII 560+ elementos o seguridad IA) |
| `/kesekit-check` | Lista de verificacion de cumplimiento de seguridad previo al despliegue |
| `/kesekit-fix` | Generacion automatica de scripts de hardening y correcciones de seguridad |
| `/kesekit-guide` | Generar prompts de codificacion segura para herramientas de IA |

## Directrices soportadas

### 1. CII (Infraestructura Critica de Informacion) — 560+ elementos

**Evaluacion tecnica**
| Sistema | Codigo | Elementos |
|---------|--------|:---------:|
| Servidores Unix/Linux | U-01~U-67 | 67 |
| Servidores Windows | W-01~W-64 | 64 |
| Servicios web | WEB-01~WEB-26 | 26 |
| Equipos de seguridad | S-01~S-23 | 23 |
| Equipos de red | N-01~N-38 | 38 |
| Sistemas de control | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| SGBD | D-01~D-26 | 26 |
| Dispositivos moviles | M-01~M-04 | 4 |
| Aplicaciones web | 21 codigos | 21 |
| Virtualizacion | HV-01~HV-25 | 25 |
| Nube | CA-01~CA-19 | 19 |

**Evaluacion administrativa**: A-1~A-127 (127 elementos, 14 dominios)
**Evaluacion fisica**: P-1~P-18 (18 elementos)

### 2. Guia de seguridad de IA — 54+ elementos

| Destinatario | Elementos | Ciclo de vida |
|--------------|:---------:|---------------|
| Desarrollador de IA | 54 | 6 etapas (Planificacion→Datos→Modelo→Despliegue→Monitoreo→Desmantelamiento) |
| Proveedor de servicios | ~43 | 6 etapas (Planificacion→Desarrollo→Operaciones→Mantenimiento→Retroalimentacion→Desmantelamiento) |
| Usuario | 7 | Mejores practicas de seguridad |

## Instalacion

```bash
claude plugins install kesekit
```

## Uso

```bash
# Iniciar evaluacion completa de seguridad
/kesekit-start

# Ejecutar lista de verificacion previa al despliegue
/kesekit-check

# Generar scripts de hardening
/kesekit-fix

# Obtener prompts de codificacion segura
/kesekit-guide
```

---

## Estructura del proyecto

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Metadatos del plugin
├── skills/                            ← Skills en ingles (enrutador)
│   ├── start/
│   │   ├── SKILL.md                  ← Enrutador (~80 lineas)
│   │   └── references/               ← Conocimiento por directriz
│   │       ├── cii/                  ← 14 archivos de referencia CII
│   │       └── ai-security/          ← 4 archivos de referencia de seguridad IA
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Skills en coreano (misma estructura)
├── authorkit/                         ← Documentos originales y materiales de trabajo
│   ├── converted/
│   │   ├── ref-001/                  ← Guia administrativa/fisica (full.md)
│   │   ├── ref-002/                  ← Guia tecnica (full.md)
│   │   └── ref-003/                  ← Guia de seguridad IA (full.md)
│   └── ...
├── 문서/                              ← PDFs originales
└── README.md
```

---

## Historial de cambios

### v2.0.0 (2026-03-30)

**Refactorizacion de estructura — Aplicacion del patron Progressive Disclosure**

| Cambio | Antes (v1.0) | Despues (v2.0) |
|--------|--------------|----------------|
| SKILL.md | Todo el conocimiento en linea (270~465 lineas) | Solo enrutador (~50~80 lineas) |
| Directrices | Solo CII | CII + seguridad IA |
| Almacenamiento de conocimiento | Codificado en SKILL.md | Separado en `references/` (18 archivos) |
| Codigos de elementos | Solo algunos elementos incluidos | Todos los elementos basados en la guia 2026 |
| Escalabilidad | Agregar directrices aumenta el numero de skills | 4 skills fijos, solo se agregan references |

**Nueva directriz: Guia de seguridad de IA**
- Fuente: Ministerio de Ciencia y TIC · KISA «Guia de seguridad de Inteligencia Artificial (IA)»
- 54 elementos de verificacion para desarrolladores de IA (ciclo de vida de 6 etapas)
- Requisitos de seguridad para proveedores de servicios de IA
- 7 reglas de seguridad para usuarios de IA

**Actualizacion de la directriz CII**
- Reextraccion completa de elementos basada en la guia detallada 2026
- Incorporacion del sistema de codigos de elementos (nuevos codigos: WEB, HV, CA, etc.)

### v1.0.0 (2026-03-29)

- Lanzamiento inicial
- 4 skills de evaluacion de vulnerabilidades CII (coreano/ingles)
- Elementos tecnicos (424) + administrativos (127) + fisicos (9)

---

## Base legal

- **Ley de proteccion de infraestructuras de informacion y comunicaciones** (Act on Protection of Information and Communications Infrastructure)
- **Ley de gobierno electronico** (e-Government Act)
- **Ley de proteccion de datos personales** (Personal Information Protection Act)
- **Ley basica de inteligencia artificial** (AI Basic Act, en vigor desde el 22.01.2026)

---

## Recursos relacionados

- [Guia detallada de KISA para evaluacion tecnica de vulnerabilidades](https://www.kisa.or.kr)
- [Guia de seguridad de Inteligencia Artificial (IA)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Construido con

| Plugin | Descripcion |
|--------|-------------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill de apoyo a la redaccion de libros — analisis de PDF, extraccion de estructura, revision/reescritura |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Compatibilidad de hooks de plugins de Claude Code en entornos Windows |

---

## Licencia

MIT License

## Autor

CDPP Corp (https://github.com/cdppcorp)
