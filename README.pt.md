[English](README.md) | [Español](README.es.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

# Luma

**Um motor de renderização de imagem para terminal de alta fidelidade escrito em Python.**

O Luma é um motor de renderização de terminal de código aberto focado em um único objetivo:

> **Máxima fidelidade visual com o mínimo de espaço no terminal.**

Ao contrário dos conversores ASCII tradicionais que simplesmente mapeiam o brilho da imagem para caracteres, o Luma explora diferentes sistemas de glifos de terminal, matemática de cores RGB Linear e técnicas de renderização para preservar a maior quantidade de informações visuais possível dentro de um número limitado de células do terminal.

## Recursos

* Renderização de imagens de alta fidelidade no terminal
* Renderização baseada em ASCII, Braille e Blocos
* **Renderização Estilo OS (`--os-style`)**: Caracteres clássicos de terminal (pontos, letras) para logotipos estilo Neofetch.
* **Troca de Cor em Tempo Real (`--swap`)**: Troque dinamicamente até 5 cores com base na distância de cor Euclidiana em 3D.
* **Motor Épico de Cores (Padrão)**: Calcula a média das cores no espaço RGB Linear para evitar resultados opacos, enquanto aplica contraste dinâmico e saturação (HDR).
* Largura de saída configurável
* Suporte a terminal Truecolor (ANSI de 24 bits)
* Projetado para tamanhos de saída extremamente pequenos
* Baseado em Python e altamente expansível

## Exemplo

```bash
# Converta uma imagem usando caracteres Braille, cores, e trocando roxo por rosa
luma image.png -w 45 --braille -c --swap purple pink
```

## Instalação

Você pode executar o Luma diretamente do código fonte ou compilá-lo em um pacote nativo do Linux (DEB, RPM ou Arch PKGBUILD).

**Opção 1: Baixar Pacotes Pré-compilados (Recomendado)**
Você pode baixar os pacotes `.deb` ou `.rpm` prontos para uso diretamente da página de [GitHub Releases](https://github.com/SilentBlox01/Luma/releases).

**Opção 2: Executar diretamente do código fonte**
```bash
git clone https://github.com/SilentBlox01/Luma.git
cd Luma
# Certifique-se de ter o Pillow instalado
pip install -r requirements.txt
python3 lumart.py --help
```

**Opção 3: Compilar e construir pacotes nativos você mesmo**
O Luma inclui um script de construção automatizado para empacotar a ferramenta em um binário autônomo usando o PyInstaller.
```bash
chmod +x build_packages.sh
./build_packages.sh
```
Após compilar, você pode instalá-lo globalmente através do seu gerenciador de pacotes:
- **Debian/Ubuntu**: `sudo apt install ./dist/lumart-2.0.0.deb`
- **Fedora/RHEL**: `sudo dnf install ./dist/lumart-2.0.0.rpm`
- **Arch Linux**: `cd dist/arch && makepkg -si`

## Uso

Se você instalou o pacote, pode executar `lumart` ou `luma` de qualquer lugar. Caso contrário, execute o script Python diretamente.

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

Forçar renderização clássica de caracteres estilo OS retro (útil para logotipos de SO):
```bash
python3 lumart.py image.png --os-style -c
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

## Roteiro

* [x] Renderizador inicial de imagem para terminal
* [x] Renderização Braille
* [x] Renderização baseada em blocos
* [x] Melhoria de renderização perceptiva (Motor RGB Linear)
* [x] Processamento de contraste e luminância (Motor Épico)
* [x] Mapeamento de cores em tempo real e limites
* [ ] Pontilhado (Dithering) avançado
* [ ] Seleção automática de glifos
* [ ] Benchmarks de similaridade de imagens
* [ ] Otimização de renderização
* [ ] Renderização assistida por aprendizado de máquina (Machine Learning)
* [ ] Suporte para renderização de Vídeo e GIF
* [ ] Expansão de sistemas de glifos de terminal

## Contribuindo

O Luma é um projeto de código aberto e contribuições são bem-vindas.

Se você tem uma ideia para um algoritmo de renderização, otimização, sistema de glifos, benchmark ou melhoria, fique à vontade para abrir um *issue* ou enviar um *pull request*. (Veja `CONTRIBUTING.md` para mais detalhes).

## Licença

O Luma é lançado sob a GNU Affero General Public License v3.0 (AGPL-3.0). Veja o arquivo `LICENSE` para mais detalhes.
