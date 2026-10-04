[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
  ██║     ██║   ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██╔████╔██║███████║██████╔╝   ██║   
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
   Modern Terminal Visual Suite • v2.4.1 (Apex Horizon)
   [ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]
```

# Lumart (Luma) v2.4.1

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
3. [비주얼 갤러리 및 결과물 쇼케이스](#비주얼-갤러리-및-결과물-쇼케이스)
4. [그래픽 이미지 내보내기, 애니메이션 및 스티커 정책](#그래픽-이미지-내보내기-애니메이션-및-스티커-정책)
5. [지원 언어 (8개 언어)](#지원-언어)
6. [설치](#설치)
7. [CLI 명령어 전체 레퍼런스](#cli-명령어-전체-레퍼런스)
8. [실전 쿡북 및 예제](#실전-쿡북)
9. [엔지니어링 비밀, Pro-Tips & 터미널 철학](#엔지니어링-비밀-pro-tips--터미널-철학)
10. [업데이트 및 롤백 시스템](#업데이트-및-롤백-시스템)
11. [운영체제 및 데스크톱 연동](#운영체제-및-데스크톱-연동)
12. [내부 아키텍처 및 수학 원리](#내부-아키텍처-및-수학-원리)
13. [문제 해결](#문제-해결)
14. [라이선스](#라이선스)

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
* **기본 Unicode 13.0 섹스턴트 2x3 탑재**: 1셀당 6개의 서브픽셀 솔리드 블록 (`🬀`-`🬻`, `█`, `▌`, `▐`). 2x4 점자 (`-B`), 2x2 쿼드런트 (`-Q`), 하프 블록 (`--blocks`) 지원.
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

## 비주얼 갤러리 및 결과물 쇼케이스

### 1. 엔진 맞대결: Mary Apex 3.5 vs Trumble Orelx 2.2
![Lumart 엔진 비교 쇼다운](assets/engine_showdown.png)

### 2. 나란히 비교: 실사 TrueColor vs 투명 만화 스티커

| Mary Apex 3.5 (실사 벡터 TrueColor) | Luris Mono 2.6 (투명 만화 스티커) |
| :---: | :---: |
| ![Cinderella Mary](assets/cinderella_mary_apex.png)<br><sub>`lumart cinderella.jpg` *(Mary 섹스턴트 기본값)*</sub> | ![Cinderella Manga Sticker](assets/cinderella_manga_sticker.png)<br><sub>`lumart cinderella.jpg -m --transparent -o sticker.png`</sub> |
| ![Hanako Mary Boosted](assets/hanako_boosted.png)<br><sub>`lumart hanako.png --boost` *(Punch Arcade Retinex)*</sub> | ![Hanako Manga Sticker](assets/hanako_manga_sticker.png)<br><sub>`lumart hanako.png -m --transparent -o sticker.png`</sub> |
| ![Gothic Nun Mary](assets/gothic_nun_mary.png)<br><sub>`lumart gothic_nun.png`</sub> | ![Gothic Nun Manga Sticker](assets/gothic_nun_manga_sticker.png)<br><sub>`lumart gothic_nun.png -m --transparent -o sticker.png`</sub> |
| ![Slime Mary](assets/slime_mary.png)<br><sub>`lumart slime.png`</sub> | ![Slime Manga Sticker](assets/slime_manga_sticker.png)<br><sub>`lumart slime.png -m --transparent -o sticker.png`</sub> |

### 3. 서브픽셀 글리프 텍스처 밀도

| 섹스턴트 2x3 (`-S` / 기본값) | 점자 Braille 2x4 (`-B`) | 쿼드런트 2x2 (`-Q`) |
| :---: | :---: | :---: |
| ![Sextants 2x3](assets/texture_sextants.png)<br><sub>셀당 6 서브픽셀 (자연스러운 그라디언트)</sub> | ![Braille 2x4](assets/texture_braille.png)<br><sub>셀당 8 서브픽셀 (정밀 점묘 & 포트레이트)</sub> | ![Quadrants 2x2](assets/texture_quadrants.png)<br><sub>셀당 4 서브픽셀 (픽셀아트 & 아케이드)</sub> |

---

## 그래픽 이미지 내보내기, 애니메이션 및 스티커 정책

Lumart는 터미널 아트를 스튜디오 표준 해상도인 **160열**로 고해상도 그래픽 이미지(`-o output.png`, `-o output.jpg` 또는 `-o anim.gif`)로 내보낼 수 있습니다.

### 1. 애니메이션 모드 및 애니메이션 GIF 내보내기 (`--loop`)
![터미널 애니메이션 데모](assets/animated_demo.gif)

Lumart v2.4.0에는 애니메이션 파일(GIF 및 APNG)에 대한 네이티브 지원이 추가되었습니다:
* **터미널에서의 부드러운 재생**: `lumart anim.gif --loop` 는 각 프레임을 사전에 계산하여 ANSI 시퀀스로 캐싱하여 터미널 내에서 60 FPS로 부드럽게 반복 재생합니다.
* **애니메이션 GIF 생성**: `lumart anim.gif --loop -o output.gif` (또는 `--save output.gif`)는 각 프레임을 고정밀 서브픽셀로 래스터화하여 완전한 애니메이션 GIF를 생성합니다.

### 2. WebP 형식 영구 지원 중단
* **`.webp` 형식으로의 내보내기는 영구적으로 비활성화되었습니다**.
* `.webp` 파일을 지정할 경우 작업이 안전하게 중단되며 `.png`, `.jpg` 또는 `.gif` 사용을 안내합니다.
* 지원 형식:
  * **`.png`**: 무손실 압축 및 알파 채널 투명도 완전 지원.
  * **`.jpg` / `.jpeg`**: 광범위한 호환성 및 95% 품질 최적화.
  * **`.gif`**: 웹 및 터미널용 멀티프레임 애니메이션.

### 3. 투명 스티커는 Luris Mono 전용
* 컬러 엔진 이미지를 투명 배경으로 오려내 일반 뷰어에서 보면 터미널 프레임이 사라져 저화질 이미지처럼 보일 위험이 있습니다. 따라서 컬러 엔진은 항상 **기품 있는 다크 터미널 캔버스(`#0c0c0c`)** 위로 저장됩니다.
* **흑백 만화(Luris Mono)**는 망점 패턴과 잉크 선화가 스티커로서 완벽한 완성도를 가지므로 `--transparent`를 통한 투명 스티커 출력이 허용됩니다 (95% 이상의 검증된 투명도).
* Mary나 Trumble에서 `--transparent`를 지정할 경우 알림을 표시하고 터미널 배경을 유지하여 고품질로 저장합니다.

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

### 방법 3: 사전 컴파일된 네이티브 Linux 패키지
[GitHub Releases](https://github.com/SilentBlox01/Luma/releases)에서 배포판별 패키지를 직접 다운로드할 수 있습니다:
* **Debian / Ubuntu / Linux Mint**: `sudo apt install ./lumart-*.deb`
* **Fedora / RHEL / AlmaLinux**: `sudo dnf install ./lumart-*.rpm`
* **Arch Linux / Manjaro**: `dist/arch` 디렉터리에서 `makepkg -si`

---

## CLI 명령어 전체 레퍼런스

```text
사용법: lumart [옵션] <이미지_경로_또는_URL>
```

| 옵션 | 인자 | 설명 |
| :--- | :--- | :--- |
| `-E`, `--engine` | `mary` \| `trumble` \| `luris` \| `spectra` | 렌더링 엔진 명시적 선택 (기본값: 자동 라우팅). |
| `-S`, `--sextants`| — | Unicode 2x3 섹스턴트 블록 사용 (Mary Apex 플래그십 기본값). |
| `-m`, `--manga` | — | 만화 스크린톤 2.0 모드 (Bayer 8x8 망점 + DoG 선화). |
| `-s`, `--sketch`| — | 깔끔한 펜화 스케치 모드. |
| `-B`, `--braille` | — | 유니코드 2x4 점자 문자 (셀당 8 서브픽셀). |
| `-Q`, `--quadrants`| — | 유니코드 2x2 쿼드런트 블록 (셀당 4 서브픽셀). |
| `--blocks` | — | 최적화된 터미널 블록 문자 사용 (`▀` / `▄`). |
| `-w`, `--width` | `<정수>` | 출력 너비(열 수, `-F`와 호환되지 않음). |
| `-F`, `--fit` | — | **뷰포트 자동 맞춤**: 스크롤 없이 터미널 화면에 맞추도록 가로/세로를 자동 계산 (`-w`와 호환되지 않음). |
| `--fastfetch`, `--logo` | — | 로고용 빈 여백/투명 테두리 자동 트리밍. |
| `-c`, `--color` | — | TrueColor 풀 컬러 모드로 출력 강제 (기본값). |
| `--no-color` | — | 컬러 출력을 비활성화하고 흑백 엔진 사용. |
| `--font-ratio` | `<소수>` | 터미널 폰트 가로/세로 비율 보정 (기본값: `0.5`). |
| `--boost`, `--vibrant` | — | 선명한 아케이드 스타일 출력을 위해 채도, 대비 및 Retinex 효과를 적용합니다. |
| `-i`, `--invert`| — | 명암 반전 (밝은 배경 터미널용; `-m` 모드 자동 감지 지원). |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | 디더링 알고리즘 선택. |
| `--swap` | `<색상1> <색상2>` | RGB 3D 공간에서 동적 색상 교체. |
| `-o`, `-O`, `--output`, `--save` | `<파일.png / .jpg / .gif>` | 고해상도 그래픽 이미지 또는 애니메이션 GIF로 저장. |
| `--loop` | — | **애니메이션 모드**: 터미널 반복 재생 또는 애니메이션 GIF 내보내기. |
| `--transparent` | — | **Luris Mono 전용**: 투명 배경 스티커 생성. |
| `--instant` | — | 프로그레시브 스캔 애니메이션 없이 즉시 출력 (기본값). |
| `--reveal` | — | 한 줄씩 출력되는 프로그레시브 스캔 애니메이션 활성화. |
| `--paste` | — | 클립보드에 복사된 이미지를 즉시 렌더링. |
| `-W`, `--webcam`| `[id]` | 터미널 실시간 웹캠 스트리밍 (30-60 FPS). |
| `--lang` | `<코드>` | 인터페이스 언어 설정 (`ko`, `en`, `es` 등). |
| `-H`, `--history` | `[N]` | 최근 N개의 실행 기록 조회. |
| `-R`, `--replay` | `[N]` | 기록에서 N번째 명령 재실행. |
| `--clear-history`| — | 저장된 명령 기록 삭제. |
| `--install-desktop` | — | 리눅스 우클릭 메뉴에 "Lumart로 열기" 등록. |
| `-v`, `--version` | — | 하드웨어, OS 및 엔진 진단 보고서 출력. |
| `-u`, `--check-update`| — | GitHub 최신 릴리스 확인. |
| `-uu`, `--upgrade` | — | 대화형 자동 업그레이드 실행. |
| `-dg`, `--downgrade` | `[버전]` | 이전 버전으로 대화형 롤백. |

---

## 실전 쿡북

### 1. 고해상도 터미널 렌더링 (기본 모드 또는 명시적 플래그)
```bash
# 터미널 창 너비에 맞춰 자연스러운 컬러로 즉시 렌더링 (Zero-Flag)
lumart photo.jpg

# 동일한 명시적 플래그 실행
lumart photo.jpg -E mary -S -w 90

# 출력 폭을 110열로 직접 지정
lumart portrait.png -w 110

# 채도 및 Retinex 명암비 부스트 (아케이드 발색)
lumart photo.jpg --boost

# Trumble 아케이드 셀 셰이딩 블록 렌더링
lumart anime.png -E trumble --blocks
```

### 2. 문자 텍스처 모드
```bash
# 부드러운 점자 2x4 서브픽셀
lumart character.png -B

# 고밀도 사분면(Quadrants) 2x2 블록
lumart character.png -Q

# 클래식 아케이드 하프블록 (Capcom CPS-2 / Neo-Geo 스타일)
lumart character.png --blocks -w 85
```

### 3. 투명 배경 일본 만화 스티커 제작 (Luris Mono)
```bash
# Discord 및 Telegram용 투명 PNG 스티커 생성
lumart artwork.png -m --transparent -o manga_sticker.png

# 순수 펜 드로잉 건축 스케치
lumart building.jpg -s -w 120

# Bayer 패턴 디더링 레트로 포스터
lumart poster.jpg -m -d bayer -w 100
```

### 4. 터미널 실시간 웹캠 스트리밍 (Spectra Weep 1.4)
```bash
# 기본 웹캠으로 실시간 셰이더 스트리밍
lumart -W

# 보조 외장 웹캠(ID: 1) 스트리밍
lumart -W 1
```

### 5. 웹 URL, 클립보드 및 Unix 파이프라인
```bash
# HTTPS URL에서 직접 다운로드하여 렌더링
lumart https://example.com/art.png -w 80

# 현재 클립보드에 복사된 이미지 즉시 렌더링
lumart --paste

# curl 파이프라인 입력 받아 렌더링
curl -sL https://example.com/photo.jpg | lumart -
```

### 6. 동적 컬러 교체 (Color Swapping)
```bash
# 보라색 톤을 핫핑크(bubblegum pink)로 즉시 교체
lumart sprite.png --blocks --swap purple pink
```

---

## 엔지니어링 비밀, Pro-Tips & 터미널 철학

> *"강력한 렌더링 파워에는 위대한 미적 책임이 따른다."*

### 1. 글꼴 종횡비의 만유인력 법칙 (`--font-ratio`)
* **수학적 현실**: 일반적인 그래픽 캔버스에서 픽셀은 완벽한 정사각형($1:1$)입니다. 그러나 터미널 에뮬레이터라는 가혹한 야생에서 모든 문자 셀은 세로로 길쭉한 직사각형 모놀리스(일반적으로 $1:2$ 또는 $0.5$ 비율)입니다.
* **증상**: 렌더링된 애니메이션 캐릭터가 50톤 유압 프레스에 눌린 것처럼 납작해졌거나 웜홀을 통과한 껌처럼 길쭉하게 늘어난다면, 렌더링 엔진 탓이 아닙니다. 당신의 폰트 기하학을 점검하십시오.
* **Pro의 처방전**:
  * 슬림하고 키가 큰 폰트(커스텀 줄간격 없는 *Fira Code* 또는 *JetBrains Mono*): `--font-ratio 0.45` ~ `0.48` 권장.
  * 가로폭이 넓거나 정사각형에 가까운 모노스페이스 폰트: `--font-ratio 0.52` ~ `0.58` 권장.
  * Lumart 기본값은 `0.5`이며, 알려진 우주의 현대 터미널 에뮬레이터 중 90%를 완벽하게 만족합니다.

### 2. 암흑 캔버스의 정리 및 WebP 파문령
* **왜 TrueColor 엔진(Mary & Trumble)은 투명 스티커 출력을 극구 거부하는가?**
  * TrueColor 터미널 아트는 터미널 배경인 깊은 칠흑색 `#0c0c0c` 공간에 가산 혼합으로 빛을 방출하는 원리로 작동합니다.
  * 이 배경을 강제로 걷어내고 순백색 WhatsApp 대화창이나 투명 뷰어에 붙여넣으면 광학 대비가 완전히 무너집니다. 테두리는 톱니처럼 깨지고, 캐릭터는 토너 공장 폭발 사고로 흩날린 디지털 꽃가루처럼 변합니다.
  * **Luris Mono가 선택받은 자인 이유**: 순수 블랙 잉크, 하프톤 스크린톤(*Ami-tone*), DoG 벡터 외곽선만 다루는 Luris는 92.9% 이상의 검증된 알파 투명도를 자랑하는 진짜 스티커를 만들어 Telegram, Discord, Slack에서 극상의 시각미를 선사합니다.
* **WebP의 비극**:
  * 수개월 동안 표준 데스크톱 뷰어들은 터미널 래스터화된 `.webp` 파일을 제대로 처리하지 못해 선명한 ANSI 아트를 흐릿한 진흙탕으로 뭉개버렸습니다. v2.4.0에서 `.webp`는 어둠의 세계로 공식 파문되었습니다. **삼위일체** 만세: `.png`(무손실 초고해상도 및 스티커), `.jpg`(95% 압축 사진), `.gif`(멀티프레임 애니메이션).

### 3. Oklab 결투: 왜 Mary는 700나노초 만에 31가지 조합을 평가하는가
* 표준 RGB 유클리드 공간에서 피타고라스 정리($\sqrt{\Delta R^2 + \Delta G^2 + \Delta B^2}$)로 색상 거리를 계산하는 것은 생물학적 망상입니다. 인간의 망막은 녹색의 미세한 밝기 변화에는 극도로 예민하지만, 어두운 파란색의 섬세한 차이에는 거의 눈이 멀어 있습니다.
* Mary Apex는 모든 서브픽셀을 인지 색공간 **Oklab**($L, a, b$)으로 투영하고 C++17 OpenMP SIMD 벡터화를 통해 **셀당 가능한 모든 31가지 색상 분할 조합**을 철저하게 전수 조사합니다.
* 터미널을 위해 왜 이토록 많은 연산력을 쏟아붓는가? CPU 사이클은 저렴하지만, 흉물스러운 터미널 아트는 미학적 중범죄이기 때문입니다.

### 4. Trumble Orelx & 1990년대 아케이드 셀 셰이딩의 황금률
* 전통적인 이미지 다운샘플링 알고리즘(Lanczos, Bicubic 등)은 이웃 픽셀을 평균화합니다. 그 결과 1픽셀짜리 날카로운 검은 잉크 외곽선이 3픽셀짜리 비겁한 회색 안개로 번져버립니다.
* Trumble Orelx는 우주의 질서를 뒤집습니다. 이미지를 목표 셀 해상도로 *먼저* 축소한 뒤, **터미널 실제 서브픽셀 해상도 위에서 Canny 에지 검출을 실행**합니다.
* 그 결과 캐릭터의 머리카락, 눈동자 윤곽선, 옷주름이 **정확히 1서브픽셀 두께의 칠흑빛 잉크**로 면도날처럼 날카롭게 유지되며, 1996년 캡콤 CPS-2 아케이드 기판의 묵직하고 생동감 넘치는 펀치력을 그대로 재현합니다.

### 5. 뷰포트 맞춤의 신성한 계명 (`-F` vs `-w`)
* **제1계명**: 마우스 휠을 참치잡이 릴처럼 감아올릴 필요 없이 화면에 맞춤 정장처럼 딱 맞추고 싶다면 `-F` (`--fit`)를 사용하라.
* **제2계명**: *Fastfetch*의 60열 고정 사이드바나 상태 대시보드에 임베딩할 때는 `-w 60 --fastfetch`를 사용하라.
* **제3계명**: 절대 `lumart image.png -F -w 80`을 실행하지 마라. Lumart에게 동적 뷰포트 높이를 계산하면서 동시에 고정 너비를 지키라고 요구하는 것은 아리스토텔레스 논리학에 대한 모독이다. Lumart는 정중한 `Exit Code 2`와 친절한 설명을 남기고 종료할 것이다.

### 6. `animate` 명령어의 미스터리
* 만약 당신이 `animate` 명령어를 찾으며 왜 `--loop`를 사용하는지 의아해한다면: 원작자는 `animate`라는 이름을 현재 준비 중인 고차원 극비 프로젝트를 위해 아껴두었습니다. 당신의 터미널이 아직 렌더링할 수 없는 답에 대해 묻지 마십시오. `--loop`를 사용하여 부드러운 60 FPS의 쾌락을 즐기십시오.

---

## 업데이트 및 롤백 시스템

Lumart는 CLI 내부에서 완전한 라이프사이클 관리를 제공합니다:

* **업데이트 확인 (`lumart -u`)**:
  로컬 파일을 수정하지 않고 GitHub Releases API를 안전하게 조회합니다.
* **자동 업그레이드 (`lumart -uu`)**:
  최신 릴리스를 다운로드하고, 네이티브 C++ 공유 라이브러리를 재빌드하며, `~/.config/luma/backup/`에 자동 백업을 생성합니다.
* **즉각적 롤백 / 다운그레이드 (`lumart -dg`)**:
  대화형 메뉴를 통해 이전 버전이나 로컬 백업으로 즉시 되돌리거나, 대상 버전을 직접 지정할 수 있습니다:
  ```bash
  lumart -dg 2.2.0
  ```

---

## 운영체제 및 데스크톱 연동

### 1. 파일 관리자 우클릭 메뉴 연동
최초 1회 실행:
```bash
lumart --install-desktop
```
`.desktop` 파일 및 우클릭 액션을 등록하여 다음 파일 관리자에서 **이미지 파일을 우클릭**하여 즉시 열 수 있습니다:
* **GNOME Files (Nautilus)**
* **KDE Dolphin**
* **Cinnamon Nemo**
* **XFCE Thunar**

"Lumart로 열기"를 선택하면 고해상도 터미널 창이 뜨며 이미지가 즉시 렌더링됩니다.

### 2. 환경 진단 도구 (`lumart -v`)
TrueColor(24비트) 지원 여부, C++ OpenMP 컴파일러 유무, 활성화된 공유 라이브러리(`libmary.so`, `libmonochrome.so`), 터미널 크기 및 설정 경로를 즉시 진단합니다.

---

## 내부 아키텍처 및 수학 원리

### 1. 지각적 Oklab 색공간 및 이산 조합 최적화
기존 터미널 도구들은 비선형 sRGB 공간에서 색상 거리를 계산하므로 중간 톤이 탁해지고 색조가 왜곡됩니다. Mary Apex 3.5는 sRGB를 선형 RGB로 변환한 뒤 **Oklab**($L, a, b$) 공간으로 사상합니다:

$$\Delta E = \sqrt{(L_1 - L_2)^2 + (a_1 - a_2)^2 + (b_1 - b_2)^2}$$

각 섹스턴트 셀($2 \times 3 = 6$ 서브픽셀)에서 전경색과 배경색으로 나뉘는 비자명 분할 수는 정확히 $2^5 - 1 = 31$개입니다. Mary는 이 31가지 경우를 직접 전수 평가하여 확률적 노이즈가 전혀 없는 수학적 최적해를 보장합니다.

### 2. Trumble의 1-to-1 사전 스케일 인킹
고해상도 에지 맵을 Lanczos 등으로 축소하면 1픽셀짜리 미세한 선이 배경에 흡수되어 사라집니다. Trumble Orelx는 Canny 그래디언트를 계산하기 *전에* 이미지를 셀의 정확한 서브픽셀 해상도($target\_width \times 2$)로 리사이즈하여 외곽선이 완벽한 1서브픽셀 굵기를 유지하도록 합니다.

### 3. ECMA-48 ANSI 이스케이프 시퀀스 압축기
Lumart는 현재 터미널 스타일링 상태(`current_fg`, `current_bg`)를 추적합니다. 동일한 색상을 가진 인접 셀에 대한 중복 색상 코드를 생략하여 ANSI 출력 페이로드를 최대 **45%** 줄이고 SSH 원격 렌더링 속도를 대폭 가속합니다.

---

## 문제 해결

### 1. 색상이 물빠진 것처럼 보이거나 밴딩 현상이 발생하는 경우
* 터미널이 TrueColor(24비트)를 지원하는지 확인하십시오. 셸 설정 파일(`.bashrc` / `.zshrc`)에 추가:
  ```bash
  export COLORTERM=truecolor
  ```
* 추천 TrueColor 터미널: **Kitty**, **Alacritty**, **WezTerm**, **iTerm2**, **Foot**, **GNOME Terminal**, **Konsole**, **Windows Terminal**.

### 2. 섹스턴트(`-S`)나 점자(`-B`) 문자가 빈 네모(두부) 기호로 깨지는 경우
* 현재 폰트에 Unicode 13.0 기호가 누락되어 있습니다.
* 추천 모노스페이스 폰트:
  * **Symbols Nerd Font** / **JetBrains Mono Nerd Font**
  * **DejaVu Sans Mono**
  * **Cascadia Code**

### 3. 완전 삭제 (Uninstallation)
```bash
./uninstall.sh
# 또는 패키지 관리자 사용 시:
sudo apt remove lumart     # Debian/Ubuntu
sudo dnf remove lumart     # Fedora
sudo pacman -Rns lumart    # Arch Linux
```

---

## 라이선스

Lumart는 GNU Affero General Public License v3.0 (**AGPL-3.0**)에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 확인하세요.
