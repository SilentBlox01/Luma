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
3. [Exportação Gráfica e Política de Stickers](#exportação-gráfica-e-política-de-stickers)
4. [Idiomas Suportados (8 Idiomas)](#idiomas-suportados)
5. [Instalação Rápida e Pacotes](#instalação)
6. [Referência Completa de Comandos (CLI)](#referência-completa-de-comandos)
7. [Exemplos Práticos e Cookbook](#exemplos-práticos-e-cookbook)
8. [Sistema de Atualizações e Rollback](#sistema-de-atualizações-e-rollback)
9. [Integração com o Sistema Operacional](#integração-com-o-sistema)
10. [Arquitetura e Engenharia Interna](#arquitetura-e-engenharia-interna)
11. [Solução de Problemas](#solução-de-problemas)
12. [Licença](#licença)

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

## Exportação Gráfica e Política de Stickers

O Lumart conta com exportador de alta definição (`-o imagem.png` ou `-o imagem.jpg`) com largura padrão de estúdio de **160 colunas**.

### 1. Desativação Permanente do Formato WebP
* **O formato `.webp` foi desativado permanentemente para exportação gráfica**.
* Caso seja especificado um arquivo com extensão `.webp`, o Lumart encerra a operação com aviso informativo solicitando `.png` ou `.jpg`.
* Formatos suportados:
  * **`.png`**: Alta definição sem perdas, compressão otimizada e suporte a canal alfa transparente.
  * **`.jpg` / `.jpeg`**: Máxima compatibilidade, qualidade 95% e tabelas Huffman otimizadas.

### 2. Stickers Transparentes Exclusivos do Luris Mono
* **Por que os motores a cores não fazem stickers transparentes?**
  Ao recortar um personagem colorido com 160 colunas em fundo transparente, visualizadores de imagem padrão exibem o contorno sem o contraste da terminal, dando a impressão de imagem comprimida ou em baixa qualidade. Ao exportar com seu **fundo escuro de terminal (`#0c0c0c`)**, a peça se destaca com total clareza como uma legítima obra de arte de terminal de alta resolução.
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
* **Debian / Ubuntu**: `sudo apt install ./lumart-*.deb`
* **Fedora / RHEL**: `sudo dnf install ./lumart-*.rpm`
* **Arch Linux**: Execute `makepkg -si` no diretório `dist/arch`

---

## Referência Completa de Comandos

```text
Uso: lumart [OPÇÕES] <caminho_ou_url_da_imagem>
```

| Opção | Parâmetro | Descrição |
| :--- | :--- | :--- |
| `-m`, `--manga` | — | Ativa modo Manga Screentone 2.0 (trama Bayer 8x8 + linhas DoG). |
| `-s`, `--sketch`| — | Ativa modo de esboço limpo de linhas puras. |
| `-B`, `--braille` | — | Ativa caracteres Braille Unicode 2x4 (8 subpixels/célula). |
| `-Q`, `--quadrants`| — | Ativa blocos Quadrantes Unicode 2x2 (4 subpixels/célula). |
| `--blocks` | — | Ativa modo de blocos de terminal otimizados (`▀`). |
| `-w`, `--width` | `<int>` | Largura de saída em colunas (padrão: tamanho da janela). |
| `-i`, `--invert`| — | Inverte o mapa de brilho (para terminais com fundo claro; autodetectado em `-m`). |
| `--boost`, `--vibrant` | — | Aplica realce de saturação, contraste e curvas Retinex para saída estilo arcade vibrante. |
| `-d`, `--dither` | `atkinson` \| `floyd` \| `bayer` \| `none` | Algoritmo de difusão de erro ou retícula. |
| `--swap` | `<cor1> <cor2>` | Substitui dinamicamente cores em espaço RGB 3D. |
| `-o`, `--output` | `<arquivo.png / .jpg>` | Exporta a arte para arquivo de imagem de alta definição. |
| `--transparent` | — | **Exclusivo Luris Mono**: exporta stickers recortados com transparência. |
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

### 1. Renderização de Alta Definição (Sem Flags / Padrão)
```bash
lumart foto.jpg -w 90
```

### 2. Arte em Blocos Otimizados
```bash
lumart personagem.png --blocks -w 85
```

### 3. Sticker de Mangá com Fundo Transparente (Luris Mono)
```bash
lumart manga.png -m --transparent -o sticker.png
```

### 4. Transmissão de Webcam ao Vivo
```bash
lumart -W
```

### 5. Imagem da Área de Transferência
```bash
lumart --paste
```

---

## Licença

Lumart é distribuído sob a Licença Pública Geral Affero GNU v3.0 (**AGPL-3.0**). Consulte o arquivo `LICENSE` para os termos completos.
