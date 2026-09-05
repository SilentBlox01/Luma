[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

# Luma

**Um motor de renderização de imagem para terminal de alta fidelidade escrito em Python e C/C++ moderno.**

O Luma é um motor de renderização de terminal de código aberto focado em um único objetivo:

> **Máxima fidelidade visual com o mínimo de espaço no terminal.**

Ao contrário dos conversores ASCII tradicionais que simplesmente mapeiam o brilho da imagem para caracteres, o Luma explora diferentes sistemas de glifos de terminal, matemática de cores RGB Linear e algoritmos nativos de visão computacional em C/C++ para preservar a maior quantidade de informações visuais possível dentro de um número limitado de células do terminal.

## Recursos

* Renderização de imagens de alta fidelidade no terminal
* Renderização baseada em ASCII, Braille e Blocos
* **Arquitetura Híbrida de Motor Duplo**:
  * **Motor de Cores RGB Linear** (Python / Pillow): Curvas de contraste HDR dinâmicas, mistura em espaço de cor linear ($C_{\text{linear}} = C_{\text{srgb}}^{2.2}$) e TrueColor ANSI de 24 bits.
  * **Motor Monocromático e Manga de Alto Desempenho** (C++17 Nativo): Execução sub-10ms, extração de contornos por Diferença de Gaussianas (DoG), difusão de erro Bill Atkinson (1984, MacPaint) e retículas de meio-tom Bayer 8x8 (*Ami-tone*).
* **Seletor de Motor (`-E`, `--engine`)**: Alterne dinamicamente entre `color`, `mono`, `bw`, `manga` e `sketch`.
* **Modo Esboço de Traço Puro (`-s`, `-E sketch`)**: Extração de contornos nítidos sem ruído para anime e ilustrações.
* **Manga Screentone 2.0 (`-m`, `-E manga`)**: Retículas autênticas de impressão de mangá para tons médios com brancos de papel puros e tinta preta sólida.
* **Pontilhado Atkinson e Halftone (`-d` / `--dither`)**: Suporta `atkinson`, `floyd`, `bayer` e `none`.
* **Blocos Quadrantes HD 2x2 (`--blocks`)**: 4 subpixels por célula usando caracteres de quadrante Unicode (`▘▝▀▖▌▞▛▗▚▐▜▄▙▟█`).
* **Renderização Estilo OS (`--os-style`)**: Caracteres clássicos de terminal (pontos, letras) para logotipos estilo Neofetch.
* **Troca de Cor em Tempo Real (`--swap`)**: Troque dinamicamente até 5 cores com base na distância de cor Euclidiana em 3D.
* **Zero Dependências Nativas Externas**: O motor C++ é autocontido com cabeçalhos de domínio público (`stb_image.h` e `stb_image_resize2.h`). Não requer OpenCV nem libpng.
* **Paridade Total com Fallback em Python**: Se o compilador C++ não estiver disponível, o Luma utiliza uma implementação equivalente em Python puro sem quebras.
* Largura de saída configurável e autodetecção de fundo claro/escuro (`-i`, `--invert`)
* Suíte interativa de atualização (`-uu`), restauração/downgrade (`-dg`) e verificação (`-u`)
* Painel de diagnóstico integral do sistema e motores (`-v`, `--version`)

## Exemplo

```bash
# Converta uma imagem usando caracteres Braille, cores, e trocando roxo por rosa
luma image.png -w 45 --braille -c --swap purple pink
```

## Instalação

Você pode instalar o Luma com um único comando, executá-lo diretamente do código fonte ou compilá-lo em um pacote nativo do Linux (DEB, RPM ou Arch PKGBUILD).

**Instalação Rápida (Recomendado):**
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

**Opção 1: Executar diretamente do código fonte / Instalador local**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
./install.sh
```

**Opção 2: Baixar Pacotes Pré-compilados**
Você pode baixar os pacotes `.deb` ou `.rpm` prontos para uso diretamente da página de [GitHub Releases](https://github.com/SilentBlox01/Luma/releases).

**Opção 3: Compilar e construir pacotes nativos você mesmo**
O Luma inclui um script de construção automatizado para empacotar a ferramenta em um binário autônomo usando o PyInstaller:
```bash
chmod +x build_packages.sh
./build_packages.sh
```
Após compilar, você pode instalá-lo globalmente através do seu gerenciador de pacotes:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-*.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-*.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

**Opção 4: Compilação manual do motor nativo C++**
Se deseja compilar apenas o motor nativo em C++ sem gerar pacotes completos:
```bash
# Binário CLI independente:
g++ -O3 -std=c++17 monochrome.cpp -o luma-mono

# Biblioteca compartilhada (para aceleração em processo via ctypes a partir do Python):
g++ -O3 -std=c++17 -fPIC -shared monochrome.cpp -o libmonochrome.so
```

## Uso

Se você instalou o pacote ou executou o instalador, pode executar `lumart` ou `luma` de qualquer lugar. Caso contrário, execute o script python diretamente.

> **💡 Dica Pro:** O Luma funciona perfeitamente com imagens sem fundo (transparentes)! O motor ignora automaticamente os pixels transparentes, fazendo com que logotipos e personagens se destaquem contra o fundo do seu terminal.

```bash
# Uso básico
python3 lumart.py image.png
```

Especificar a largura de saída (em caracteres):
```bash
python3 lumart.py image.png -w 30
```

Habilitar renderização Braille de alta fidelidade com Truecolor:
```bash
python3 lumart.py image.png --braille -c
```

Renderizar no Modo Esboço de Traço Puro (contornos nítidos DoG sem ruído):
```bash
python3 lumart.py image.png -E sketch -w 100
# ou: python3 lumart.py image.png -s -w 100
```

Renderizar com o motor Manga Screentone 2.0 (tinta DoG + retícula Bayer 8x8):
```bash
python3 lumart.py image.png -E manga -w 120
# ou: python3 lumart.py image.png -m -w 120
```

Renderizar em monocromático com Pontilhado Atkinson (MacPaint 1984):
```bash
python3 lumart.py image.png -E mono -d atkinson -w 100
# ou floyd-steinberg clássico: python3 lumart.py image.png -E mono -d floyd -w 100
```

Renderizar em Blocos Quadrantes HD (2x2 subpixels por célula em P&B):
```bash
python3 lumart.py image.png -E mono --blocks -w 80
```

Renderizar em monocromático puro sem cores:
```bash
python3 lumart.py image.png -E mono --braille -w 100
```

Forçar renderização clássica de caracteres estilo OS retro (útil para logotipos de SO):
```bash
python3 lumart.py image.png --os-style -c
```

Exibir Diagnóstico Completo do Sistema e Motores:
```bash
luma -v
# ou: luma --version
```

## Atualizações e Rollback

O Luma oferece controle explícito sobre atualizações e restaurações:

- **Verificar se há atualizações (sem baixar nada):**
  ```bash
  luma -u
  # ou: luma --update / luma --check-update
  ```
- **Atualização Interativa:**
  ```bash
  luma -uu
  # ou: luma --upgrade
  ```
  *(Permite selecionar qual versão instalar com pré-visualização de notas e backup automático em `~/.config/luma/backup/`)*

- **Restauração Interativa / Downgrade:**
  ```bash
  luma -dg
  # ou: luma --downgrade / luma --rollback
  ```
  *(Abre um menu interativo no terminal para escolher entre backups locais ou releases do GitHub)*

  Você também pode passar a versão diretamente:
  ```bash
  luma -dg 2.1.0
  ```

## Desinstalação

Se você deseja remover o Luma do seu sistema, o comando depende de como você o instalou:

**Se instalado via Gerenciador de Pacotes (.deb, .rpm, PKGBUILD):**
- **Debian/Ubuntu**: `sudo apt remove lumart`
- **Fedora/RHEL**: `sudo dnf remove lumart`
- **Arch Linux**: `sudo pacman -Rns lumart`

**Se instalado via pip:**
```bash
pip uninstall lumart
```

**Se instalado manualmente:**
Você pode executar o script de desinstalação fornecido:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## Filosofia

Renderização de terminal é uma forma de compressão visual.

O desafio não é simplesmente converter uma imagem em caracteres. O desafio é representar a maior quantidade de informações visuais possível usando o menor número de células do terminal.

Portanto, o Luma foca na **fidelidade perceptiva**, utilizando espaços de cores matematicamente precisos (RGB Linear vs sRGB) e curvas HDR dinâmicas, em vez de simplesmente produzir arte ASCII reconhecível.

## Solução de Problemas

Com problemas em fontes, cores ou módulos ausentes? Confira nosso [Guia de Solução de Problemas](TROUBLESHOOTING.md) para correções rápidas.
