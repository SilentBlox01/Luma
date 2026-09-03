# 🔧 Troubleshooting / "It's Broken!" Guide

If Luma is acting up, don't panic. You're probably just hitting one of the classic terminal rendering limitations. I've compiled this list so you don't have to spend hours debugging or searching on StackOverflow like I did.

## 1. "It looks like absolute garbage / weird characters"
**The problem:** Your terminal font doesn't support Unicode Braille (`--braille`) or Half-blocks (`--blocks`). Or your terminal emulator is just ancient.
**The fix:** 
- Install a proper nerd font (like Fira Code, JetBrains Mono, or Hack).
- If you're on Windows, use Windows Terminal instead of the old `cmd.exe`. Seriously, `cmd.exe` is from the stone age and will butcher the unicode characters.

## 2. "The colors look washed out or completely wrong"
**The problem:** Luma outputs 24-bit Truecolor (ANSI escape codes) by default to get that HDR look. If your terminal only supports 256 colors, it will try to approximate it and usually fails miserably.
**The fix:** 
- Make sure your terminal supports Truecolor (Alacritty, Kitty, Windows Terminal, and iTerm2 are all fine).
- Mac users: the default macOS `Terminal.app` sucks at colors. Switch to iTerm2.

## 3. "ImportError: No module named PIL"
**The problem:** You didn't install Pillow, and my lazy auto-installer failed because of permission issues (or your OS blocked it).
**The fix:** 
Just install it manually: 
```bash
pip3 install Pillow
```
*Note: If you get a "managed environment" error on newer Linux distros, use a virtual environment (`python3 -m venv venv && source venv/bin/activate`) before running pip.*

## 4. "The image is way too massive and it broke my terminal history"
**The problem:** By default, Luma tries to render at a width of 90 characters. If you passed a massive image and your terminal window is small, it wraps the text and ruins the illusion.
**The fix:**
Use `-w` to shrink it down to fit your window. 
Example: `luma image.png -w 50`

## 5. "I used `--swap` and the script crashed"
**The problem:** `--swap` needs pairs of colors. If you gave it an odd number of arguments (e.g., `--swap red blue green`), it freaks out because it doesn't know what to swap 'green' into.
**The fix:**
Always pass them in pairs: `--swap [color_to_replace] [new_color]`. 
Example: `--swap red blue green yellow`.

## 6. "Luma is stuck in Russian and I don't speak Russian"
**The problem:** You tested `--lang ru` once, and now it saved that to the config file at `~/.config/luma/config.json`. (Happened to me actually lol 🤓☝️)
**The fix:**
Just force it back to your language with `luma --lang en` (or `es`, `ja`, etc.). Or you can just nuke the config file entirely. I probably should have made a `reset` command, but deleting the file works fine for now.

---
### Still broken?
If you found a bug that isn't here, feel free to open an issue. But please, **attach a screenshot** of what's happening. I can't debug "it looks weird" blindly!
