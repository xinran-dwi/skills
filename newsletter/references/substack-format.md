# Shipping to Substack with formatting intact

Substack's editor is **ProseMirror**, and that decides everything here. It reads
rich text off the clipboard and parses it against a strict schema, quietly
dropping or reshaping anything that doesn't fit. Nothing errors — you just get a
draft where the numbering restarted, a quote became a plain paragraph, and a
heading came in at the wrong level.

So the job isn't "produce HTML". It's **produce HTML that already matches
ProseMirror's schema**, and hand it over through a copy button rather than hoping
the browser serialises a Cmd+A selection the same way twice.

## The five things that actually break

All found by pasting into a real Substack draft, not by reasoning about the
schema. Every one of them fails silently.

**0. Relative image paths.** `src="images/01.jpg"` becomes `file:///…` on the
clipboard, and Substack cannot fetch local files, so every picture arrives as
"image not found". Inline each image as a `data:` URI before shipping the file —
then there is nothing left to fetch:

```python
b64 = base64.b64encode(pathlib.Path(src).read_bytes()).decode()
html = html.replace(f'src="{src}"', f'src="data:image/jpeg;base64,{b64}"')
```

Keep the original files in `images/` anyway: a large payload can still fail, and
dragging one file in is the fallback. `assets/paste-template.html` also puts a
small **Copy this image** button beside each picture (marked `data-nocopy` so it
never enters the payload) which copies that one image as PNG — the most reliable
per-image path when a bulk paste drops them.

**0b. No visual break between sections.** Substack drops the CSS margins that
separate sections on the source page, so everything runs together. Put an
explicit `<hr>` before each `<h2>` — it's a real ProseMirror node and comes
through as Substack's divider.

**1. `<pre>` inside `<li>`.** A code block is not valid inside a list item, so the
parser splits the list around it and the numbering restarts at 1. This is the
usual cause of "my numbered steps came out wrong".

Fix: don't put code blocks in lists. For a procedure with commands, number the
steps by hand as bold lead-ins and let the `<pre>` sit as a sibling:

```html
<p><strong>Step 2.</strong> Paste this into Terminal.</p>
<pre><code>the command</code></pre>
```

Manual numbers also survive the author reordering steps later in the editor,
which a real `<ol>` does not.

**2. Bare text inside `<li>` or `<blockquote>`.** The schema wants block content
in both. Bare text gets rewrapped inconsistently — quotes flatten into ordinary
paragraphs. Always wrap:

```html
<li><p>Item text</p></li>
<blockquote><p>Quoted text</p></blockquote>
```

**3. `<h1>` in the body.** H1 belongs to the post title, so a body `<h1>` gets
demoted or dropped. Use `<h2>` for section headings and bold lead-ins for
anything below that. Keep the title and subtitle out of the pasted payload
entirely — give them their own copy buttons for Substack's own fields.

## Copy synchronously, or the button dies in a sandbox

The order of the two clipboard paths is not a style choice. Copy from a detached
off-screen node with `document.execCommand('copy')` **first**, and only fall back
to `navigator.clipboard.write()` if that fails.

The reason: `execCommand` is synchronous, so it runs inside the click's
user-activation window. Anything after an `await` may have lost that window. Put
the async API first and you get a button that works on a local file and silently
does nothing once the page is published, because a published page is embedded in
a sandboxed iframe where the async clipboard call is often blocked — and by the
time it rejects, the gesture that would have authorised the fallback is gone.

Same ordering for per-image buttons: select the `<img>` and copy it synchronously
before trying the canvas-to-PNG clipboard route.

## Give it a copy button, not Cmd+A

`assets/paste-template.html` ships with one. It matters for three reasons:

- **Cmd+A grabs page chrome.** Any toolbar, instructions, or footer on the page
  lands in the draft. The template keeps the payload in `<article id="article">`
  and everything else outside it.
- **You control the markup.** The button serialises a cleaned clone — attributes
  stripped, `<li>`/`<blockquote>` children wrapped in `<p>` — rather than
  whatever the browser decides a visual selection means.
- **It writes real `text/html`.** Via `navigator.clipboard.write()` with a
  `ClipboardItem`, so the editor receives rich text, with a selection-based
  `execCommand` fallback for browsers that block the async API.

Verify the payload before handing the file over, by running `clean()` in the page
and checking the result: no `<h1>`, no `<pre>` inside `<li>`, no bare text nodes
in `<li>`/`<blockquote>`, no leftover `class`/`style`/`id`, no `<table>`. A clean
run should contain only h2, p, strong, em, ul, ol, li, blockquote, pre, code, a,
img, br, hr.

## Why an HTML page, never Markdown

Copying from a rendered web page hands the editor real formatting, so an `<h2>`
lands as a Substack heading and `<strong>` lands as bold.

Pasting a Markdown file does the opposite. Substack converts some Markdown
*as you type*, but pasted Markdown stays literal — the author gets `##` and `**`
scattered through the draft and has to reformat every heading by hand. Handing
over a `.md` file looks like a deliverable and is actually a chore.

So: produce an HTML file the author opens, selects all, and copies.

## What survives, what doesn't

**Survives the paste:** headings, bold, italic, links, bulleted and numbered
lists, blockquotes, code blocks, horizontal rules, images.

**Does not survive:** fonts, colours, spacing, custom layout — every bit of CSS.
Substack applies its own theme.

This is why the paste file's styling should be deliberately plain and *nothing in
it load-bearing*. Style it enough to proofread comfortably, then stop. A designed
paste file wastes effort on pixels that will be thrown away, and worse, it hides
structural problems that only appear once Substack restyles everything.

## Element whitelist

Use only these in the paste file body:

```
h1  h2  p  strong  em  ul  ol  li  blockquote  pre  code  hr  a  img  br
```

Two conversions are needed coming from any normally-structured article:

**`<h3>` → bold lead-in.** Substack gives you two heading levels in practice.
A third level pastes unpredictably. Convert sub-headings to a bold run followed by
`<br>`:

```html
<p><strong>3. Furniture isn't furniture.</strong><br>
In the file, the chairs and the table aren't separate things…</p>
```

This also matches the newsletter's own bold-lead-in habit, so nothing is lost.

**`<table>` → image.** Substack has no table support at all. A pasted table either
collapses into a run-on paragraph or vanishes. Render the table as a picture
instead:

1. Build the table in a styled HTML page.
2. Screenshot just the table element at device scale (Playwright's element
   screenshot, or any 2× capture).
3. Put the full figures in the image's `alt` text, so the data survives for screen
   readers and search even though the pixels don't.

Anything else built out of CSS — a boxed diagram, a pipeline strip, a stat tile —
flattens the same way. Convert it to a sentence, a list, or an image. A row of
labelled boxes usually reads fine as one bolded line with arrows.

## Title and subtitle

Substack has dedicated Title and Subtitle fields. Put both at the top of the paste
file as an `<h1>` and one italic paragraph, followed by an `<hr>`, and tell the
author to cut them into the proper fields and delete the rule. That's a few
seconds of work and it keeps the paste file readable as a standalone document.

## Images

Browsers differ in whether they put image bytes on the clipboard, so plan for both
outcomes:

- Reference images with relative paths (`images/01-….jpg`) so the paste file
  renders locally.
- Ship the files numbered in reading order so any that arrive broken can be
  dragged in.
- List which image goes where in `HOW-TO-PASTE.md`, anchored to a nearby sentence
  rather than a section number — sections get reordered, sentences don't.

Substack has a real caption field. Captions in the paste file should be marked so
the author knows to move them there rather than leaving them as body text.

## Deliverable shape

```
newsletter/
├── substack-paste.html
├── images/
│   ├── 01-….jpg
│   └── …
└── HOW-TO-PASTE.md
```

`HOW-TO-PASTE.md` should cover: the four-step paste, why HTML and not Markdown,
what survives, the image fallback table, and anything in the draft the author
should make their own before publishing (the sign-off especially).

**Publish the paste page itself as the artifact.** The obvious move is to publish
a nicely styled reading version and leave the paste file on disk — don't. The
author's actual job is getting the piece into Substack, and a local file they
have to hunt down is friction at exactly the wrong moment. The page with the
copy buttons is the one worth having behind a link; it reads perfectly well as
an article too, since the toolbar is small and sits above the content.

Give it the article's own name as the `<title>` (not "… paste source") so it
reads properly in the artifact gallery, and say plainly that the buttons should
be tested on the published link, since sandbox clipboard behaviour differs from
a local file.

Verify before handing over — it takes one script and catches real mistakes:

- No tags outside the whitelist in the body.
- Every `src` resolves to a file that exists.
- Open it in the browser so the author can read it before copying.
