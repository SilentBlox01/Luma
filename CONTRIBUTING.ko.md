[English](CONTRIBUTING.md) | [Español](CONTRIBUTING.es.md) | [Português](CONTRIBUTING.pt.md) | [Русский](CONTRIBUTING.ru.md) | [日本語](CONTRIBUTING.ja.md) | [Deutsch](CONTRIBUTING.de.md) | [한국어](CONTRIBUTING.ko.md)

# Luma 기여 가이드

Luma 개선에 관심을 가져주셔서 감사합니다! 이 프로젝트는 터미널 그래픽의 한계를 넓히는 것을 목표로 하며, 모든 기여를 진심으로 환영합니다.

## 🐛 버그 신고 및 기능 제안

버그를 발견했거나 새로운 아이디어(새로운 렌더링 알고리즘, 디더링 패턴, 애니메이션 지원 등)가 있다면 GitHub **Issue**를 등록해 주세요. 다음 내용을 포함해 주시면 도움이 됩니다:
- 운영체제 및 터미널 에뮬레이터 (예: Fedora + Alacritty, Ubuntu + Kitty, Windows Terminal).
- 문제를 발생시킨 정확한 명령어 및 인자.
- 가능한 경우, 생성된 ASCII 아트 또는 원본 이미지.

## 🛠️ 코드로 기여하기

1. GitHub에서 저장소를 **Fork**합니다.
2. 새 기능 또는 버그 수정을 위한 **브랜치를 생성**합니다 (`git checkout -b feature/awesome-new-engine`).
3. 코드를 작성하고 **테스트**합니다. 엔진의 핵심 로직은 `lumart.py`에 있습니다.
4. 명확한 메시지로 변경사항을 **커밋**합니다 (`git commit -m 'feat: 새로운 디더링 기능 추가'`).
5. 브랜치에 **푸시**합니다 (`git push origin feature/awesome-new-engine`).
6. **Pull Request**를 생성합니다.

### 프로젝트 구조
- `lumart.py`: 엔진 핵심 전체: 선형 RGB 기반 색상 혼합, Bayer 디더링, 점자/하프 블록 렌더링 및 다국어 지원 CLI.
- `install.sh`: Fedora, Debian/Ubuntu, Arch Linux, openSUSE, macOS와 호환되는 유니버설 Plug & Play 설치 스크립트.
- `build_packages.sh`: `PyInstaller` 독립 바이너리, `.deb`, `.rpm`, `PKGBUILD` 패키지 자동 빌드 스크립트.
- `pyproject.toml`: `pipx install .` 및 `pip install --user .`를 지원하는 패키징 설정.

### 개발 가이드라인
- **무거운 종속성 금지**: Luma는 가볍고 즉시 실행(Plug & Play) 가능해야 합니다. Pillow(`PIL`)와 표준 라이브러리만 사용합니다.
- **터미널 시각적 완성도**: 모든 모드는 터미널에서의 최고 수준의 시각적 품질을 최우선으로 합니다.
- **다국어 지원**: 새로운 CLI 옵션이나 메시지를 추가할 때는 `TRANSLATIONS`의 7개 언어(`en`, `es`, `pt`, `ru`, `ja`, `de`, `ko`)를 모두 업데이트해 주세요.

터미널 그래픽의 세계를 즐겨보세요! 🎨
