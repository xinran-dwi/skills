Creator: Xinran Ma

More resources like this on: designwithai.co

# images-to-video

## What it is

Turns a set of SVG diagrams (or flat images) into a self-playing, looping animated HTML trailer — each element draws, fades, or pops in individually, then the scene cuts to the next. The output is one standalone `.html` file you open in a browser and screen-record to get a video or GIF. Pairs directly with the `newsletter-diagram` skill, which produces the monochrome SVG diagrams that are the ideal scene source.

## When to use it

- You have diagrams (especially from `newsletter-diagram`) and want to turn them into an animated reel or teaser
- You say things like "animate my diagrams", "make an animated trailer", "turn these into a motion graphic", "a trailer that draws the lines in", or "animated version of these"
- You want a looping HTML that you can screen-record into a video or GIF for a newsletter, social post, or presentation
- You only have flat PNGs — it can still crossfade between them (though without per-element draw-on)

## How to use it

### Install (one time)

**macOS / Linux**
```bash
mkdir -p ~/.claude/skills/images-to-video/references
mkdir -p ~/.claude/skills/images-to-video/scripts
curl -fsSL https://raw.githubusercontent.com/xinran-dwi/skills/main/images-to-video/SKILL.md -o ~/.claude/skills/images-to-video/SKILL.md
curl -fsSL https://raw.githubusercontent.com/xinran-dwi/skills/main/images-to-video/references/animation-guide.md -o ~/.claude/skills/images-to-video/references/animation-guide.md
curl -fsSL https://raw.githubusercontent.com/xinran-dwi/skills/main/images-to-video/scripts/build_trailer.py -o ~/.claude/skills/images-to-video/scripts/build_trailer.py
```

**Windows (PowerShell)**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\images-to-video\references"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\images-to-video\scripts"
Invoke-WebRequest "https://raw.githubusercontent.com/xinran-dwi/skills/main/images-to-video/SKILL.md" -OutFile "$env:USERPROFILE\.claude\skills\images-to-video\SKILL.md"
Invoke-WebRequest "https://raw.githubusercontent.com/xinran-dwi/skills/main/images-to-video/references/animation-guide.md" -OutFile "$env:USERPROFILE\.claude\skills\images-to-video\references\animation-guide.md"
Invoke-WebRequest "https://raw.githubusercontent.com/xinran-dwi/skills/main/images-to-video/scripts/build_trailer.py" -OutFile "$env:USERPROFILE\.claude\skills\images-to-video\scripts\build_trailer.py"
```

Restart Claude Code.

### Step by step

1. **Trigger the skill** — just ask naturally:
   - "Turn these diagrams into an animated trailer"
   - "Animate my SVGs into a looping HTML"
   - "Make a motion graphic from these scenes"

2. **Provide your scenes** — share SVG diagrams (ideal, for per-element draw-on) or flat PNGs (crossfade only). If you don't have SVGs yet, ask Claude to generate them with `newsletter-diagram` first

3. **Claude chooses animation depth:**
   - **Quick** (`--auto`): staggered fade-in on every element — works on any plain diagram SVG, no manual tagging needed
   - **Full effect**: Claude hand-tags each element with `draw` / `fade` / `pop` classes and delay offsets so lines draw themselves on, dots pop, and labels rise in — the signature look

4. **HTML is built** — one self-contained `.html` file with a 16:9 stage, per-element CSS animations, and a hairline progress bar tracking the loop

5. **Open and screen-record** — open the file full-screen in Chrome (F11), record one full loop with macOS Cmd+Shift+5 or Windows Win+G, then optionally convert to GIF at ezgif.com

## Requirements

- [Claude Code](https://claude.ai/code)
- Python 3 (pre-installed on macOS and most Linux distros)
- SVG scenes for the draw-on effect (flat PNGs work too, but only crossfade)
- A browser + screen recorder to capture the animation as a video/GIF
