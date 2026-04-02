# Contributing to KESE-KIT

## 새 가이드라인 추가 방법

KESE-KIT은 **스킬 4개 고정 + references 확장** 구조입니다. 새 보안 가이드라인을 추가할 때 스킬 파일을 수정할 필요 없이 reference 파일만 추가하면 됩니다.

### Step 1: 원본 문서 준비

```
authorkit/new pdf/           ← PDF 파일 배치
```

### Step 2: PDF를 Markdown으로 변환

```bash
python authorkit/convert_pdf.py "authorkit/new pdf/가이드라인.pdf" authorkit/converted/ref-XXX ref-XXX
```

### Step 3: Reference 파일 작성

`skills-ko/kesekit-start-ko/references/` 아래에 새 가이드라인 디렉터리를 생성합니다:

```
skills-ko/kesekit-start-ko/references/
├── cii/                    ← 기존
├── ai-security/            ← 기존
└── new-guideline/          ← 신규
    ├── overview.md
    ├── category-1.md
    └── category-2.md
```

각 reference 파일은 다음을 포함해야 합니다:
- 항목 코드, 이름, 중요도
- 점검 내용 및 판단 기준 (양호/취약)
- 점검 명령어 또는 확인 방법
- 조치 방법

### Step 4: SKILL.md 라우터 업데이트

`skills-ko/kesekit-start-ko/SKILL.md`의 가이드라인 선택 테이블에 새 가이드라인을 추가합니다:

```markdown
| 3 | **새 가이드라인** | 설명 | 항목 수 |
```

그리고 새 분기 섹션을 추가합니다:

```markdown
## 새 가이드라인 분기 시

`references/new-guideline/` 디렉터리에서 해당 reference를 읽어 평가합니다.
```

**4개 스킬 (kesekit-start, kesekit-check, kesekit-fix, kesekit-guide) 모두 동일하게 업데이트합니다.**

### Step 5: References 복사

모든 스킬 디렉터리에 references를 복사합니다:

```bash
# 한국어 스킬
cp -r skills-ko/kesekit-start-ko/references/new-guideline skills-ko/kesekit-check-ko/references/
cp -r skills-ko/kesekit-start-ko/references/new-guideline skills-ko/kesekit-fix-ko/references/
cp -r skills-ko/kesekit-start-ko/references/new-guideline skills-ko/kesekit-guide-ko/references/

# 영문 스킬
cp -r skills-ko/kesekit-start-ko/references/new-guideline skills/kesekit-start/references/
cp -r skills-ko/kesekit-start-ko/references/new-guideline skills/kesekit-check/references/
cp -r skills-ko/kesekit-start-ko/references/new-guideline skills/kesekit-fix/references/
cp -r skills-ko/kesekit-start-ko/references/new-guideline skills/kesekit-guide/references/
```

### Step 6: marketplace.json 업데이트

`.claude-plugin/marketplace.json`의 `keywords`와 `description`에 새 가이드라인 관련 키워드를 추가합니다.

### Step 7: README 업데이트

`README.md`와 `docs/` 아래 각 언어별 README에 새 가이드라인 정보를 추가합니다.

### Step 8: 검증 스크립트 실행

PR을 올리기 전에 아래 검증 스크립트를 실행하세요:

```bash
node scripts/validate-content.mjs
```

이 스크립트는 다음을 검사합니다:
- README / SKILL / reference 간 항목 수 정합성
- `start/check/fix/guide` 간 reference 파일 목록 및 내용 드리프트
- Robot Security 라우터 분기 누락 여부

GitHub Actions에서도 동일한 검증이 자동 실행됩니다.

---

## Reference 파일 작성 가이드

### 구조

```markdown
# [시스템명] 취약점 분석·평가 항목

> 출처 정보

## 1. 카테고리명 (N항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| XX-01 | 항목명 | 상 |

### 주요 점검 명령어
```

### 원칙

1. **Progressive Disclosure**: SKILL.md < 500줄, reference는 무제한
2. **자기 완결적**: reference 파일만 읽어도 평가 가능해야 함
3. **실용적**: 점검 명령어와 조치 방법을 반드시 포함
4. **한국어 기준**: 원본 가이드의 용어를 그대로 사용

### 파일 크기 가이드

| 항목 수 | 권장 줄 수 |
|:------:|:---------:|
| ~20개 | 100~200줄 |
| ~50개 | 200~400줄 |
| ~100개 | 400~600줄 |
| 100+개 | 분할 권장 |

---

## 버전 관리

- `marketplace.json`의 `version` 필드를 업데이트
- `README.md`의 변경 이력에 기록
- 커밋 메시지: `feat: Add [가이드라인명] security guideline`
