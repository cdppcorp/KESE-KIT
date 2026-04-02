# authorkit 설정 질문지

> 각 `> Answer:` 줄 아래에 답변을 작성해주세요.
> 작성 완료 후 `/authorkit.init`을 다시 실행하면 프로젝트가 설정됩니다.

---

## 1. 작업 유형
- [x] 참고자료를 기반으로 새 책 집필


## 2. 도서 분류

- [x] 실용/교육 가이드 (예: 엑셀 입문서)


## 3. 대상 독자
> Answer: 바이브코딩을 하는 사람, 개발자지만 서버를 운용하는 사람, 정부과제로 개발을 하는 사람, 공공조달시장에서 개발을 하는 사람, 정부 관련 코딩하는 사람, 서버를 처음 다루는 사람, JavaScript/Python으로 웹 서비스를 개발하는 사람, AI 도구(Claude, Cursor, Copilot)로 코딩하면서 보안을 신경 쓰고 싶은 사람

## 4. 책 제목 (가제)
> Answer: KESE KIT: Korea Enhanced Security Evaluation - KISA Infrastructure Toolkit

## 5. 참고자료
참고자료가 있는 폴더 경로를 입력하세요.
지원 형식: pdf, docx, txt, xlsx, hwpx
폴더가 아닌 경우 파일명을 직접 입력하세요. 없으면 "없음"이라고 입력하세요.
> Answer: C:\Users\Nowzero\PycharmProjects\Skills\KESE-KIT\authorkit\new pdf

참고자료 목록:
- ref-011: Javascript_시큐어코딩_가이드(2023년_개정본).pdf (159p, KISA, 42개 항목)
- ref-012: Python_시큐어코딩_가이드(2023년_개정본).pdf (176p, KISA, 46개 항목)

기존 참고자료 (authorkit/converted/에 분석 완료):
- ref-001~010: CII 기술/관리/물리, AI 보안, 로봇 보안, 우주 보안 가이드

## 6. 기존 원고
원고가 있는 폴더 경로를 입력하세요.
지원 형식: pdf, docx, txt, xlsx, hwpx, md
폴더가 아닌 경우 파일명을 직접 입력하세요. 없으면 "없음"이라고 입력하세요.
> Answer: 없음 (기존 kesekit 스킬의 references/ 파일들을 원고 대신 활용)

## 7. 목차
- [x] 있음 (아래에 작성하거나 파일 경로 입력)
- [ ] 없음 (참고자료 기반으로 제안받고 싶음)
> Answer:

### 변환 목표 구조 (kesekit guide 스킬용 reference 파일)

```
references/secure-coding/
├── overview.md              ← 시큐어코딩 개요, 7개 카테고리 설명, CWE 매핑 요약
├── javascript.md            ← JS 시큐어코딩 42개 항목 (안전/위험 코드 예시)
└── python.md                ← Python 시큐어코딩 46개 항목 (안전/위험 코드 예시)
```

각 항목 구조:
1. 보안약점명 + CWE 코드
2. 설명 (위험성, 영향)
3. 안전하지 않은 코드 예시
4. 안전한 코드 예시
5. 점검 기준

## 8. 문체 설정
기존 원고가 있으면 비워두세요 — 자동 분석됩니다.

문장 종결어미 (예: 합니다체, 해요체, 한다체):
> Answer: 합니다체

경어 수준 (예: 존칭, 평어):
> Answer: 평어

특수 요소 (예: 팁 박스, 주의 박스, 연습문제):
> Answer: 팁박스, 주의박스, 코드블록(안전/위험 코드 쌍)

용어 표기 형식 (예: "한글(영문, 약어)"):
> Answer: 한글(영문, 약어) — 예: SQL 삽입(SQL Injection, CWE-89)

## 9. 작업 디렉토리
비워두면 현재 프로젝트 루트에 `authorkit/` 폴더가 생성됩니다.
> Answer: C:\Users\Nowzero\PycharmProjects\Skills\KESE-KIT\authorkit
