[English](CONTRIBUTING.md) | [Español](CONTRIBUTING.es.md) | [Português](CONTRIBUTING.pt.md) | [Русский](CONTRIBUTING.ru.md) | [日本語](CONTRIBUTING.ja.md) | [Deutsch](CONTRIBUTING.de.md) | [한국어](CONTRIBUTING.ko.md)

# Contribuindo com o Luma

Obrigado pelo seu interesse em melhorar o Luma! Este projeto busca expandir os limites gráficos do terminal, e todas as contribuições são muito bem-vindas.

## 🐛 Reportar Bugs ou Sugerir Ideias

Se você encontrar um problema ou tiver uma ótima ideia (como um novo algoritmo de renderização, padrão de pontilhamento ou suporte a animações), abra uma **Issue** no GitHub. Por favor, inclua:
- O sistema operacional e emulador de terminal que você está usando (ex: Fedora com Alacritty, Ubuntu com Kitty, Windows Terminal).
- O comando exato e os argumentos que causaram o erro.
- Se possível, um exemplo da arte ASCII gerada ou da imagem original.

## 🛠️ Contribuir com Código

1. Faça um **Fork** do repositório no GitHub.
2. Crie uma **nova branch** para sua funcionalidade ou correção (`git checkout -b feature/nova-magica`).
3. Escreva e teste o seu código. O núcleo do motor está em `lumart.py`.
4. Faça commit das alterações com uma mensagem clara (`git commit -m 'feat: novo algoritmo XYZ'`).
5. Envie para a sua branch (`git push origin feature/nova-magica`).
6. Abra um **Pull Request**.

### Estrutura do Projeto
- `lumart.py`: Todo o núcleo do motor: processamento perceptivo em Linear RGB, pontilhamento com Matriz de Bayer, esculpido com Braille/meios-blocos e CLI multilíngue.
- `install.sh`: Instalador universal Plug & Play compatível com Fedora, Debian/Ubuntu, Arch Linux, openSUSE e macOS.
- `build_packages.sh`: Script automatizado para compilar binários autônomos com `PyInstaller` e gerar pacotes `.deb`, `.rpm` e `PKGBUILD`.
- `pyproject.toml`: Definição de empacotamento moderno suportando `pipx install .` e `pip install --user .`.

### Diretrizes de Desenvolvimento
- **Zero dependências pesadas**: Mantenha o Luma leve e plug-and-play. Dependa apenas de Pillow (`PIL`) e da biblioteca padrão do Python.
- **Fidelidade Visual no Terminal**: Todo novo recurso deve priorizar a máxima fidelidade visual em ambientes de terminal reais.
- **Suporte Multilíngue**: Se você adicionar novos argumentos de CLI ou mensagens, adicione as traduções aos 7 idiomas no dicionário `TRANSLATIONS` (`en`, `es`, `pt`, `ru`, `ja`, `de`, `ko`).

Divirta-se criando gráficos incríveis no terminal! 🎨
