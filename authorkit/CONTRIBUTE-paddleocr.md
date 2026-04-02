# Contribution: PaddleOCR 기반 한국어 PDF 변환 파이프라인

> authorkit의 PDF → Markdown 변환 시 한국어 OCR 품질을 대폭 개선하는 PaddleOCR 통합 제안

## 배경

authorkit의 기존 `convert_pdf.py`는 pymupdf(`fitz`)의 `get_text("text")`를 사용하여 PDF에서 텍스트를 추출합니다. 대부분의 경우 잘 작동하지만, 다음 상황에서 한국어 텍스트 추출 품질이 크게 저하됩니다:

| 문제 상황 | 증상 |
|----------|------|
| 이미지 기반 PDF (스캔본) | 텍스트 추출 자체가 불가 |
| 한국어 폰트가 임베드되지 않은 PDF | 깨진 문자 또는 빈 텍스트 |
| 표지/도해 페이지 | 텍스트 레이어 없이 이미지만 존재 |
| 정부/공공기관 발행 PDF | CID 폰트 사용으로 한글 추출 실패 빈번 |

## 해결책: PaddleOCR Hybrid 방식

pymupdf 텍스트 추출을 1차 시도하고, 실패 시 PaddleOCR로 폴백하는 **하이브리드 방식**을 구현했습니다.

```
[PDF 페이지]
    │
    ▼
[pymupdf get_text()]
    │
    ├─ 텍스트 충분 & 한국어 비율 정상 → 그대로 사용 (빠름)
    │
    └─ 텍스트 부족 or 한국어 비율 < 5% → PaddleOCR 폴백
        │
        ▼
    [페이지 → 2x 이미지 렌더링]
        │
        ▼
    [PaddleOCR (korean, confidence > 0.5)]
        │
        ▼
    [OCR 텍스트 사용]
```

### 핵심 로직

```python
# pymupdf 텍스트 추출 시도
raw_text = page.get_text("text").strip()

# 한국어 비율 기반 OCR 필요 여부 판단
korean_ratio = len(re.findall(r'[가-힣]', raw_text)) / max(len(raw_text), 1)
use_ocr = len(raw_text) < 50 or korean_ratio < 0.05

if use_ocr:
    # 2x 해상도로 이미지 렌더링 → PaddleOCR
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)
    # ... OCR 수행
```

### 왜 PaddleOCR인가?

| OCR 엔진 | 한국어 정확도 | 속도 | GPU 지원 | 설치 용이성 |
|----------|:----------:|:----:|:-------:|:---------:|
| Tesseract | 중 | 느림 | X | 별도 바이너리 필요 |
| EasyOCR | 중상 | 보통 | O | pip만으로 가능 |
| **PaddleOCR** | **상** | **빠름** | **O** | **pip만으로 가능** |
| Google Vision | 최상 | 빠름 | - | API 키 필요, 유료 |

PaddleOCR은 한국어 인식 정확도가 높고, GPU 가속을 지원하며, 오프라인으로 동작합니다.

## 실제 적용 결과

KISA 발행 「우주 보안모델」 시리즈 5개 PDF (총 628페이지)를 변환한 결과:

| 문서 | 페이지 | 추출 문자수 | 헤딩 탐지 | 비고 |
|------|:------:|:----------:|:---------:|------|
| 우주 보안모델 Part1 요약본 | 22 | 12,746 | 21 | 표지 OCR 성공 |
| 우주 보안모델 Part1 | 134 | 117,974 | 481 | 목차/본문 정상 추출 |
| 우주 보안모델 Part2 요약본 | 31 | 16,547 | 24 | 도해 페이지 OCR 적용 |
| 우주 보안모델 Part2 | 223 | 195,171 | 129 | GSaaS 전문 용어 정상 |
| 우주 보안모델 해설서 | 218 | 208,471 | 276 | 53개 체크리스트 완전 추출 |
| **합계** | **628** | **550,909** | **931** | |

## 추가 구현 사항

### 1. 배치 모드 지원

```bash
python convert_pdf_ocr.py --batch <pdf_dir> <output_base_dir> <start_ref_num>
```

여러 PDF를 한 번에 순차 변환하고 최종 요약을 출력합니다.

### 2. 이미지 추출 개선

- 50x50px 미만 장식 이미지 자동 스킵
- CMYK → RGB 자동 변환
- colorspace 호환 에러 graceful 처리

### 3. 한국어 헤딩 패턴 확장

```python
# 기존: 제N장, N.X 패턴만
# 추가: 제I장 (로마자), 제N절, 가/나/다 패턴
if re.match(r'^제?\s*\d+장', line) or re.match(r'^제?\s*[IVX]+\s*[\.장]', line):
    # chapter heading
elif re.match(r'^\d+\.\s+[가-힣A-Z]', line):
    # section heading
```

## 설치 방법

### 요구사항

- Python 3.10~3.12 (PaddlePaddle이 3.13 미지원)
- CUDA 11.x~12.x (GPU 사용 시)

### 설치

```bash
# CPU 전용
pip install paddlepaddle==2.6.2 "paddleocr==2.9.1" pymupdf

# GPU (CUDA 12.x + cuDNN 8.x 필요)
pip install paddlepaddle-gpu==2.6.2 "paddleocr==2.9.1" pymupdf
```

### 호환성 참고

| PaddlePaddle | PaddleOCR | Python | 비고 |
|:------------:|:---------:|:------:|------|
| 2.6.2 | 2.9.1 | 3.10~3.12 | 안정 조합 |
| 2.6.2 | 3.4.0 | 3.10~3.12 | `set_optimization_level` 에러 — 비호환 |
| GPU | 2.9.1 | 3.12 | cuDNN 8 필요 (12.x 드라이버와 별도) |

**권장**: `paddlepaddle==2.6.2` + `paddleocr==2.9.1` 조합이 가장 안정적입니다.

Python 3.13 환경에서는 별도 venv를 만들어 사용:

```bash
py -3.12 -m venv .venv-ocr
.venv-ocr/Scripts/python.exe -m pip install paddlepaddle==2.6.2 "paddleocr==2.9.1" pymupdf
```

## authorkit 통합 제안

### 방안 A: analyze 스킬에 OCR 옵션 추가

```markdown
# analyze 스킬 사용 시
/authorkit:analyze --ocr korean path/to/document.pdf
```

analyze 스킬이 `convert_pdf.py` 대신 `convert_pdf_ocr.py`를 호출하도록 분기.

### 방안 B: convert_pdf.py에 OCR 폴백 통합

기존 `convert_pdf.py`에 PaddleOCR 폴백을 옵셔널로 통합:

```python
try:
    from paddleocr import PaddleOCR
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

# 텍스트 추출 실패 시에만 OCR 사용
if use_ocr and OCR_AVAILABLE:
    # PaddleOCR 폴백
elif use_ocr:
    print("Warning: OCR not available. Install paddleocr for better results.")
```

PaddleOCR가 설치되지 않은 환경에서도 기존 동작이 유지됩니다.

### 방안 C: 별도 OCR 프리프로세서

`convert_pdf_ocr.py`를 독립 도구로 유지하고, authorkit 워크플로우에서 선택적으로 호출.

## 제공 파일

| 파일 | 설명 |
|------|------|
| `convert_pdf_ocr.py` | PaddleOCR 기반 PDF→MD 변환기 (단일/배치 모드) |
| 이 문서 | 컨트리뷰션 설명 및 통합 제안 |

## 라이선스

PaddleOCR: Apache License 2.0
본 코드: authorkit 프로젝트 라이선스를 따름
