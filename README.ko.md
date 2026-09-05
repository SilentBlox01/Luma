[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**Python 및 최신 C/C++로 작성된 고충실도 이미지-터미널 렌더링 엔진.**

Luma는 단 하나의 목표에 집중하는 오픈 소스 터미널 렌더링 엔진입니다:

> **최소한의 터미널 공간에서 최대의 시각적 충실도를 구현합니다.**

이미지 밝기를 단순히 문자에 매핑하는 기존의 ASCII 변환기와 달리, Luma는 다양한 터미널 글리프 시스템, 선형 RGB 색상 연산 및 네이티브 C/C++ 컴퓨터 비전 알고리즘을 활용하여 제한된 수의 터미널 셀 내에서 가능한 한 많은 시각적 정보를 보존합니다.

## 기능

* 터미널에서의 고충실도 이미지 렌더링
* ASCII, 점자 및 블록 기반 렌더링
* **하이브리드 듀얼 엔진 아키텍처**:
  * **선형 RGB 컬러 엔진** (Python / Pillow): 동적 HDR 대비 곡선, 선형 색 공간 블렌딩 ($C_{\text{linear}} = C_{\text{srgb}}^{2.2}$), 24비트 ANSI 트루컬러.
  * **고성능 흑백 및 망가 엔진** (네이티브 C++17): 10ms 미만의 초고속 연산, 가우시안 차분법 (DoG) 윤곽선 추출, Bill Atkinson 오차 확산 (1984년 MacPaint), 8x8 Bayer 스크린톤 (*Ami-tone*).
* **엔진 선택기 (`-E`, `--engine`)**: `color`, `mono`, `bw`, `manga`, `sketch` 모드를 동적으로 전환.
* **순수 선화 스케치 모드 (`-s`, `-E sketch`)**: 애니메이션 및 일러스트를 위한 노이즈 없는 깔끔한 윤곽선 추출.
* **망가 스크린톤 2.0 (`-m`, `-E manga`)**: 깨끗한 흰색 용지와 깊은 검은색 잉크, 중간 톤을 위한 전통적인 8x8 망점 스크린톤.
* **Atkinson 및 하프톤 디더링 (`-d` / `--dither`)**: `atkinson`, `floyd`, `bayer`, `none` 지원.
* **2x2 4분면 HD 블록 (`--blocks`)**: 유니코드 4분면 블록 문자 (`▘▝▀▖▌▞▛▗▚▐▜▄▙▟█`)를 사용한 셀당 4개 서브픽셀 렌더링.
* **OS 스타일 렌더링 (`--os-style`)**: Neofetch 스타일 로고를 위한 클래식 터미널 문자(점, 문자).
* **실시간 색상 교환 (`--swap`)**: 3D 유클리드 색상 거리를 기반으로 최대 5개의 색상을 동적으로 교환.
* **외부 네이티브 종속성 없음**: 퍼블릭 도메인 단일 파일 헤더 (`stb_image.h` 및 `stb_image_resize2.h`)로 자체 완결. OpenCV나 libpng가 필요하지 않습니다.
* **완벽한 Python 폴백 호환성**: C++ 컴파일러가 없는 환경에서도 순수 Python 구현체로 원활하게 전환됩니다.
* 터미널 너비 설정 및 밝은/어두운 터미널 배경 자동 감지 (`-i`, `--invert`)
* 대화형 업그레이드 (`-uu`), 롤백 (`-dg`), 업데이트 확인 (`-u`) 제품군
* 포괄적인 시스템 및 엔진 진단 (`-v`, `--version`)

## 예시

```bash
# 점자 문자, 색상을 사용하여 이미지를 변환하고 보라색을 분홍색으로 바꿉니다.
luma image.png -w 45 --braille -c --swap purple pink
```

## 설치

Luma는 단일 명령으로 설치하거나, 소스에서 직접 실행하거나, 네이티브 Linux 패키지(DEB, RPM 또는 Arch PKGBUILD)로 빌드할 수 있습니다.

**빠른 설치(권장):**
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

**옵션 1: 소스에서 직접 실행 / 로컬 설치 프로그램**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
./install.sh
```

**옵션 2: 빌드된 패키지 다운로드**
[GitHub Releases](https://github.com/SilentBlox01/Luma/releases) 페이지에서 직접 사용할 수 있는 `.deb` 또는 `.rpm` 패키지를 다운로드할 수 있습니다.

**옵션 3: 네이티브 패키지 직접 컴파일 및 빌드**
Luma에는 도구를 독립형 바이너리로 패키징하기 위해 PyInstaller를 사용하는 자동 빌드 스크립트가 포함되어 있습니다:
```bash
chmod +x build_packages.sh
./build_packages.sh
```
컴파일 후 패키지 관리자를 사용하여 전역으로 설치할 수 있습니다:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-*.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-*.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

**옵션 4: 네이티브 C++ 엔진 수동 컴파일**
전체 패키지 없이 네이티브 C++ 엔진만 컴파일하려는 경우:
```bash
# 독립형 CLI 바이너리:
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono

# 공유 라이브러리 (Python ctypes 인프로세스 가속):
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
```

## 사용법

패키지를 설치했거나 설치 스크립트를 사용한 경우 어디서나 `lumart` 또는 `luma`를 실행할 수 있습니다. 그렇지 않은 경우 Python 스크립트를 직접 실행하세요.

> **💡 유용한 팁:** Luma는 투명 배경 이미지와 완벽하게 작동합니다! 투명 픽셀을 자동으로 무시하므로 로고와 캐릭터가 터미널 배경 위에서 완벽하게 돋보입니다.

```bash
# 기본 사용법
python3 lumart.py image.png
```

출력 너비 지정 (문자 단위):
```bash
python3 lumart.py image.png -w 30
```

트루컬러 지원 점자 렌더링 활성화:
```bash
python3 lumart.py image.png --braille -c
```

순수 선화 스케치 모드 (깔끔한 DoG 윤곽선):
```bash
python3 lumart.py image.png -E sketch -w 100
# 또는: python3 lumart.py image.png -s -w 100
```

망가 스크린톤 2.0 모드 (DoG 외곽선 + 8x8 Bayer 스크린톤):
```bash
python3 lumart.py image.png -E manga -w 120
# 또는: python3 lumart.py image.png -m -w 120
```

Atkinson 디더링을 사용한 흑백 렌더링 (1984 MacPaint):
```bash
python3 lumart.py image.png -E mono -d atkinson -w 100
# 또는 클래식 Floyd-Steinberg: python3 lumart.py image.png -E mono -d floyd -w 100
```

2x2 4분면 HD 블록:
```bash
python3 lumart.py image.png -E mono --blocks -w 80
```

순수 흑백 모노크롬:
```bash
python3 lumart.py image.png -E mono --braille -w 100
```

클래식 OS 스타일 렌더링:
```bash
python3 lumart.py image.png --os-style -c
```

전체 시스템 및 엔진 진단 표시:
```bash
luma -v
# 또는: luma --version
```

## 업데이트 및 롤백

Luma는 업데이트와 복원을 사용자가 명시적으로 제어할 수 있도록 지원합니다:

- **업데이트 확인 (다운로드나 변경 사항 없음):**
  ```bash
  luma -u
  # 또는: luma --update / luma --check-update
  ```
- **대화형 업그레이드:**
  ```bash
  luma -uu
  # 또는: luma --upgrade
  ```
  *(릴리스 노트를 확인하고 버전을 선택할 수 있으며, `~/.config/luma/backup/`에 자동 백업 생성)*

- **대화형 롤백 / 다운그레이드:**
  ```bash
  luma -dg
  # 또는: luma --downgrade / luma --rollback
  ```
  *(로컬 백업 또는 GitHub 릴리스 중에서 선택하여 복원)*

  특정 버전을 직접 지정할 수도 있습니다:
  ```bash
  luma -dg 2.1.0
  ```

## 제거

시스템에서 Luma를 제거하려는 경우:

**패키지 관리자를 통해 설치한 경우 (.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**pip를 통해 설치한 경우:**
```bash
pip uninstall lumart
```

**수동으로 설치한 경우:**
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## 철학

터미널 렌더링은 시각적 압축의 한 형태입니다.

단순히 이미지를 문자로 변환하는 것이 문제가 아닙니다. 최소한의 터미널 셀을 사용하여 가능한 한 많은 시각적 정보를 표현하는 것이 과제입니다.

따라서 Luma는 단순히 알아볼 수 있는 ASCII 아트를 생성하는 대신, 수학적으로 정밀한 색 공간(선형 RGB vs sRGB)과 동적 HDR 곡선을 사용하는 **지각적 충실도**에 중점을 둡니다.

## 문제 해결

글꼴, 색상 또는 누락된 모듈에 문제가 있나요? 빠른 해결 방법은 [문제 해결 가이드](TROUBLESHOOTING.md)를 확인하세요.
