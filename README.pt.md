[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md) | [한국어](README.ko.md)

```
  ██╗     ██╗   ██╗███╗   ███╗ █████╗ ██████╗ ████████╗
  ██║     ██║   ██║████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ██║     ██║   ██║██╔████╔██║███████║██████╔╝   ██║   
  ██║     ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
   Modern Terminal Visual Suite • v2.5.0 (Apex Nova)
   [ Mary Apex 3.5 • Trumble Orelx 2.2 • Luris Mono 2.6 • Spectra Weep 1.4 ]
```

# Lumart (Luma) v2.5.0

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Language: Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![C++: 17 Multi-Core](https://img.shields.io/badge/C%2B%2B-17%20OpenMP%20SIMD-orange.svg)](https://isocpp.org/)
[![Platform: Linux / macOS / BSD](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20BSD-lightgrey.svg)](https://github.com/SilentBlox01/Luma)
[![8 Idiomas Suportados](https://img.shields.io/badge/Idiomas-8%20Locales-purple.svg)](#idiomas-suportados)

**Lumart** é uma suíte visual de alta engenharia para terminais modernos, concebida com um único princípio fundamental:

> **Máxima densidade visual e impacto estético no menor espaço de terminal.**

Ao contrário dos conversores ASCII convencionais que apenas mapeiam o brilho de pixels para caracteres alfanuméricos, o Lumart integra **quatro motores especializados de visão computacional e renderização subpixel** desenvolvidos em C++17 nativo multi-core (OpenMP) e Python otimizado. Ele transforma qualquer fotografia, ilustração de anime, sprite de jogo arcade ou transmissão de webcam ao vivo em uma experiência gráfica imersiva no seu emulador de terminal.

---

## Índice
1. [Os Quatro Motores Principais](#os-quatro-motores-principais)
   - [Mary Apex 3.5](#1-mary-apex-35-fotorrealista-vetorial)
   - [Trumble Orelx 2.2](#2-trumble-orelx-22-retro-arcade--anime-cel-shading)
   - [Luris Mono 2.6](#3-luris-mono-26-manga-screentone--monocromático)
   - [Spectra Weep 1.4](#4-spectra-weep-14-webcam-ao-vivo)
2. [Matriz Comparativa de Motores](#matriz-comparativa-de-motores)
3. [Galeria Visual e Demonstração de Resultados](#galeria-visual-e-demonstração-de-resultados)
4. [Exportação Gráfica, Animações e Política de Stickers](#exportação-gráfica-animações-e-política-de-stickers)
5. [Idiomas Suportados (8 Idiomas)](#idiomas-suportados)
6. [Instalação](#instalação)
7. [Referência Completa de Comandos (CLI)](#referência-completa-de-comandos-cli)
8. [Exemplos Práticos e Cookbook](#exemplos-práticos-e-cookbook)
9. [Segredos de Engenharia, Dicas Pro e Filosofia de Terminal](#segredos-de-engenharia-dicas-pro-e-filosofia-de-terminal)
10. [Sistema de Atualizações e Rollback](#sistema-de-atualizações-e-rollback)
11. [Integração com o Sistema Operacional](#integração-com-o-sistema)
12. [Arquitetura e Engenharia Interna](#arquitetura-e-engenharia-interna)
13. [Solução de Problemas](#solução-de-problemas)
14. [Licença](#licença)

---

## Os Quatro Motores Principais

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

### 1. Mary Apex 3.5 (Fotorrealista Vetorial)
* **Objetivo**: Microdegradês contínuos, fotografias complexas, iluminação realista e retratos fiéis.
* **C++17 Multi-Core**: Acelerado com OpenMP e instruções SIMD (`libmary.so` e executável `luma-mary`).
* **Bipartição Global Oklab Exata (31 combinações por célula)**: Elimina mínimos locais de algoritmos heurísticos. Avalia exaustivamente todas as 31 bipartições de cores por célula em menos de 700 nanossegundos, garantindo o mínimo absoluto de erro perceptual ($\Delta E$).
* **Filtro Guiado Rápido $O(1)$ com Realce Especular ($L > 0.82$)**: Realça reflexos e brilhos nos olhos e superfícies lustrosas enquanto preserva gradientes naturais na pele.
* **Sextantes Unicode 2x3 por Padrão**: 6 subpixels por caractere terminal em blocos sólidos Unicode 13.0 (`🬀`-`🬻`, `█`, `▌`, `▐`). Suporta também Braille 2x4 dual-color (`-B`), Quadrantes 2x2 (`-Q`) e Meios-Blocos (`--blocks`).
* **Isolamento Alfa Rigoroso**: Áreas transparentes não contaminam as bordas do objeto, eliminando bordas escuras.
* **Exportação com Fundo de Terminal**: Imagens salvas em `.png` ou `.jpg` são geradas sobre um fundo escuro de terminal (`#0c0c0c`), preservando a estética de arte de terminal em alta fidelidade.

### 2. Trumble Orelx 2.2 (Retro-Arcade & Anime Cel-Shading)
* **Objetivo**: Ilustrações de anime, sprites de jogos, quadrinhos e pop-art retrô.
* **Contorno 1-a-1 na Resolução Subpixel**: O redimensionamento é executado *antes* do filtro bilateral e detecção de bordas Canny. Os traços pretos mantêm exatamente 1 subpixel de espessura, evitando que a redução Lanczos borre as linhas.
* **Paleta Arcade Capcom CPS-2 / SNK Neo-Geo de 32 bits**: Curva de contraste e saturação (+28% vivacidade, +15% contraste seletivo) inspirada em clássicos jogos de luta dos anos 90.
* **Penalidade de Forma Adaptativa**: Piso de `shape_penalty` reduzido para 30, permitindo que glifos diagonais (`▞`, `▚`, `▘`, `▝`) acompanhem com perfeição o contorno dos olhos, cabelos e roupas.

### 3. Luris Mono 2.6 (Manga Screentone & Monocromático C++17)
* **Objetivo**: Mangás japoneses autênticos, arte a nanquim, bicos de pena e stickers recortados.
* **Extração de Traços DoG (Diferença de Gaussianas)**: Linhas limpas sem ruído de textura, adaptando os raios de convolução à resolução do terminal.
* **Manga Screentone 2.0 (*Ami-tone*)**: Retícula pontilhada de impressão japonesa com matrizes Bayer 8x8, entregando tons médios equilibrados com brancos puros e preto absoluto.
* **Difusão de Erro Atkinson (MacPaint 1984)**: O consagrado algoritmo de Bill Atkinson que retém 25% de energia residual para criar texturas limpas e sem desordem estocástica.
* **Exclusividade de Stickers Transparentes (`--transparent`)**: Luris Mono é o **único motor autorizado a gerar stickers recortados em `.png` com fundo transparente real**, ideal para WhatsApp, Telegram e Discord.

### 4. Spectra Weep 1.4 (Webcam ao Vivo no Terminal)
* **Objetivo**: Streaming interativo em tempo real a 30-60 FPS diretamente no terminal (`lumart --webcam` ou `lumart -W`).
* **Latência Zero**: Captura otimizada via OpenCV/V4L2 com sincronização direta à taxa de atualização do emulador.
* **5 Filtros em Tempo Real**: Normal TrueColor, Weep Cyberpunk, Matrix Green Rain, Thermal FLIR Infravermelho e Manga Ink.

---

## Matriz Comparativa de Motores

| Recurso | Mary Apex 3.5 | Trumble Orelx 2.2 | Luris Mono 2.6 | Spectra Weep 1.4 |
| :--- | :--- | :--- | :--- | :--- |
| **Estilo Visual** | Fotorrealista Vetorial | Retro-Arcade / Cel-Shading | Mangá Japonês / Tinta | Vídeo ao Vivo / Webcam |
| **Linguagem Base** | C++17 OpenMP + SIMD | Python + OpenCV Otimizado | C++17 Nativo | Python + OpenCV V4L2 |
| **Espaço de Cor** | Oklab Perceptual ($\Delta E$) | 32-bit Capcom CPS-2 | Monocromático / Ami-tone | TrueColor / Shaders RGB |
| **Modo Padrão** | **Sextantes 2x3 (`-S`)** | **Quadrantes 2x2 (`--blocks`)**| **Manga 2.0 (`-m`)** | **Streaming 30-60 FPS** |
| **Densidade Subpixel**| Até 6 subpixels/célula | Até 4 subpixels/célula | Até 4 subpixels/célula | Dinâmico |
| **Contorno de Linhas** | Suave Anti-aliasing | **Canny 1-a-1 Subpixel** | **DoG Adaptativo** | Opcional (Shader Manga) |
| **Exportação Gráfica** | Fundo de Terminal (`.png`, `.jpg`)| Fundo de Terminal (`.png`, `.jpg`)| **Stickers PNG (`--transparent`)**| Captura instantânea |
| **Comando Rápido** | `-E mary -S` | `-E trumble --blocks` | `-E luris -m` | `-W` ou `--webcam` |

---

## Galeria Visual e Demonstração de Resultados

### 1. Duelo de Motores: Mary Apex 3.5 vs Trumble Orelx 2.2
![Demonstração dos Motores Lumart](assets/engine_showdown.png)

### 2. Comparação Lado a Lado: Cor Fotorrealista vs Stickers Mangá Transparentes

| Mary Apex 3.5 (TrueColor Fotorrealista) | Luris Mono 2.6 (Stickers Mangá Transparentes) |
| :---: | :---: |
| ![Cinderella Mary](assets/cinderella_mary_apex.png)<br><sub>`lumart cinderella.jpg` *(Mary Sextantes padrão)*</sub> | ![Cinderella Manga Sticker](assets/cinderella_manga_sticker.png)<br><sub>`lumart cinderella.jpg -m --transparent -o sticker.png`</sub> |
| ![Hanako Mary Boosted](assets/hanako_boosted.png)<br><sub>`lumart hanako.png --boost` *(Punch Arcade Retinex)*</sub> | ![Hanako Manga Sticker](assets/hanako_manga_sticker.png)<br><sub>`lumart hanako.png -m --transparent -o sticker.png`</sub> |
| ![Gothic Nun Mary](assets/gothic_nun_mary.png)<br><sub>`lumart gothic_nun.png`</sub> | ![Gothic Nun Manga Sticker](assets/gothic_nun_manga_sticker.png)<br><sub>`lumart gothic_nun.png -m --transparent -o sticker.png`</sub> |
| ![Slime Mary](assets/slime_mary.png)<br><sub>`lumart slime.png`</sub> | ![Slime Manga Sticker](assets/slime_manga_sticker.png)<br><sub>`lumart slime.png -m --transparent -o sticker.png`</sub> |

### 3. Densidades de Glifos Subpixel

| Sextantes 2x3 (`-S` / Padrão) | Braille 2x4 (`-B`) | Quadrantes 2x2 (`-Q`) |
| :---: | :---: | :---: |
| ![Sextantes 2x3](assets/texture_sextants.png)<br><sub>6 subpixels/célula (Gradientes contínuos)</sub> | ![Braille 2x4](assets/texture_braille.png)<br><sub>8 subpixels/célula (Pontos finos & retratos)</sub> | ![Quadrantes 2x2](assets/texture_quadrants.png)<br><sub>4 subpixels/célula (Pixel-art & arcade)</sub> |

---

## Exportação Gráfica, Animações e Política de Stickers

O Lumart conta com exportador de alta definição (`-o imagem.png`, `-o imagem.jpg` ou `-o anim.gif`) com largura padrão de estúdio de **160 colunas**.

### 1. Modo de Animação e Exportação GIF Animado (`--loop`)
![Demonstração Animada no Terminal](assets/animated_demo.gif)

O Lumart v2.4.0 introduz suporte nativo a arquivos de animação (GIFs e APNGs):
* **Reprodução Fluida no Terminal**: `lumart animacao.gif --loop` pré-computa e armazena em cache cada quadro em sequências ANSI para reprodução suave a 60 FPS no seu terminal.
* **Compilação para GIF Animado**: `lumart animacao.gif --loop -o resultado.gif` (ou `--save resultado.gif`) renderiza cada quadro em alta precisão subpixel gerando um GIF animado completo.

### 2. Desativação Permanente do Formato WebP
* **O formato `.webp` foi desativado permanentemente para exportação gráfica**.
* Caso seja especificado um arquivo com extensão `.webp`, o Lumart encerra a operação com aviso informativo solicitando `.png`, `.jpg` ou `.gif`.
* Formatos suportados:
  * **`.png`**: Alta definição sem perdas, compressão otimizada e suporte a canal alfa transparente.
  * **`.jpg` / `.jpeg`**: Máxima compatibilidade, qualidade 95% e tabelas Huffman otimizadas.
  * **`.gif`**: Animações multiquadro para web ou terminal.

### 3. Stickers Transparentes Exclusivos do Luris Mono
* **Por que os motores a cores não fazem stickers transparentes?**
  Ao recortar um personagem colorido com 160 colunas em fundo transparente, visualizadores de imagem padrão exibem o contorno sem o contraste do terminal, dando a impressão de imagem comprimida ou em baixa qualidade. Ao exportar com seu **fundo escuro de terminal (`#0c0c0c`)**, a peça se destaca com total clareza como uma legítima obra de arte de terminal de alta resolução.
* **Stickers em Preto e Branco (Luris Mono)**:
  A opção `--transparent` é **exclusiva do Luris Mono** (`-m`, `-s`, `-E luris`). As tramas de mangá e traços DoG criam stickers de recorte autênticos com canal alfa transparente (>95% de transparência verificada).
* Se `--transparent` for usado com Mary ou Trumble, o sistema emite um aviso e exporta a imagem completa com fundo de terminal para preservar a fidelidade cromática.

---

## Idiomas Suportados

O Lumart conta com suporte completo a **8 idiomas**:

| Código | Idioma | Autodetecção | Forçar no Terminal |
| :---: | :--- | :--- | :--- |
| `pt` | Português | Automática via `$LANG=pt_*` | `lumart --lang pt` |
| `en` | English | Automática via `$LANG=en_*` (Padrão) | `lumart --lang en` |
| `es` | Español | Automática via `$LANG=es_*` | `lumart --lang es` |
| `fr` | Français | Automática via `$LANG=fr_*` | `lumart --lang fr` |
| `ru` | Русский | Automática via `$LANG=ru_*` | `lumart --lang ru` |
| `ja` | 日本語 | Automática via `$LANG=ja_*` | `lumart --lang ja` |
| `de` | Deutsch | Automática via `$LANG=de_*` | `lumart --lang de` |
| `ko` | 한국어 | Automática via `$LANG=ko_*` | `lumart --lang ko` |

---

## Instalação

### Método 1: Instalador Automático de Linha Única (Recomendado)
```bash
curl -fsSL https://raw.githubusercontent.com/SilentBlox01/Luma/main/install.sh | bash
```

### Método 2: Instalação Manual do Repositório
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
chmod +x install.sh
./install.sh
```

### Método 3: Pacotes Nativos Linux
Baixe pacotes pré-compilados em [GitHub Releases](https://github.com/SilentBlox01/Luma/releases):
* **Debian / Ubuntu / Linux Mint**: `sudo apt install ./lumart-*.deb`
* **Fedora / RHEL / AlmaLinux**: `sudo dnf install ./lumart-*.rpm`
* **Arch Linux / Manjaro**: `makepkg -si` no diretório `dist/arch`

---

## Referência Completa de Comandos (CLI)

| Opção | Parâmetro | Descrição |
| :--- | :--- | :--- |
| `-E`, `--engine` | `mary` \| `trumble` \| `luris` \| `spectra` | Seleciona o motor de renderização explicitamente (auto-roteado por padrão). |
| `-S`, `--sextants`| — | Ativa blocos Sextantes Unicode 2x3 (padrão de máxima fidelidade Mary Apex). |
| `-m`, `--manga` | — | Ativa modo Manga Screentone 2.0 (trama Bayer 8x8 + linhas DoG). |
| `-s`, `--sketch`| — | Ativa modo de esboço limpo de linhas puras. |
| `-B`, `--braille` | — | Ativa caracteres Braille Unicode 2x4 (8 subpixels/célula). |
| `-Q`, `--quadrants`| — | Ativa blocos Quadrantes Unicode 2x2 (4 subpixels/célula). |
| `--blocks` | — | Ativa modo de blocos de terminal otimizados (`▀` / `▄`). |
| `-w`, `--width` | `<int>` | Largura de saída em colunas (incompatível com `-F`). |
| `-F`, `--fit` | — | **Ajuste Viewport**: calcula largura e altura ideais para caber na tela sem rolagem (incompatível com `-w`). |
| `--fastfetch`, `--logo` | — | Recorte automático de margens vazias/transparentes para logos compactos. |
| `-c`, `--color` | — | Força saída em modo colorido TrueColor (padrão). |
| `--no-color` | — | Desativa saída de cor e usa motor monocromático. |
| `--font-ratio` | `<float>` | Calibração de proporção largura/altura da fonte (padrão: `0.5`). |
| `--boost`, `--vibrant` | — | Aplica realce de saturação, contraste e curvas Retinex para saída estilo arcade vibrante. |
| `-i`, `--invert`| — | Inverte o mapa de brilho (para terminais com fundo claro; autodetectado em `-m`). |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | Algoritmo de difusão de erro ou retícula. |
| `--swap` | `<cor1> <cor2>` | Substitui dinamicamente cores em espaço RGB 3D. |
| `-o`, `-O`, `--output`, `--save` | `<arquivo.png / .jpg / .gif>` | Exporta a arte para arquivo de imagem ou GIF animado. |
| `--loop` | — | **Modo animação**: reprodução contínua no terminal ou exportação em GIF animado. |
| `--transparent` | — | **Exclusivo Luris Mono**: exporta stickers recortados com transparência. |
| `--instant` | — | Exibe imediatamente sem animação de varredura (padrão). |
| `--reveal` | — | Ativa animação de varredura progressiva linha por linha. |
| `--paste` | — | Carrega e renderiza a imagem atualmente na área de transferência. |
| `-W`, `--webcam`| `[id]` | Transmite vídeo de webcam ao vivo no terminal (30-60 FPS). |
| `--lang` | `<code>` | Define o idioma da interface (`pt`, `en`, `es`, `fr`, etc.). |
| `-H`, `--history` | `[N]` | Exibe os últimos N comandos executados no histórico. |
| `-R`, `--replay` | `[N]` | Reexecuta o comando N do histórico (padrão: o último). |
| `--clear-history`| — | Limpa o histórico de comandos salvos. |
| `--install-desktop` | — | Adiciona ação "Abrir com Lumart" no menu de contexto do Linux. |
| `-v`, `--version` | — | Exibe o diagnóstico completo do sistema e dos motores. |
| `-u`, `--check-update`| — | Verifica se há novas versões disponíveis no GitHub. |
| `-uu`, `--upgrade` | — | Atualização assistida para a versão mais recente. |
| `-dg`, `--downgrade` | `[ver]` | Restauração interativa para versões anteriores. |

---

## Exemplos Práticos e Cookbook

### 1. Renderização Vetorial de Alta Definição
```bash
# Renderização direta em tela cheia com cores naturais (Zero-Flag)
lumart foto.jpg

# Comando explícito equivalente
lumart foto.jpg -E mary -S -w 90

# Especificar largura personalizada em colunas
lumart retrato.png -w 110

# Impacto arcade com saturação vibrante e Retinex
lumart foto.jpg --boost

# Renderização cel-shading arcade com Trumble
lumart anime.png -E trumble --blocks
```

### 2. Modos de Textura de Caracteres
```bash
# Braille 2x4 suave em subpixels
lumart personagem.png -B

# Quadrantes densos 2x2 blocos
lumart personagem.png -Q

# Meio-blocos clássicos Capcom CPS-2 / Neo-Geo
lumart personagem.png --blocks -w 85
```

### 3. Sticker de Mangá com Fundo Transparente (Luris Mono)
```bash
# Criação de sticker PNG transparente para Discord ou Telegram
lumart arte.png -m --transparent -o sticker_manga.png

# Esboço arquitetônico puro a nanquim
lumart predio.jpg -s -w 120

# Pôster retrô com dithering Bayer ordenado
lumart poster.jpg -m -d bayer -w 100
```

### 4. Transmissão de Webcam ao Vivo no Terminal (Spectra Weep 1.4)
```bash
# Transmissão da webcam padrão com filtros shader em tempo real
lumart -W

# Transmissão de dispositivo de webcam secundário
lumart -W 1
```

### 5. URLs Web, Área de Transferência e Pipelines Unix
```bash
# Baixar e renderizar diretamente de uma URL HTTPS
lumart https://exemplo.com/arte.png -w 80

# Renderizar imagem copiada na área de transferência
lumart --paste

# Entrada encadeada via pipeline do curl
curl -sL https://exemplo.com/foto.jpg | lumart -
```

### 6. Substituição Dinâmica de Cores
```bash
# Substituir tons de roxo por rosa chiclete
lumart sprite.png --blocks --swap purple pink
```

---

## Segredos de Engenharia, Dicas Pro e Filosofia de Terminal

> *"Com grande poder de renderização vem uma grande responsabilidade estética."*

### 1. A Lei da Gravitação da Proporção de Fonte (`--font-ratio`)
* **Realidade Matemática**: Em telas gráficas padrão, os pixels são perfeitamente quadrados ($1:1$). Na selva dos emuladores de terminal, cada célula de caractere é um monólito retangular alongado (tipicamente na proporção de $1:2$ ou $0.5$).
* **O Sintoma**: Se o seu personagem de anime parecer ter sido esmagado por uma prensa hidráulica de 50 toneladas ou esticado como chiclete em um buraco de minhoca, não culpe o motor de renderização: culpe a geometria da sua fonte.
* **O Remédio Pro**:
  * Fontes esbeltas e altas (como *Fira Code* ou *JetBrains Mono* sem espaçamento vertical forçado): tente `--font-ratio 0.45` a `0.48`.
  * Fontes monospace largas ou quadradas: tente `--font-ratio 0.52` a `0.58`.
  * O Lumart usa `0.5` por padrão, cobrindo com perfeição 90% dos emuladores modernos da galáxia.

### 2. O Teorema do Fundo Escuro e a Excomunhão do WebP
* **Por que os motores TrueColor (Mary e Trumble) recusam-se veementemente a gerar stickers recortados transparentes?**
  * As cores TrueColor no terminal funcionam por emissão luminosa aditiva sobre o preto profundo da tela (`#0c0c0c`).
  * Se você remove esse fundo escuro e cola a arte no WhatsApp com fundo branco ou em um visualizador transparente, o contraste óptico entra em colapso total: as bordas ficam serrilhadas e o personagem parece confete digital após uma explosão numa fábrica de cartuchos de tinta.
  * **Luris Mono é o Único Profeta do Sticker**: Ao trabalhar com tinta preta pura, retícula de impressão (*Ami-tone*) e linhas vetoriais DoG, o Luris gera stickers com mais de 92.9% de transparência alfa real que ficam espetaculares no Telegram, Discord e Slack.
* **A Tragédia do WebP**:
  * Durante meses, visualizadores de desktop tentaram decodificar artes de terminal salvas em `.webp` e as transformaram em massas borradas de artefatos. Na versão 2.4.0, o formato `.webp` foi formalmente banido para o reino das sombras. Vida longa à **Santíssima Trindade**: `.png` (alta fidelidade e stickers), `.jpg` (fotos compactas 95%) e `.gif` (animações multi-frame).

### 3. O Duelo Oklab: Por que Mary Avalia 31 Combinações em 700 Nanossegundos
* No espaço RGB euclidiano comum, calcular a distância entre cores com a fórmula de Pitágoras ($\sqrt{\Delta R^2 + \Delta G^2 + \Delta B^2}$) é ficção biológica: a retina humana é hiper-sensível a variações de verde e quase cega a mudanças sutis em azuis escuros.
* Mary Apex converte cada subpixel para o espaço perceptual **Oklab** ($L, a, b$) e testa matematicamente **todas as 31 bipartições de cores possíveis por célula** usando instruções SIMD e OpenMP em C++17 nativo.
* Por que tanta matemática para um terminal? Porque ciclos de CPU são baratos, mas arte medíocre no terminal é crime de lesa-majestade estética.

### 4. Trumble Orelx e a Regra de Ouro do Cel-Shading de Arcade dos Anos 90
* Redimensionamentos tradicionais (como Lanczos ou Bicúbico) calculam a média dos pixels vizinhos. Um traço preto nítido de 1 pixel se transforma em 3 pixels de névoa cinzenta e covarde.
* Trumble Orelx inverte a ordem do cosmos: reduz a imagem primeiro e **depois aplica a detecção de bordas Canny diretamente na resolução exata de subpixels do terminal**.
* O resultado: cabelos, olhos e dobras de roupas de personagens de anime mantêm exatamente **1 subpixel de espessura em preto puro**, resgatando o impacto visual inconfundível de uma máquina de fliperama Capcom CPS-2 de 1996.

### 5. Os Mandamentos Sagrados do Ajuste de Tela (`-F` vs `-w`)
* **1º Mandamento**: Se você quer que a imagem caiba como uma luva na tela sem precisar girar o scroll do mouse como um carretel de pesca, use `-F` (`--fit`).
* **2º Mandamento**: Se você for incorporar a saída numa barra lateral de 60 colunas do *Fastfetch*, use `-w 60 --fastfetch`.
* **3º Mandamento**: Jamais execute `lumart imagem.png -F -w 80`. Pedir ao Lumart que calcule a altura dinâmica da tela e ao mesmo tempo forçar uma largura fixa é uma heresia lógica. O Lumart parará educadamente com `Código de Saída 2` e uma explicação pedagógica.

### 6. O Mistério do Comando `animate`
* Se você está procurando o comando `animate` e se perguntando por que usamos `--loop`: o criador do projeto reservou o nome `animate` para um desenvolvimento secreto em dimensões superiores. Não faça perguntas cujas respostas seu emulador de terminal ainda não consegue renderizar. Use `--loop` e desfrute de suaves 60 FPS.

---

## Sistema de Atualizações e Rollback

O Lumart inclui gerenciamento completo de ciclo de vida diretamente pelo terminal:

* **Verificar Atualizações (`lumart -u`)**:
  Consulta a API de lançamentos do GitHub com segurança, sem alterar arquivos locais.
* **Atualização Automática (`lumart -uu`)**:
  Baixa a versão mais recente, recompila as bibliotecas C++ nativas e cria um backup automático em `~/.config/luma/backup/`.
* **Restauração e Downgrade Imediato (`lumart -dg`)**:
  Permite retornar a qualquer versão anterior ou backup local através de um menu interativo ou indicando a versão diretamente:
  ```bash
  lumart -dg 2.2.0
  ```

---

## Integração com o Sistema Operacional

### 1. Menu de Contexto do Gerenciador de Arquivos
Execute uma única vez:
```bash
lumart --install-desktop
```
Registra um arquivo `.desktop` e adiciona a ação *"Abrir com Lumart"* ao clicar com o botão direito em:
* **GNOME Files (Nautilus)**
* **KDE Dolphin**
* **Cinnamon Nemo**
* **XFCE Thunar**

### 2. Diagnóstico de Ambiente (`lumart -v`)
Exibe o status do suporte TrueColor de 24 bits, disponibilidade do compilador C++, bibliotecas dinâmicas aceleradas (`libmary.so`, `libmonochrome.so`), extensões SIMD e caminhos ativos de configuração.

---

## Arquitetura e Engenharia Interna

### 1. Espaço Perceptual Oklab e Otimização Discreta
Conversores tradicionais calculam distâncias euclidianas no espaço sRGB não-linear, causando distorções tonais. Mary Apex 3.5 converte cada pixel para **RGB linear** e em seguida para **Oklab** ($L, a, b$):

$$\Delta E = \sqrt{(L_1 - L_2)^2 + (a_1 - a_2)^2 + (b_1 - b_2)^2}$$

Em cada célula de Sextantes ($2 \times 3 = 6$ subpixels), existem exatamente $2^5 - 1 = 31$ formas únicas de dividir os subpixels entre primeiro plano e plano de fundo. Mary avalia todas as 31 partições, garantindo uma **solução matematicamente ótima** com zero ruído estocástico.

### 2. Tinta Subpixel 1-para-1 do Trumble
Trumble Orelx escala a imagem para a resolução exata de subpixels **antes** de calcular os gradientes de borda Canny, garantindo que cada traço preserve sua nitidez original de 1 subpixel.

### 3. Compressor de Sequências de Escape ANSI ECMA-48
Lumart utiliza um buffer inteligente que rastreia o estado de cor atual (`current_fg`, `current_bg`). Células adjacentes que compartilham a mesma cor omitem códigos repetitivos, reduzindo o fluxo de dados em até **45%** e acelerando drasticamente a renderização via SSH.

---

## Solução de Problemas

### 1. Cores parecem opacas ou distorcidas
* Verifique se o seu terminal suporta TrueColor (24-bit):
  ```bash
  export COLORTERM=truecolor
  ```
* Terminais recomendados: **Kitty**, **Alacritty**, **WezTerm**, **iTerm2**, **Foot**, **GNOME Terminal**, **Konsole**, **Windows Terminal**.

### 2. Caracteres Sextantes (`-S`) ou Braille (`-B`) aparecem como quadrados vazios
* Sua fonte monospace não possui os blocos Unicode 13.0.
* Fontes recomendadas com suporte completo a símbolos:
  * **Symbols Nerd Font** / **JetBrains Mono Nerd Font**
  * **DejaVu Sans Mono**
  * **Cascadia Code**

### 3. Desinstalação Limpa
```bash
./uninstall.sh
# Ou se instalado via gerenciador de pacotes:
sudo apt remove lumart     # Debian/Ubuntu
sudo dnf remove lumart     # Fedora
sudo pacman -Rns lumart    # Arch Linux
```

---

## Licença

Lumart é distribuído sob a Licença Pública Geral Affero GNU v3.0 (**AGPL-3.0**). Consulte o arquivo `LICENSE` para os termos completos.
