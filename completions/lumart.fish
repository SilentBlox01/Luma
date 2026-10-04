# Fish completion for lumart and luma
# Generated for Lumart v2.4.1 "Apex Horizon"

function __fish_lumart_needs_command
    set -l cmd (commandline -opc)
    if [ (count $cmd) -eq 1 ]
        return 0
    end
    return 1
end

for c in lumart luma
    # Help & Information
    complete -c $c -s h -l help -d "Show usage and options help"
    complete -c $c -s v -l version -d "Display hardware, OS and engine diagnostic card"
    complete -c $c -s u -l update -l check-update -d "Check for latest version on GitHub"
    complete -c $c -l uu -l upgrade -d "Perform interactive automatic upgrade"
    complete -c $c -l dg -l downgrade -l rollback -d "Rollback to previous version" -r

    # Viewport & Dimensions
    complete -c $c -s w -l width -d "Output width in columns" -r
    complete -c $c -s F -l fit -d "Auto-fit to terminal viewport without vertical scroll"
    complete -c $c -l fastfetch -l logo -d "Auto-crop empty margins for fastfetch logos"

    # Engines & Textures
    complete -c $c -s E -l engine -d "Select rendering engine" -r -a "mary trumble luris spectra"
    complete -c $c -s S -l sextants -d "Unicode 2x3 sextant blocks (Mary Apex default)"
    complete -c $c -s B -l braille -d "Unicode 2x4 braille characters (8 subpixels)"
    complete -c $c -s Q -l quadrants -d "Unicode 2x2 quadrant blocks (4 subpixels)"
    complete -c $c -l blocks -d "Optimized terminal half-blocks (▀/▄)"
    complete -c $c -s m -l manga -d "Manga Screentone 2.0 (Bayer 8x8 + DoG lines)"
    complete -c $c -s s -l sketch -d "Clean pen-and-ink line sketch mode"

    # Color & Visuals
    complete -c $c -s c -l color -d "Force TrueColor output (default)"
    complete -c $c -l no-color -d "Disable color and use monochrome engine"
    complete -c $c -l boost -l vibrant -d "Vibrant arcade saturation, contrast and Retinex"
    complete -c $c -s i -l invert -d "Invert character lightness"
    complete -c $c -s d -l dither -d "Select dithering algorithm" -r -a "atkinson floyd bayer none"
    complete -c $c -l font-ratio -d "Calibrate font aspect ratio width/height" -r
    complete -c $c -l swap -d "Dynamically swap colors in 3D RGB space" -r

    # Export & Animation
    complete -c $c -s o -s O -l output -l save -d "Export to graphic image or animated GIF" -r
    complete -c $c -l loop -d "Animation mode: smooth terminal loop or animated GIF export"
    complete -c $c -l transparent -d "Luris Mono exclusive: transparent background sticker"
    complete -c $c -l instant -l no-reveal -d "Display output instantly without scan animation"
    complete -c $c -l reveal -d "Enable progressive line-by-line reveal animation"
    complete -c $c -l paste -d "Render image currently in clipboard"

    # System & Utilities
    complete -c $c -l lang -d "Set interface language" -r -a "en es pt fr ru ja de ko"
    complete -c $c -s W -l webcam -d "Live webcam terminal streaming at 30-60 FPS" -r
    complete -c $c -s H -l history -d "Show last N commands in history" -r
    complete -c $c -s R -l replay -l last -d "Re-run command from history" -r
    complete -c $c -l clear-history -d "Wipe command execution history"
    complete -c $c -l install-desktop -d "Register file manager context menu integration"
    complete -c $c -l completions -d "Generate shell completion script" -r -a "bash zsh fish"
end
