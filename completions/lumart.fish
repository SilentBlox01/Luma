# Fish completion for lumart and luma
# Generated for Lumart v2.5.0 "Apex Nova"

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
    complete -c $c -l crop -d "Crop image: center, square, or x,y,w,h" -r
    complete -c $c -l zoom -d "Digital zoom factor centered on subject" -r
    complete -c $c -l rotate -d "Rotate image 90, 180, or 270 degrees clockwise" -r -a "90 180 270"
    complete -c $c -l flip -l mirror -d "Mirror image horizontally or vertically" -r -a "h v horizontal vertical"

    # Engines & Textures
    complete -c $c -s E -l engine -d "Select rendering engine" -r -a "mary trumble luris spectra color mono bw manga sketch crosshatch"
    complete -c $c -s S -l sextants -d "Unicode 2x3 sextant blocks (Mary Apex default)"
    complete -c $c -s B -l braille -d "Unicode 2x4 braille characters (8 subpixels)"
    complete -c $c -s Q -l quadrants -d "Unicode 2x2 quadrant blocks (4 subpixels)"
    complete -c $c -l blocks -d "Optimized terminal half-blocks (▀/▄)"
    complete -c $c -s m -l manga -d "Manga Screentone 2.0 (Bayer 8x8 + DoG lines)"
    complete -c $c -s s -l sketch -d "Clean pen-and-ink line sketch mode"
    complete -c $c -s ch -l crosshatch -d "Authentic Manga 45-degree pen crosshatching dither"
    complete -c $c -s cs -l charset -d "Select typography charset ramp" -r -a "dense standard simple blocks shades math runes katakana crosshatch minimal binary hex braille"
    complete -c $c -l gamma -d "Gamma contrast adjustment factor" -r
    complete -c $c --border -d "Decorative frame border style" -r -a "rounded single double heavy ascii blocks"
    complete -c $c --align -d "Horizontal alignment" -r -a "left center right"
    complete -c $c --center -d "Center horizontally in terminal"
    complete -c $c --brightness -d "Adjust image brightness multiplier" -r
    complete -c $c --contrast -d "Adjust image contrast multiplier" -r
    complete -c $c --saturation -d "Adjust image color saturation multiplier" -r
    complete -c $c -l preload -l smooth -d "Preload all frames into RAM for smooth 60 FPS playback"
    complete -c $c -l bench -l benchmark -d "Run performance benchmark suite"
    complete -c $c -l matrix -d "Render image in digital Katakana and binary green Matrix code"
    complete -c $c -l matrix-rain -d "Falling Katakana digital rain animation"

    # Color & Visuals
    complete -c $c -s c -l color -d "Force TrueColor output (default)"
    complete -c $c -l no-color -d "Disable color and use monochrome engine"
    complete -c $c -l boost -l vibrant -d "Vibrant arcade saturation, contrast and Retinex"
    complete -c $c -s i -l invert -d "Invert character lightness"
    complete -c $c -s d -l dither -d "Select dithering algorithm" -r -a "atkinson floyd bayer none"
    complete -c $c -l font-ratio -d "Calibrate font aspect ratio width/height" -r
    complete -c $c -l swap -d "Dynamically swap colors in 3D RGB space" -r
    complete -c $c -l theme -l palette -d "Terminal color palette" -r -a "catppuccin dracula nord gruvbox synthwave vaporwave gameboy solarized"
    complete -c $c -l crt -l scanlines -d "Simulate retro CRT scanlines and phosphor monitor" -r -a "green amber color scanlines"

    # Export & Animation & Clipboard
    complete -c $c -s o -s O -l output -l save -d "Export to PNG, JPG, GIF, ANS, or TXT" -r
    complete -c $c -l loop -d "Animation mode: smooth terminal loop or animated GIF export"
    complete -c $c -s r -l remove-bg -d "Remove background without quality loss (standalone saves HD PNG)"
    complete -c $c -l bg-tolerance -l tolerance -d "Color tolerance for background removal (1-100)" -r
    complete -c $c -l fps -l target-fps -d "Target framerate for animations and video" -r
    complete -c $c -l transparent -d "Luris Mono exclusive: transparent background sticker"
    complete -c $c -s C -l copy -d "Copy rendered ANSI art to system clipboard"
    complete -c $c -l copy-plain -d "Copy plain ASCII text without escape codes to clipboard"
    complete -c $c -l instant -l no-reveal -d "Display output instantly without scan animation"
    complete -c $c -l reveal -d "Enable progressive line-by-line reveal animation"
    complete -c $c -l paste -d "Render image currently in clipboard"

    # Interactive & Gallery & Diff
    complete -c $c -s I -l interactive -l tui -d "Interactive live parameter tuning terminal UI"
    complete -c $c -l slideshow -d "Interactive terminal slideshow gallery"
    complete -c $c -l delay -d "Slideshow delay between images in seconds" -r
    complete -c $c -l diff -d "Side-by-side terminal image comparison" -r
    complete -c $c -l showcase -d "Generate 4-in-1 comparison showcase across all flagship engines"
    complete -c $c -l info -l inspect -d "Display visual image inspector, resolution, and color palette"
    complete -c $c -l fetch-preset -d "Generate Fastfetch/Neofetch ANSI logo and config.jsonc snippet"
    complete -c $c -l shader -d "Spectra Weep 2.0 multi-spectral shader" -r -a "neon cyberpunk thermal tron matrix amber manga theme normal hologram glitch phosphor-bloom solarize"

    # System & Utilities
    complete -c $c -l lang -d "Set interface language" -r -a "en es pt fr ru ja de ko"
    complete -c $c -s W -l webcam -d "Live webcam terminal streaming at 30-60 FPS" -r
    complete -c $c -s H -l history -d "Show last N commands in history" -r
    complete -c $c -s R -l replay -l last -d "Re-run command from history" -r
    complete -c $c -l clear-history -d "Wipe command execution history"
    complete -c $c -l install-desktop -d "Register file manager context menu integration"
    complete -c $c -l completions -d "Generate shell completion script" -r -a "bash zsh fish"
end
