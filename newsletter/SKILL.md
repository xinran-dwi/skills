---
name: newsletter
description: Write a Design with AI newsletter article in Xinran's voice and package it as a Substack-pasteable HTML file that keeps heading/bold hierarchy. Use this whenever the user wants to write, draft, or format a newsletter issue, Substack post, or article - especially when turning something they just built or tested with AI into a written piece ("write this up", "turn this session into an article", "draft a newsletter about what we just did", "make this pasteable into Substack"). Also use it when the user asks to fix an existing draft's voice, make an article less technical, or produce a Substack-ready version of something already written. Triggers on /newsletter.
---

# Design with AI newsletter

Turn something the user built, tested, or figured out into a published newsletter
issue: written in their voice, aimed at designers who don't code, and shipped as a
file they can paste straight into Substack with formatting intact.

Two things make or break this, and both are easy to get wrong:

1. **The voice is specific and it is not the default essay voice.** Read
   `references/voice.md` before writing a single line. The failure mode is writing
   something cool, formal and contraction-free that reads like a trade journal.
2. **Substack destroys most formatting on paste, including tables entirely.**
   Read `references/substack-format.md` before producing output. The failure mode
   is handing over Markdown, which pastes as literal `##` and `**`.

## The workflow

**1. Find out what the piece is about.** Usually it's right there in the
conversation — the user just did the thing. Pull the details from the session
history rather than interviewing them about work you both watched happen: what
they asked for verbatim, what broke, what surprised them, what it cost.

If the piece covers an AI session, get the real numbers with
`scripts/session_stats.py` (see **Real numbers** below). Never estimate them.

**2. Confirm the audience.** The default is *designers who use AI tools, know what
Figma is, and have never written code.* Nearly every readability problem traces
back to writing for engineers instead. If the user says otherwise, follow them.

**3. Draft in the voice.** `references/voice.md` has the rules and before/after
pairs. Keep the running order below unless the user asks for something else.

**4. Produce the Substack paste file.** Start from
`assets/paste-template.html` and follow `references/substack-format.md` for the
element whitelist and the conversions. This is the deliverable. A beautiful
styled page that can't be pasted isn't finished work.

**5. Publish that same page as the artifact.** Not a separate styled version —
the paste page *is* the useful view, and a local file the author has to hunt
down is friction at exactly the wrong moment. It reads fine as an article; the
copy toolbar is small and sits above the content. Ask them to test the buttons
on the published link, because a published page runs in a sandboxed iframe and
clipboard behaviour there differs from a local file.

## Running order

This order is deliberate and the user has asked for it explicitly: the overview
comes first, and **setup comes early, not buried at the end**. A reader deciding
whether to try something wants to know the cost of entry before the story.

```
Title
Subtitle (one italic line)
---
Opening question           A real question the piece answers. Not a teaser.
Overview                   What you had, what you tried, what happened.
[hero image]               The finished result, up top. Show the payoff.
"Here's what we'll cover"  Bulleted, bold lead-ins.
Term definitions           One short para defining anything a designer won't know.
"Let's get into it."

1. Set it up first         Numbered steps. Commands in code blocks.
2. [What you actually did]  Verbatim prompts if there were any. Keep the typos.
3. [How it works]           The mechanism, in plain words.
4. [What it cost]           Real numbers only.
5. N things I got wrong     Bold lead-ins, one lesson each. Usually the best part.

Closing                    Short, warm, human.
```

Sections 2-4 flex with the subject. Section 5 rarely should — the mistakes are
what make a piece worth reading rather than a press release, and they're the part
that's hardest to reconstruct later. Collect them as you go.

## Voice, in brief

Full guide with examples: `references/voice.md`. The five things that matter most:

- **"I" and "you", always.** Personal experience, then direct address.
- **Contractions everywhere.** "It's", "didn't", "you'll". Their absence is the
  single clearest tell that the draft is in the wrong register.
- **Short sentences, and single-sentence paragraphs for emphasis.** Vary the
  rhythm. Let a good line stand alone.
- **Imperative headings.** "Set it up first", not "Setup". "Watch the loop, not
  the prompt", not "The loop".
- **Define terms as you go.** Assume no baseline. One clause is usually enough:
  "Blender is a free 3D program — think Figma, but for rooms instead of screens."

## Keeping it non-technical

The recurring failure is keeping the *lesson* plain while the *evidence* stays in
implementation terms. Lead with what the reader would experience. Keep a number
only when it is the point of the sentence. Don't name a file, flag, function, or
object unless the reader has to type it.

Before: "Selecting a chair by bounding box quietly grabs the table too — a box
query returned 36 vertices where 32 were wanted."

After: "In the file, the chairs and table are welded into one lump. Ask it to move
'the chair' and it can take part of the table with it — they touch at exactly the
same spot."

Same insight, no jargon, and it's *more* vivid. That's the bar.

After drafting, sweep the body for terms that shouldn't have survived — the ones
specific to this piece's domain, plus the usual suspects: file extensions, flags,
function names, regexes, `snake_case`, and words like *vertices*, *socket*,
*regex*, *repo*, *cache*. A quick grep is faster and more honest than rereading.

Technical specifics belong in the repo's own docs, not the article. Cut them
unless the user asks for an appendix.

## Real numbers

If the piece makes a claim about time or cost, measure it:

```bash
python3 ~/.claude/skills/newsletter/scripts/session_stats.py --project <dir>
```

It reads the Claude Code transcript for a project, splits it at each user prompt,
and reports per-task turns, tool calls, wall-clock minutes, output tokens, and
cached input.

Two things about those numbers that are worth explaining *in the article*, because
they're genuinely counterintuitive and readers get them wrong:

- Cached input dwarfs output, often 200:1. The whole conversation is re-sent on
  every tool round-trip, so cost tracks **how many steps it took**, not how much
  the user typed. "Long prompts are cheap; it's the checking that adds up."
- Wall-clock is time *inside* a task, not elapsed across the day. Say so, or the
  numbers imply a focused sprint that didn't happen.

Define "token" once, in passing — *roughly three-quarters of a word* — and then
use it freely. The audience meets the word constantly; they just haven't been told
what it means.

## Images

Screenshots and renders carry a lot here, and this newsletter uses them heavily.
Prefer images that do work over images that decorate:

- **A before/after pair** beats any amount of description, especially when the two
  states are one sentence apart. This is the highest-value image in most pieces.
- **The hero** goes up top, showing the finished result.
- **A failure** is worth showing. The bad render, the broken state.

Resize to ~1400px and convert to JPEG (~78 quality) — source screenshots are
usually 1MB+ PNGs and Substack doesn't need that. `sips` does this on macOS:

```bash
sips -Z 1400 -s format jpeg -s formatOptions 78 in.png --out out.jpg
```

Number the files in reading order (`01-`, `02-`) so they're easy to drag in if the
paste doesn't carry them.

## Output

Put deliverables in a `newsletter/` folder next to the work being written about:

```
newsletter/
├── substack-paste.html    The article + copy buttons. Publish this one.
├── images/                01-, 02-, ... in reading order, full size
└── HOW-TO-PASTE.md        Steps + which image goes where
```

Images get **inlined as data: URIs** inside `substack-paste.html` (a relative
path becomes `file:///…` on the clipboard, which Substack can't read), while the
originals stay in `images/` as the drag-in fallback.

Open the file in the browser when you're done, and publish it so the author has
a link rather than a file to find.

## If the article changes later

The renders get embedded in the paste page, so a change to the underlying work
means re-rendering and re-embedding — the published page won't pick it up on its
own. Match images by their `alt` text when swapping, not by order, so an edit
can't silently replace the wrong picture.

One judgement call worth making deliberately: a **before/after pair documents a
past state**. Re-rendering the "after" with unrelated later fixes in it makes the
pair differ in two things at once and quietly breaks the comparison the section
is making. Leave those; refresh the images that show current state.
