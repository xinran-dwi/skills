# The Design with AI voice

Derived from published issues of the newsletter. The point of this file is to get
a draft into the right register on the first pass, because the gap between "a good
article" and "an article that sounds like this newsletter" is large and almost
entirely mechanical.

## Person and address

First person singular for experience, second person for instruction — often in the
same paragraph.

> I've been figuring out how to do this. You don't have to work it out yourself.

Never the editorial "we" for the author. "We" only appears in "here's what we'll
cover", where it means author-and-reader together.

## Tone

Conversational, warm, slightly self-deprecating. The stance is *a peer who just
did this and is telling you how it went* — not an expert issuing findings.

**Contractions are mandatory.** This is the single highest-signal marker. A draft
without them reads formal and distant no matter how good the content is:

| Wrong | Right |
|---|---|
| It is not a progress update | It's not a progress update |
| You do not need to know what they do | You don't need to know what they do |
| That is what makes this work | That's what makes this work |
| I did not write a brief | I didn't write a brief |

If you finish a draft and the contraction count is near zero, the register is
wrong and no amount of line-editing will fix it. Rewrite.

## Rhythm

Highly varied. Long explanatory sentences alternate with very short ones.
Single-sentence paragraphs carry emphasis and are used freely.

> Each of those was enough. And that surprised me.

> That's the thing I wanted to test.

> Look at the shape of that, because it's the useful bit.

Paragraphs run 1–5 sentences. Nothing dense. If a paragraph is over about six
lines on screen, it wants splitting.

## Headings

Imperative or action-oriented. They tell the reader what to *do* or what to *look
at*, not what the section is *called*.

| Flat | In voice |
|---|---|
| Setup | Set it up first |
| The loop | Watch the loop, not the prompt |
| Costs | Check what it cost |
| Lessons learned | Six things I got wrong |
| Conclusion | That's enough for now |

The opening heading is a question the article actually answers:

> What if you could redesign a room by just saying what's wrong with it?

Not a teaser, not a hook for its own sake — a real question, answered by the piece.

## Formatting habits

- **Bold lead-ins** to open a point, especially in lists of lessons.
- **Numbered steps** for anything procedural, with code blocks for commands.
- **Bulleted lists** for options, alternatives, and the "what we'll cover" opener.
- **Images after most sections**, with captions.
- **Em dashes** for asides — used often, and comfortably.
- **Exact prompts quoted verbatim**, typos included. These are gold: they show
  the reader how little precision was needed. Never clean them up.

## Explaining technical things

Introduce, then immediately clarify, in the same breath. Assume the reader knows
nothing and is not embarrassed about it.

> **Blender** is a free 3D program — think Figma, but for rooms and objects
> instead of screens.

> (A token is roughly three-quarters of a word.)

Analogies to tools designers already use (Figma, Sketch, Framer) work better than
precise definitions. Acronyms get established in context before being used, or
avoided entirely.

## Opening and closing

**Opening** poses the aspirational question, flags why it's hard, then sets up
what the piece will deliver. It earns the reader's next five minutes.

**Closing** is short, human, and unbothered. A note on what the thing does and
doesn't replace, then a sign-off. Past issues end with variations of "That's
enough for now" and "See you next time."

One caution: those exact sign-off phrases are the author's own. Use them as a
model for register, but flag them when you use them verbatim so the author can
make the closing theirs — a borrowed sign-off is the one line a reader is most
likely to notice as not-quite-right.

## Sample cadence

A passage that hits the register — note the contractions, the short opener, the
single-sentence paragraph, and the plain-language explanation:

> That's the thing I wanted to test.
>
> I had a 3D model of a two-bedroom flat sitting on my laptop — walls, furniture,
> kitchen, the lot. Normally, changing anything in it means opening Blender and
> pushing things around with a mouse. If you've ever tried that, you know it's a
> whole afternoon.
>
> So I tried something else. I connected Blender to Claude Code, and then I just…
> talked to it.

## Quick self-check before handing over

- Contractions throughout? (count them if unsure)
- Any heading that's just a noun? Rewrite it as an instruction.
- Any paragraph over six lines? Split it.
- Any term a non-coding designer wouldn't know, used without a definition?
- Are the original prompts quoted verbatim, typos intact?
- Does the closing sound like the author, or like a summary?
