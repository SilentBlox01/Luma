[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**Python으로 작성된 고충실도 이미지-터미널 렌더링 엔진.**

Luma는 단 하나의 목표에 집중하는 오픈 소스 터미널 렌더링 엔진입니다.

> **최소한의 터미널 공간에서 최대의 시각적 충실도를 구현합니다.**

이미지 밝기를 단순히 문자에 매핑하는 기존의 ASCII 변환기와 달리, Luma는 다양한 터미널 글리프 시스템, 선형 RGB 색상 연산 및 렌더링 기술을 탐구하여 제한된 수의 터미널 셀 내에서 가능한 한 많은 시각적 정보를 보존합니다.

## 기능

* 터미널에서의 고충실도 이미지 렌더링
* ASCII, 점자 및 블록 기반 렌더링
* **OS 스타일 렌더링 (`--os-style`)**: Neofetch 스타일 로고를 위한 클래식 터미널 문자(점, 문자).
* **실시간 색상 교환 (`--swap`)**: 3D 유클리드 색상 거리를 기반으로 최대 5개의 색상을 동적으로 교환합니다.
* **에픽 컬러 엔진(기본값)**: 선형 RGB 공간에서 색상을 평균화하여 탁한 출력을 방지하는 동시에 동적 대비 및 채도(HDR)를 적용합니다.
* 구성 가능한 출력 너비
* 트루컬러 터미널 지원(24비트 ANSI)
* 극도로 작은 출력 크기를 위해 설계됨
* Python 기반이며 확장성이 뛰어남

## 예시

```bash
# 점자 문자, 색상을 사용하여 이미지를 변환하고 보라색을 분홍색으로 바꿉니다.
luma image.png -w 45 --braille -c --swap purple pink
```

## 설치

Luma를 소스에서 직접 실행하거나 네이티브 Linux 패키지(DEB, RPM 또는 Arch PKGBUILD)로 빌드할 수 있습니다.

**옵션 1: 컴파일된 패키지 다운로드(권장)**
[GitHub Releases](https://github.com/SilentBlox01/Luma/releases) 페이지에서 직접 사용할 수 있는 `.deb` 또는 `.rpm` 패키지를 다운로드할 수 있습니다.

**옵션 2: 소스에서 직접 실행**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
# Pillow가 설치되어 있는지 확인하세요
pip install -r requirements.txt
python3 lumart.py --help
```

**옵션 3: 네이티브 패키지 직접 컴파일 및 빌드**
Luma에는 도구를 독립형 바이너리로 패키징하기 위해 PyInstaller를 사용하는 자동 빌드 스크립트가 포함되어 있습니다.
```bash
chmod +x build_packages.sh
./build_packages.sh
```
컴파일 후 패키지 관리자를 사용하여 전역으로 설치할 수 있습니다.
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-2.0.0.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-2.0.0.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

## 사용법

패키지를 설치한 경우 어디서나 `lumart` 또는 `luma`를 실행할 수 있습니다. 그렇지 않으면 python 스크립트를 직접 실행합니다.

> **💡 꿀팁:** Luma는 배경이 투명한 이미지에서 가장 잘 작동합니다! 엔진이 투명 픽셀을 자동으로 무시하므로 로고와 캐릭터가 터미널 배경과 완벽하게 조화를 이룹니다.

```bash
# 기본 사용법
python3 lumart.py image.png
```

출력 너비(문자 수) 지정:
```bash
python3 lumart.py image.png -w 30
```

트루컬러가 포함된 고충실도 점자 렌더링 활성화:
```bash
python3 lumart.py image.png --braille -c
```

레트로 OS 스타일 문자 렌더링 강제 적용(OS 로고에 유용함):
```bash
python3 lumart.py image.png --os-style -c
```

## 제거

시스템에서 Luma를 제거하려는 경우 명령은 설치 방법에 따라 다릅니다.

**패키지 관리자를 통해 설치한 경우(.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**pip를 통해 설치한 경우:**
```bash
pip uninstall lumart
```

**수동으로 설치한 경우:**
제공된 제거 스크립트를 실행할 수 있습니다.
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## 철학

터미널 렌더링은 시각적 압축의 한 형태입니다.

단순히 이미지를 문자로 변환하는 것이 과제가 아닙니다. 최소한의 터미널 셀을 사용하여 가능한 한 많은 시각적 정보를 표현하는 것이 과제입니다.

따라서 Luma는 단순히 알아볼 수 있는 ASCII 아트를 생성하는 대신 수학적으로 정밀한 색 공간(선형 RGB vs sRGB)과 동적 HDR 곡선을 사용하여 **지각적 충실도**에 중점을 둡니다.

## 문제 해결

글꼴, 색상 또는 누락된 모듈에 문제가 있습니까? 일반적인 문제에 대한 빠른 해결 방법은 [문제 해결 가이드](TROUBLESHOOTING.md)를 확인하세요.

## 기여

Luma는 오픈 소스 프로젝트이며 기여를 환영합니다.

렌더링 알고리즘, 최적화, 글리프 시스템, 벤치마크 또는 개선에 대한 아이디어가 있으면 언제든지 이슈를 열거나 풀 리퀘스트를 보내주세요. (자세한 내용은 `CONTRIBUTING.md`를 참조하세요).

## 라이선스

Luma는 GNU Affero General Public License v3.0 (AGPL-3.0)에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.
