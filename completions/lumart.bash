# Bash completion for lumart and luma
# Generated for Lumart v2.5.0 "Apex Nova"

_lumart_completions() {
    local cur prev words cword
    _init_completion || return

    local engines="mary trumble luris spectra color mono bw manga sketch"
    local dithers="atkinson floyd bayer none"
    local langs="en es pt fr ru ja de ko"
    local shells="bash zsh fish"
    local themes="catppuccin dracula nord gruvbox synthwave vaporwave gameboy solarized"
    local crts="green amber color scanlines"
    local opts="
        -h --help
        -v --version
        -u --update --check-update
        -uu --upgrade
        -dg --downgrade --rollback
        -w --width
        -F --fit
        -E --engine
        -c --color --no-color
        -S --sextants
        -B --braille
        -Q --quadrants
        --blocks
        -m --manga
        -s --sketch
        --boost --vibrant
        -i --invert
        --swap
        -d --dither
        --font-ratio
        -o -O --output --save
        --loop
        --fastfetch --logo
        -r --remove-bg
        --transparent
        --instant --no-reveal
        --reveal
        --paste
        --lang
        --theme --palette
        --crt --scanlines
        --matrix
        --matrix-rain
        -C --copy
        --copy-plain
        --crop
        --zoom
        --slideshow
        --delay
        -I --interactive --tui
        --diff
        -W --webcam
        -H --history
        -R --replay --last
        --clear-history
        --install-desktop
        --completions
    "

    case "$prev" in
        -E|--engine)
            COMPREPLY=( $(compgen -W "$engines" -- "$cur") )
            return 0
            ;;
        -d|--dither)
            COMPREPLY=( $(compgen -W "$dithers" -- "$cur") )
            return 0
            ;;
        --lang)
            COMPREPLY=( $(compgen -W "$langs" -- "$cur") )
            return 0
            ;;
        --theme|--palette)
            COMPREPLY=( $(compgen -W "$themes" -- "$cur") )
            return 0
            ;;
        --crt|--scanlines)
            COMPREPLY=( $(compgen -W "$crts" -- "$cur") )
            return 0
            ;;
        --completions)
            COMPREPLY=( $(compgen -W "$shells" -- "$cur") )
            return 0
            ;;
        -o|-O|--output|--save)
            _filedir '@(png|jpg|jpeg|gif|ans|asc|txt)' 2>/dev/null || COMPREPLY=( $(compgen -f -X '!*.@(png|jpg|jpeg|gif|ans|asc|txt)' -- "$cur") )
            return 0
            ;;
        --diff)
            _filedir '@(png|jpg|jpeg|bmp|gif|webp|apng|PNG|JPG|JPEG|BMP|GIF|WEBP|APNG)' 2>/dev/null || COMPREPLY=( $(compgen -f -- "$cur") )
            return 0
            ;;
        -w|--width|--font-ratio|--zoom|--delay|-H|--history|-R|--replay|--last|-W|--webcam|-dg|--downgrade|--rollback|--swap|--crop)
            return 0
            ;;
    esac

    if [[ "$cur" == -* ]]; then
        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
        return 0
    fi

    # Subcommand 'diff'
    if [[ "${words[1]}" == "diff" ]]; then
        _filedir '@(png|jpg|jpeg|bmp|gif|webp|apng|PNG|JPG|JPEG|BMP|GIF|WEBP|APNG)' 2>/dev/null || COMPREPLY=( $(compgen -f -- "$cur") )
        return 0
    fi

    # Image file completions
    _filedir '@(png|jpg|jpeg|bmp|gif|webp|apng|PNG|JPG|JPEG|BMP|GIF|WEBP|APNG)' 2>/dev/null || COMPREPLY=( $(compgen -f -- "$cur") )
}

complete -F _lumart_completions lumart
complete -F _lumart_completions luma
