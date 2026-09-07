[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
  ██║     ██║   ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██╔████╔██║███████║██████╔╝   ██║   
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
   Modern Terminal Visual Suite • v2.3.0
   [ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]
```

# Lumart (Luma) v2.3.0

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Language: Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![C++: 17 Multi-Core](https://img.shields.io/badge/C%2B%2B-17%20OpenMP%20SIMD-orange.svg)](https://isocpp.org/)
[![Platform: Linux / macOS / BSD](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20BSD-lightgrey.svg)](https://github.com/SilentBlox01/Luma)
[![8개 언어 지원](https://img.shields.io/badge/Languages-8%20Locales-purple.svg)](#지원-언어)

**Lumart**는 현대적인 터미널 환경을 위해 설계된 첨단 비주얼 엔지니어링 스위트입니다. 설계 원칙은 매우 명확합니다:

> **최소한의 터미널 공간에서 극대화된 시각적 밀도와 미학적 완성도를 달성한다.**

단순히 이미지의 명암을 텍스트 기호에 매핑하는 기존 아스키 변환기와 달리, Lumart는 네이티브 멀티코어 C++17(OpenMP)과 고도로 최적화된 Python으로 구현된 **4개의 특화 컴퓨터 비전 및 서브픽셀 렌더링 엔진**을 결합했습니다. 디지털 사진, 애니메이션 일러스트, 레트로 아케이드 스프라이트, 실시간 웹캠 비디오를 터미널 창 안에서 살아 숨 쉬는 그래픽 아트로 변환합니다.

---

## 목차
1. [4대 플래그십 엔진](#4대-플래그십-엔진)
   - [Mary Apex 3.5](#1-mary-apex-35-사진-실사-벡터-컬러)
   - [Trumble Orelx 2.2](#2-trumble-orelx-22-레트로-아케이드--애니메이션-셀셰이딩)
   - [Luris Mono 2.6](#3-luris-mono-26-만화-스크린톤--모노크롬)
   - [Spectra Weep 1.4](#4-spectra-weep-14-실시간-웹캠-스트리밍)
2. [엔진 비교 매트릭스](#엔진-비교-매트릭스)
3. [그래픽 이미지 내보내기 및 스티커 정책](#그래픽-이미지-내보내기-및-스티커-정책)
4. [지원 언어 (8개 언어)](#지원-언어)
5. [빠른 설치 및 패키지](#설치)
6. [CLI 명령어 전체 레퍼런스](#cli-명령어-전체-레퍼런스)
7. [실전 쿡북 및 예제](#실전-쿡북)
8. [업데이트 및 롤백 시스템](#업데이트-및-롤백-시스템)
9. [운영체제 및 데스크톱 연동](#운영체제-연동)
10. [내부 아키텍처 및 공학](#내부-아키텍처-및-공학)
11. [문제 해결](#문제-해결)
12. [라이선스](#라이선스)

---

## 4대 플래그십 엔진

```
                  ┌──────────────────────────────────────────────┐
                  │                 LUMART CLI                   │
                  └──────┬────────────┬────────────┬─────────────┘
                         │            │            │             │
        ┌────────────────┘            │            │             └────────────────┐
        ▼                             ▼            ▼                              ▼
  ┌──────────────┐             ┌──────────────┐  ┌──────────────┐          ┌──────────────┐
  │  MARY APEX   │             │TRUMBLE ORELX │  │  LURIS MONO  │          │ SPECTRA WEEP │
  │    v3.5      │             │    v2.2      │  │    v2.6      │          │     v1.4     │
  ├──────────────┤             ├──────────────┤  ├──────────────┤          ├──────────────┤
  │• C++17 OpenMP│             │• Subpixel Ink│  │• C++17 Native│          │• Live Webcam │
  │• Oklab 31-Min│             │• Capcom CPS-2│  │• DoG Lineart │          │• 30-60 FPS   │
  │• Sextants 2x3│             │• 32-bit Punch│  │• Ami-tone 8x8│          │• 5 Shaders   │
  │• Specular Fit│             │• Quad-Blocks │  │• Stickers PNG│          │• Zero-Latency│
  └──────────────┘             └──────────────┘  └──────────────┘          └──────────────┘
```

### 1. Mary Apex 3.5 (사진 실사 벡터 컬러)
* **목표**: 연속적인 마이크로 그라디언트, 복잡한 사진 조명, 자연스러운 인물 피부 톤.
* **C++17 멀티코어 엔진**: OpenMP 및 SIMD 가속 (`libmary.so` 및 실행 파일 `luma-mary`).
* **엄밀 전역 최소 Oklab 이분할 최적화 (셀당 31가지 전체 탐색)**: K-Means의 지역 최솟값 오류를 배제하고, 셀당 700나노초 이내에 31가지 분할을 전수 탐색하여 인지 색차($\Delta E$)의 전역 최솟값을 보장.
* **$O(1)$ 고속 유도 필터 및 스페큘러 하이라이트 강화 ($L > 0.82$)**: 피부 톤을 부드럽게 유지하면서 눈동자, 금속 및 반사광을 또렷하게 살려냄.
* **기본 Unicode 13.0 섹스턴트 2x3 탑재 (`-S`, `--sextants`)**: 1셀당 6개의 서브픽셀 솔리드 블록 (`🬀`-`🬻`, `█`, `▌`, `▐`). 2x4 점자 (`-B`), 2x2 쿼드런트 (`-Q`), 하프 블록 (`--blocks`), Scharr 방향성 ASCII 지원.
* **엄격한 알파 채널 격리**: 투명 영역이 경계선 색상을 왜곡하지 않아 외곽선에 검은 번짐이 생기지 않음.
* **터미널 캔버스 내보내기**: 이미지 파일(`.png`, `.jpg`) 저장 시 다크 터미널 캔버스(`#0c0c0c`) 위에 렌더링되어 품격 있는 터미널 아트의 정체성을 보존.

### 2. Trumble Orelx 2.2 (레트로 아케이드 & 애니메이션 셀셰이딩)
* **목표**: 애니메이션 일러스트, 게임 스프라이트, 코믹스 및 팝아트.
* **1-대-1 서브픽셀 선행 인킹**: 양방향 필터 및 Canny 외곽선 감지가 리사이즈 *이후*가 아닌 서브픽셀 해상도에서 직접 수행되어, 잉크 윤곽선이 정확히 1 서브픽셀 두께를 유지하고 번짐을 방지.
* **32비트 캡콤 CPS-2 / SNK 네오지오 아케이드 팔레트**: 90년대 대전 액션 게임 특유의 펀치력 있는 컬러 커브 (채도 +28%, 대비 +15% 강화).
* **적응형 쿼드런트 형상 보정**: 형상 페널티 하한을 30으로 완화하여 대각선 블록(`▞`, `▚`, `▘`, `▝`)이 눈매, 머리카락 및 의복의 유기적 곡선을 섬세하게 추적.

### 3. Luris Mono 2.6 (만화 스크린톤 & 모노크롬 C++17)
* **목표**: 정통 일본 만화 인쇄물, 잉크 드로잉, 펜화 및 투명 스티커.
* **DoG(가우시안 차분) 외곽선 추출**: 터미널 크기에 맞춰 반경을 자동 조절하며 텍스처 노이즈 없는 선명한 펜 선을 추출.
* **Manga Screentone 2.0 (*Ami-tone*)**: 8x8 Bayer 분산 행렬을 사용해 일본식 인쇄 망점 스크린톤을 터미널 위에 완벽하게 재현.
* **앳킨슨(Atkinson) 오차 확산 (1984 MacPaint)**: 빌 앳킨슨이 고안한 명작 알고리즘으로 잔여 에너지 25%를 보존해 지저분한 노이즈 없이 정갈한 톤을 형성.
* **투명 스티커 전용 엔진 (`--transparent`)**: Luris Mono는 **투명 배경 PNG 스티커를 출력할 수 있는 유일한 엔진**으로, 메신저용 이모티콘 제작에 최적화.

### 4. Spectra Weep 1.4 (실시간 웹캠 스트리밍)
* **목표**: 터미널 창에서 30~60 FPS의 초저지연 실시간 비디오 스트리밍 (`lumart --webcam` 또는 `lumart -W`).
* **제로 레이턴시**: 터미널 주사율과 완벽하게 동기화된 V4L2/OpenCV 파이프라인.
* **5가지 라이브 셰이더 필터**: Normal TrueColor, Weep Cyberpunk, Matrix Green Rain, Thermal FLIR, Manga Ink.

---

## 엔진 비교 매트릭스

| 기능 | Mary Apex 3.5 | Trumble Orelx 2.2 | Luris Mono 2.6 | Spectra Weep 1.4 |
| :--- | :--- | :--- | :--- | :--- |
| **비주얼 스타일** | 실사 벡터 컬러 | 레트로 아케이드 셀셰이딩 | 일본 만화 망점 / 잉크 | 실시간 비디오 / 웹캠 |
| **기반 언어** | C++17 OpenMP + SIMD | Python + 가속 OpenCV | C++17 네이티브 | Python + OpenCV V4L2 |
| **색 공간** | Oklab 인지 색차 ($\Delta E$) | 32비트 캡콤 CPS-2 펀치 | 모노크롬 / Ami-tone | TrueColor / 셰이더 RGB |
| **기본 모드** | **섹스턴트 2x3 (`-S`)** | **쿼드런트 2x2 (`--blocks`)**| **만화 2.0 (`-m`)** | **30-60 FPS 스트림** |
| **서브픽셀 밀도** | 셀당 최대 6 서브픽셀 | 셀당 최대 4 서브픽셀 | 셀당 최대 4 서브픽셀 | 동적 크기 |
| **외곽선 인킹** | 부드러운 안티앨리어싱 | **Canny 1-대-1 서브픽셀** | **적응형 DoG 선화** | 선택 사양 (셰이더) |
| **내보내기 캔버스**| 다크 터미널 (`.png`, `.jpg`)| 다크 터미널 (`.png`, `.jpg`)| **PNG 스티커 (`--transparent`)**| 즉시 캡처 |
| **실행 명령어** | `-E mary -S` | `-E trumble --blocks` | `-E luris -m` | `-W` 또는 `--webcam` |

---

## 그래픽 이미지 내보내기 및 스티커 정책

Lumart는 터미널 아트를 스튜디오 표준 해상도인 **160열**로 고해상도 그래픽 이미지(`-o output.png` 또는 `-o output.jpg`)로 내보낼 수 있습니다.

### 1. WebP 형식 영구 지원 중단
* **`.webp` 형식으로의 내보내기는 영구적으로 비활성화되었습니다**.
* `.webp` 파일을 지정할 경우 작업이 안전하게 중단되며 `.png` 또는 `.jpg` 사용을 안내합니다.
* 지원 형식:
  * **`.png`**: 무손실 압축 및 알파 채널 투명도 완전 지원.
  * **`.jpg` / `.jpeg`**: 광범위한 호환성 및 95% 품질 최적화.

### 2. 투명 스티커는 Luris Mono 전용
* 컬러 엔진 이미지를 투명 배경으로 오려내 일반 뷰어에서 보면 터미널 프레임이 사라져 저화질 이미지처럼 보일 위험이 있습니다. 따라서 컬러 엔진은 항상 **기품 있는 다크 터미널 캔버스(`#0c0c0c`)** 위로 저장됩니다.
* **흑백 만화(Luris Mono)**는 망점 패턴과 잉크 선화가 스티커로서 완벽한 완성도를 가지므로 `--transparent`를 통한 투명 스티커 출력이 허용됩니다.

---

## 지원 언어

Lumart는 **8개 언어**를 완벽하게 지원합니다:

| 코드 | 언어명 | 자동 감지 | 수동 설정 |
| :---: | :--- | :--- | :--- |
| `ko` | 한국어 | `$LANG=ko_*` | `lumart --lang ko` |
| `en` | English | `$LANG=en_*` (기본값) | `lumart --lang en` |
| `es` | Español | `$LANG=es_*` | `lumart --lang es` |
| `pt` | Português | `$LANG=pt_*` | `lumart --lang pt` |
| `fr` | Français | `$LANG=fr_*` | `lumart --lang fr` |
| `ru` | Русский | `$LANG=ru_*` | `lumart --lang ru` |
| `ja` | 日本語 | `$LANG=ja_*` | `lumart --lang ja` |
| `de` | Deutsch | `$LANG=de_*` | `lumart --lang de` |

---

## 설치

### 원라이너 자동 설치 (권장)
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### 소스코드 빌드 및 설치
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
chmod +x install.sh
./install.sh
```

---

## CLI 명령어 전체 레퍼런스

```text
사용법: lumart [옵션] <이미지_경로_또는_URL>
```

| 옵션 | 인자 | 설명 |
| :--- | :--- | :--- |
| `-E`, `--engine` | `mary` \| `trumble` \| `luris` \| `spectra` | 렌더링 엔진 선택. |
| `-S`, `--sextants`| — | 유니코드 2x3 섹스턴트 블록 (셀당 6 서브픽셀). |
| `-B`, `--braille` | — | 유니코드 2x4 점자 문자 (셀당 8 서브픽셀). |
| `-Q`, `--quadrants`| — | 유니코드 2x2 쿼드런트 블록 (셀당 4 서브픽셀). |
| `--blocks` | — | 최적화된 터미널 블록 문자 사용. |
| `-a`, `--ascii` | — | 전통적인 영숫자 ASCII 문자만 사용. |
| `-m`, `--manga` | — | 만화 스크린톤 2.0 모드 (Bayer 8x8 망점 + DoG 선화). |
| `-s`, `--sketch`| — | 깔끔한 펜화 스케치 모드. |
| `-w`, `--width` | `<정수>` | 출력 너비(열 수, 기본값: 터미널 크기 자동 감지). |
| `-i`, `--invert`| — | 명암 반전 (밝은 배경 터미널용). |
| `--raw-colors` | — | 필터와 셰이딩을 끄고 원본 이미지 색상 사용. |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | 디더링 알고리즘 선택. |
| `--swap` | `<색상1> <색상2>` | RGB 3D 공간에서 동적 색상 교체. |
| `-o`, `--output` | `<파일.png / .jpg>` | 고해상도 그래픽 이미지로 저장. |
| `--transparent` | — | **Luris Mono 전용**: 투명 배경 스티커 생성. |
| `-W`, `--webcam`| `[id]` | 터미널 실시간 웹캠 스트리밍 (30-60 FPS). |
| `--instant` | — | 프로그레시브 스캔 효과를 끄고 즉시 출력. |
| `--paste` | — | 클립보드에 복사된 이미지를 즉시 렌더링. |
| `--lang` | `<코드>` | 인터페이스 언어 설정 (`ko`, `en`, `es` 등). |
| `-H`, `--history` | `[N]` | 최근 N개의 실행 기록 조회. |
| `-R`, `--replay` | `[N]` | 기록에서 N번째 명령 재실행. |
| `--install-desktop` | — | 리눅스 우클릭 메뉴에 "Lumart로 열기" 등록. |
| `-v`, `--version` | — | 하드웨어, OS 및 엔진 진단 보고서 출력. |
| `-u`, `--check-update`| — | GitHub 최신 릴리스 확인. |
| `-uu`, `--upgrade` | — | 대화형 자동 업그레이드 실행. |
| `-dg`, `--downgrade` | `[버전]` | 이전 버전으로 대화형 롤백. |

---

## 실전 쿡북

### 1. Mary Apex 3.5 사진 실사 렌더링
```bash
lumart photo.jpg -E mary -S -w 90
```

### 2. Trumble Orelx 2.2 애니메이션 아트
```bash
lumart anime.png -E trumble --blocks -w 85
```

### 3. 투명 배경 일본 만화 스티커 제작 (Luris Mono)
```bash
lumart manga.png -m --transparent -o sticker.png
```

### 4. 터미널 실시간 웹캠 실행
```bash
lumart -W
```

### 5. 클립보드 이미지 즉시 렌더링
```bash
lumart --paste -E trumble --blocks
```

---

## 라이선스

Lumart는 GNU Affero General Public License v3.0 (**AGPL-3.0**)에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 확인하세요.
