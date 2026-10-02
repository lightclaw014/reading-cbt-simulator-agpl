# Authoring IELTS Reading tests

This app takes content in two forms:

1. **Markdown** (recommended — fast to write in any text editor)
2. **JSON** (the internal data model; useful for scripting/generation)

Load either one via the start screen: **Import test file**, drag-and-drop onto
the window, or **Paste test**. Once loaded, use **⬇ Export ▾ → Standalone file
for students** to bake the test into a single HTML file you can send to students.

Pasted text doesn't have to be just the test: an AI assistant's reply ("Here's
your test:", a closing remark, a ` ``` ` fence around the whole thing) is fine —
the app looks for the fenced block or the `# Test:` line and loads just that,
the same way for a pasted file, a dropped file, or the paste box.

---

## 1. The Markdown format

### Structure

```
# Test: <title>
time: <minutes>

## <Part label, e.g. "Part 1">
### Passage: <passage title>
<paragraph 1>

<paragraph 2>

### Questions: <type>
instructions: <shown above the group>
<type-specific meta lines, e.g. limit:, reusable:, options:>

Q. <question stem>
A. <answer>
W. <why / evidence note>   (optional)

Q. <next question stem>
A. <answer>
```

- Blank lines and extra whitespace are ignored except where they separate
  paragraphs (a blank line = new paragraph) or end an `options:` block.
- The parser is **strict about content it doesn't recognise** — any line it
  can't classify raises an error naming the line number. Nothing is silently
  dropped.
- Question numbers are assigned automatically, in file order, starting at 1.

### Top-level fields

| Line | Where | Meaning |
|---|---|---|
| `# Test: My Title` | first line | Sets the test title (and a URL-safe `id` derived from it) |
| `id: custom-id` | before first `## Part` | Overrides the auto-generated id (used as the localStorage key) |
| `time: 20` | before first `## Part` | Time limit in minutes (default 20) |
| `strand: listening` | before first `## Part` | Switches the test to the **listening** layout (default `reading`). See "Strands" below. |
| `time: 0` | before first `## Part` | No time limit: no clock, and nothing submits itself. What **Class work / homework** sets when you export. |
| `results: hidden` | before first `## Part` | Hides results from students (default is shown). On submit they see a confirmation + an answer code to send you; you still see full results via **View a student's answers** or a returned file. In the editor this is the **📊 Show results** checkbox. |

### Strands — Reading vs Listening

A test is one of two **strands**, set once at the top with `strand:` (default
`reading` if the line is absent):

- **`reading`** — the familiar **two-pane** screen: the passage on the left, the
  questions on the right, with a draggable divider. Every part needs a
  `### Passage:` block.
- **`listening`** — a **single column**: no passage pane at all, just the
  instructions and questions (e.g. a Part 1 notes task). Use this when the
  source material is audio, so there is nothing for the student to *read* on
  screen. In a listening test the `### Passage:` block is **optional**; if you
  include one it is kept as a **hidden transcript** (for your reference / the
  answer key / future audio) and is **never shown to the student**.

```
# Test: Section 1 — Accommodation enquiry
time: 30
strand: listening

## Part 1
### Questions: note
limit: NO MORE THAN TWO WORDS AND/OR A NUMBER
instructions: Complete the notes below.
H. Property
Q. type: ___ flat
A. ground-floor
T. available from 1 September
Q. rent: £ ___ per month
A. 650
```

In the visual editor, the strand is the **🎧 Reading / Listening** dropdown in
the top bar; switching to Listening drops the passage pane for students (the
editor keeps the passage box as the optional transcript). The choice
round-trips as the `strand:` line.

### Part / passage

```
## Part 1
### Passage: Study links early friendships with sibling relationships
First paragraph...

Second paragraph...
```

In the app, a test opens on **its own page**: the settings that apply to the
whole test, a card for each part, and the buttons that preview or export it.
Clicking a part's card opens that part; the arrow at its top left comes back.
**👁 Preview as student** and **⬇ Export** are at the foot of each part's screen
too, so you can export without going back to the test's page.
A part opens as a preview — the passage as students will read it, the questions
as they will answer them. Hover either side and an **✏ Edit passage** or
**✏ Edit questions** button appears in its corner; **✓ Done** returns it to
reading. Each side is independent, so you can rewrite a passage with its
questions still in front of you.

The `## ` heading is the part's **name**, and it can be anything on one line —
`## Section 2 — Accommodation` reads better than `## Part 2`, especially for
listening. In the editor, **✏ Rename part** (or a double-click on a tab) edits
it on its card, and dragging a card moves that part, with its passage and its
questions, somewhere else in the test. Parts you never name stay numbered automatically, and renumber
themselves when you add, delete or move one. Two names to avoid: a blank one
(it falls back to "Part n") and `Assets`, which is how the pictures section of
a file starts — the editor refuses that one.

A test can have as many `## Part` sections as you like. In a **reading** test
each part has exactly one passage (one `### Passage:` block) and one or more
`### Questions:` blocks; in a **listening** test the passage is optional (a
hidden transcript) — see "Strands" above.

Passage text can carry **glosses** (tap-a-word definitions) — see "Glosses"
below.

A part can also start with a `figure:` line (a picture for the whole part), and
any paragraph that is nothing but `![caption](#asset-id)` becomes a picture
inside the passage — see "Figures" below.

### Question groups

Each group starts with `### Questions: <type>` where `<type>` is one of:
`tfng`, `ynng`, `mcq`, `mcq_multi`, `completion`, `form`, `note`, `matching`,
`labelling`, `summary_drag`, `table_completion`, `flow_chart`, `open`.

Group-level meta lines (all optional except where noted):

| Line | Applies to | Meaning |
|---|---|---|
| `instructions: ...` | all | Instruction text shown above the group |
| `title: ...` | all (made for `flow_chart`, `table_completion`, `note`, `summary_drag`, `labelling`) | An optional **bold heading** over the group's content — above the first flow-chart box, the table, the notes, the summary, the diagram. See "Headings and line breaks" below. |
| `limit: NO MORE THAN TWO WORDS` | `completion`, `form`, `note`, `table_completion`, and any group in typed mode (see `input:` below) | Word-limit string shown to the student and **enforced** when grading. Not available on `open` — see below. |
| `reusable: true` / `false` | `matching`, `labelling` / `summary_drag` / `flow_chart` (bank mode only) | Whether a placed tile stays in the bank (`true`) or is consumed (`false`; **the default when the line is absent**). Classification and matching-features groups normally need `true`. Ignored (with a warning) if `display: dropdown` is also set. See "Reusable options" below. |
| `count: 2` | `mcq_multi` | How many answers to choose (inferred from the answer key if omitted) |
| `figure: <asset id>` | any type; **required** on `labelling` | A picture for this group, drawn above its questions (for `labelling`, the picture the answer boxes sit on). The id names an entry in the `## Assets` section; add `\| a caption` after it to print a caption. `image:` is accepted as an old spelling of the same line. See "Figures" below. |
| `display: dropdown` | `matching` only | Renders each question as a `<select>` instead of drag-and-drop tiles. See below. |
| `input: type` | `summary_drag`, `labelling`, `flow_chart` | Switches the group from the default word-bank (drag tiles) to **typed** answers (text boxes, graded like `completion`). Omit the line (or write `input: bank`/`drag`) to keep the word-bank default. See "Typed answering" below. |
| `options:` block | `matching`, `labelling`, `summary_drag`, `flow_chart` — **omit when `input: type` is set** (typed mode has no word bank) | The lettered list of options (see below) |
| `summary: ...` | `summary_drag` only | The summary paragraph; mark each gap with `___` (three or more underscores). See below. |
| `step: ...` | `flow_chart` only | One step-box's text, in chain order (one `step:` line per box); mark a gap with `___`. See below. |
| `answers: A \| B \| C` | `summary_drag` / `flow_chart` / `table_completion` | Word-bank mode: one option letter per blank. Typed mode (`summary_drag`/`flow_chart` with `input: type`, or `table_completion`, which is always typed): one accepted-answer entry per blank, alternatives separated by `/`. In all cases, order is reading order and this replaces `Q.`/`A.` lines. See below. |
| `columns: A \| B \| C` | `table_completion` only | The table's header row (cells split by `\|`). See below. |
| `row: cell \| ___ \| cell` | `table_completion` only | One line per table row (cells split by `\|`). Each `___` inside a cell is a blank — any number, anywhere in the text; `\___` is a literal. See below. |

### Question lines

Inside a group, each question is:

```
Q. <stem text>
A. <answer — format depends on type, see below>
W. <why note>        (optional but recommended)
E. <the words in the passage>   (optional — see "Evidence review" below)
```

`A.` answer formats by type:

| Type | `A.` line format | Notes |
|---|---|---|
| `tfng` | `TRUE`, `FALSE`, or `NOT GIVEN` | Case-insensitive on input, stored upper-case |
| `ynng` | `YES`, `NO`, or `NOT GIVEN` | |
| `mcq` | a single letter, e.g. `A.` → `B` — but the question also needs its own lettered options (see below) | |
| `mcq_multi` | letters separated by `\|` or `,`, e.g. `A. B \| D` | Answer letters refer to the group's shared `options:` list |
| `completion` / `form` / `note` | accepted answers separated by `\|`, e.g. `A. flightless \| non-flying` | Any one match is accepted; matching is case-insensitive and whitespace-trimmed. The three types are graded and formatted identically — see "Form vs Table completion" below for why there are three names. |
| `matching` | a single letter referring to the group's `options:` list | Works the same whether rendered as drag-and-drop tiles or a dropdown — see below |
| `labelling` (word-bank, default) | a single letter referring to the group's `options:` list | Also needs an `at: x, y` line — see below |
| `labelling` (`input: type`) | accepted answers separated by `\|`, like `completion` | Still needs an `at: x, y` line; no `options:` block. See "Typed answering" below. |
| `open` | **no `A.` line at all** | There's no single correct answer, so the parser raises an error if one is present. See below. |

### Headings and line breaks

**Line breaks: write `\n`.** Everything in a test file is one line per field
(a `Q.`, a `step:`, a `row:`…), so a break inside a field is written as the two
characters `\n`. It works in **every text field a student or the results screen
shows**: `instructions:`, `limit:`, `title:`, question stems, option text
(`mcq`, `options:`), `step:`, `summary:`, `columns:` and `row:` cells, notes
`H.` and `T.` lines, and the `W.` note shown in the results. (In a dropdown's
`<option>` list, where a menu cannot break, a break shows as a space; in the
Word export it is a space too.) `\\n` keeps a literal backslash-n. Text is
HTML-escaped before the break is added, so `<` and `&` are shown as typed.
In the **visual editor** you don't type `\n`: every one of those fields (and
table cells) is a multi-line box where **Enter**, **Shift+Enter**,
**Ctrl+Enter**, **Alt+Enter** or **Cmd+Enter** starts a new line, and the editor
writes the `\n` for you. (In the evidence/marking-note box, Enter also breaks
the line; finish with **Esc** or **Done**.)
Passage paragraphs are separate: they have their own paragraph and bold/underline
rules and are not affected.

```
instructions: Complete the notes.\nUse NO MORE THAN TWO WORDS.
Q. Sam's home is a ___ flat\nnear the station.
```

**Headings: `title:`.** An optional group-level line, drawn as a **bold heading
above the group's content**, and passed through the same line-break rule.
A group without it looks exactly as before. Where it goes:

| Type | The heading sits above… | Example |
|---|---|---|
| `flow_chart` | the first box (the word bank, if any, stays above it) | `title: How rain forms` |
| `table_completion` | the table | `title: Recycling schemes\nby city` |
| `note` | the first heading/line of the notes | `title: Visitor information` |
| `summary_drag` (bank or typed) | the summary paragraph | `title: The water cycle` |
| `labelling` (bank or typed) | the diagram | `title: Plan of the hive` |

```
### Questions: flow_chart
title: How rain forms
instructions: Complete the flow chart.
input: type
limit: ONE WORD ONLY
step: Heat makes water ___.
step: Vapour rises and forms ___.
answers: evaporate | clouds

### Questions: table_completion
title: Recycling schemes\nby city
limit: ONE WORD ONLY
columns: City | Scheme
row: Leeds | kerbside ___
answers: boxes

### Questions: note
title: Visitor information
limit: ONE WORD ONLY
H. Opening hours
Q. Open from 9 a.m. until ___
A. noon

### Questions: summary_drag
title: The water cycle
input: type
limit: ONE WORD ONLY
summary: Water ___ from the sea.
answers: evaporates

### Questions: labelling
title: Plan of the hive
figure: hive-diagram
input: type
limit: ONE WORD ONLY
Q. Where nectar collects
at: 62, 40
A. chamber
```

Any other group type accepts `title:` too and draws it the same way. In the
visual editor it is the **Title** box on those five types.

### Reusable options (`reusable:`)

For the word-bank types (`matching`, `labelling`, `summary_drag`, `flow_chart`
in bank mode) `reusable:` decides what happens to an option when the student
places it:

- **`reusable: true`** — dragging from the bank puts a **copy** in the slot and
  leaves the original in the bank, so the same letter can fill any number of
  slots. Dragging a placed copy to another slot moves only that copy; clearing
  a slot (click it, or Delete) deletes the copy and returns nothing, because the
  bank never lost anything. Flagging, saved progress, the review screen and the
  score all work with the same letter in several slots.
- **`reusable: false`** — an option is used up once placed and comes back to the
  bank when its slot is cleared. **This is the default: if the line is absent,
  the group behaves as `false`.**

Classification groups ("write A, B or C — you may use any letter more than
once") and matching-features groups **normally need `reusable: true`**: their
answer key repeats letters and often has more items than options, which a
use-once bank can't satisfy. (A `display: dropdown` group never consumes
options, so the flag does nothing there.)

```
### Questions: matching
reusable: true
instructions: Which mammal does each statement describe? You may use any letter more than once.
options:
A. Bat
B. Whale
C. Mole
Q. Uses echolocation in the air
A. A
Q. Lives underground
A. C
Q. Uses echolocation in water
A. B
Q. Flies at night
A. A
```

**Warning.** If a group is `reusable: false` (or has no `reusable:` line) and its
key **repeats a letter**, or it has **more items than options**, the test still
loads, but the teacher gets a warning naming the file, the group and the
problem — for example *"regression-test.md, Part 1, group 9 (matching):
'reusable: false' (the default), but its answer key repeats the letter A and it
has 3 items but only 2 options…"*. It appears in the import notice, in the
**Before you send it out** list on the test's page (the teacher's view), and in
the browser console — never to students, and it never blocks loading. The fix
is nearly always to add `reusable: true`.

### Evidence review — "where should I have looked?"

After submitting, every row of the detailed results table is clickable. Clicking
one goes back into the locked test at that part and **paints the words the
question was answered from**, with a chip naming the question and a way back to
the table. It is the moment that teaches scanning: the student sees where the
answer was, not just that they missed it. A listening test reveals its
transcript for this, since the test is over.

You don't have to write anything new for it. The app looks in four places, in
order:

1. An **`E.` line** on the question — the exact words from the passage.
2. **A quotation inside the `W.` note.** This is why `W. Para 1: "followed just
   over four hundred families"` is worth writing that way: the quote is found
   and painted.
3. **A paragraph the note names** — `W. Para 3 states this…` outlines paragraph
   3 rather than a sentence. Paragraphs are counted as a reader counts them, so
   a picture in between doesn't shift the numbering.
4. Nothing: the item says "no evidence marked for this one" rather than guess.

So add an `E.` line only where the note paraphrases instead of quoting:

```
Q. The researchers proved that sibling relationships cause friendship quality.
A. NOT GIVEN
W. The authors are careful never to claim this.
E. the finding does not establish causation
```

Quotes are matched loosely — curly or straight, any spacing, any case — but the
words themselves must appear in the passage.

### `CHECK:` and `UNCONVERTED:` — flags left by the AI wizard

The **🤖 Generate with AI** wizard (see the start screen) can write a `W.` note
that begins with one of these two words when it isn't sure of itself:

- **`CHECK:`** — you didn't give it an answer key, so it worked the answer out
  from the passage itself.
- **`UNCONVERTED:`** — you gave it your own question, but it fit none of the
  question types, so it became an ungraded `open` question instead.

These aren't a format requirement — you'll never need to write them by hand —
but if a test has any, its page lists them under "Before you send it out" with
the question numbers, so a guessed answer doesn't quietly ship to a class.
Check the question, then delete the word (and the colon) from the note: the
rest of the note is what students see in the evidence window.

### The `open` type — free-text, not IELTS-specific

Use `open` for anything that can't be graded by exact match: opinion
questions, "explain in your own words", short-answer prompts, discussion
questions — in any subject, not just IELTS reading.

```
### Questions: open
instructions: Answer the questions below in your own words.

Q. Who uses social media more — Emma or Jack?
W. Emma: posts daily, shops online. Jack: checks weekly, reads only.

Q. Which person uses social media in a healthier way? Why?
W. Open — accept any answer with a reason from the passage.
```

- `Q.` is the question stem — the only required line.
- **No `A.` line.** The validator raises a clear error naming the line
  number if one is present, because `open` questions have no single correct
  answer to check against.
- `W.` is optional and becomes a **marking note for you**, not evidence
  shown to the student during the test — a reminder of what a good answer
  should cover, so you can grade quickly later.

The student gets a growing multi-line text box (about 3 rows, expanding as
they type) — no word limit, no live validation. Their response is always
recorded, but:

- It's **excluded from the raw score and from the scoring denominator.** A
  test with 24 items of which 5 are `open` reads "x / 19", not "x / 24".
- It's **excluded from band-score conversion entirely.**
- It still gets a number and appears in sequence in the navigation bar and
  question list, like any other item — but with a dashed outline, and a
  small purple dot (instead of the usual blue fill) once it's been answered,
  so it's visually distinct from graded questions at a glance.

On the results screen, `open` questions don't appear in the main scored
table at all — they get their own section headed **"Written answers (not
scored)"**, listing the question, the student's response, and your marking
note. This section is included in the PDF and Word report, and — because a student's
typed responses are ordinary saved answers like any other question type —
it's automatically included in the baked-in data of their downloaded
completed file, so you see exactly what they wrote when you open it.

Because a whole test can be a mix of group types, you can drop one or more
`open` groups into an otherwise auto-graded IELTS-style test (e.g. a
reflection question at the end of a part), or author an entire test made
only of `open` groups for a completely different kind of exercise — a
discussion worksheet, a reading-response journal, etc. In that case the
score/band/percentage cards show "—" (nothing to grade) and the results
screen is just the "Written answers" section.

### The `matching` dropdown display

By default, `matching` renders as drag-and-drop tiles (a bank of lettered
tiles above the questions, dragged — or click-to-place — into drop zones).
Add `display: dropdown` to render each question as a plain `<select>`
instead, listing the group's options as "A — Emma", "B — Jack", etc.:

```
### Questions: matching
reusable: true
display: dropdown
instructions: Which person does each statement describe?
options:
A. Emma
B. Jack
C. Both Emma and Jack

Q. rarely uses social media
A. B
W. Jack says he checks it about once a week.
```

This is presentation only — the answer format, grading, results table, and
JSON model are all identical to the default drag-and-drop rendering; only
how the student interacts with it changes. A few things to note:

- Omit `display:` entirely (or leave it unset) to keep the existing
  drag-and-drop behaviour, unchanged.
- A dropdown's option list is always fully available in every question, so
  `reusable` doesn't apply once `display: dropdown` is set. If you write
  `reusable: false` together with `display: dropdown`, the app ignores
  `reusable` and shows a warning when the test loads (it still loads —
  this isn't a fatal error, just a heads-up that the line has no effect).
- The dropdown works the same as any other answer with the resume-from-
  refresh (`localStorage`) flow, and with the locked/review state after
  submission (disabled, but still showing the chosen option).

For `mcq` questions, list the four options as their own lines directly under
`Q.`, before `A.`:

```
Q. What is the main cause of the decline?
A) Habitat loss
B) Introduced predators
C) Disease
D) Climate change
A. B
W. Para 2.
```

`labelling` means one thing only: **answer boxes sitting on a picture.** Every
`labelling` group needs a `figure:` line, and every question in it needs an
`at:` coordinate line (percentages, 0–100, from the top-left of the picture)
saying where its box goes:

```
### Questions: labelling
figure: hive-diagram
options:
A. Honey storage cells
B. Brood area
C. Base of the comb

Q. Chamber where nectar collects
at: 62, 40
A. C
W. Diagram, right-hand chamber.
```

Use `labelling` (with typed answers via `input: type`) for **flow-chart, chart,
map, and diagram completion**: insert the picture and place a numbered blank
over each gap the student must fill.

If the picture already prints its own questions and numbered blanks — a scanned
IELTS diagram, say — don't use `labelling`. Put the picture on an ordinary
`completion` (typed) or `matching` (word-bank) group with a `figure:` line, and
the picture is drawn above the answers. That is what the retired `display: list`
option used to do, and old tests are converted to exactly this on load; see
"Old tests: `display: list`" below.

### Figures — pictures in a test

A picture can go in three places, and the same picture can go in all three
without being stored more than once:

| Where | How to write it | What the student sees |
|---|---|---|
| **A whole part** | a `figure:` line under `## Part 1` | Above the passage (reading) or in a pinned panel at the top of the part (listening) |
| **Inside the passage** | a paragraph that is only `![caption](#asset-id)` | Between the paragraphs, exactly where you put the line |
| **One question group** | a `figure:` line inside `### Questions: <type>` | Between the instructions and the questions. On `labelling`, this is the picture the answer boxes sit on. |

```
## Part 1
figure: ferry-plan | Figure 1: the terminal, from above
### Passage: Getting to the island

First paragraph...

![Figure 2: the timetable board](#timetable)

Second paragraph...

### Questions: completion
figure: timetable
limit: ONE WORD

Q. Departures are listed under ______.
A. destination
```

Both the part line and the group line take `asset-id | caption`; the caption is
optional. In the passage the caption is the `![...]` text. Any student can click
a picture (or press Enter on it) to see it full-screen.

**Listening parts** show the part figure in a panel pinned to the top of the
questions, since there is no passage beside it. The panel can be collapsed and
zoomed, and it remembers that per part for the rest of the attempt, so a student
working through a long map-labelling section doesn't have to keep scrolling back.

### The `## Assets` section

The pictures themselves live in an `## Assets` section at the **end** of the
file, so the (very long) base64 never buries the test you are trying to read.
Everything above refers to them by id:

```
## Assets

### Asset: ferry-plan
alt: A plan of the ferry terminal, with the café on the left
width: 1200
height: 800
src: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...
```

| Line | Meaning |
|---|---|
| `### Asset: <id>` | The id other lines point at. Letters, digits, `.`, `_`, `-`, starting with a letter or digit; unique within the test. |
| `alt:` | Optional. What the picture shows, for screen readers and for when it fails to load. The editor doesn't ask for it — the caption does that job — but a file that has one keeps it. |
| `src:` | A `data:` URI (embedded — recommended) or a plain URL. |
| `width:` / `height:` | Optional, in pixels. The app writes them; it only uses them to reserve space. |

**Why ids rather than the picture itself.** A test is one self-contained file,
so a picture used by three groups used to be stored three times. Now it is
stored once and referred to three times — in the Markdown, in the JSON, in an
exported student file, and in a returned attempt. One real test in the library
went from 323 KB to 165 KB simply by being loaded and saved again.

`src:` can be:

- **A `data:` URI (embedded — recommended).** The picture ships *inside* the
  single exported HTML: students open it offline with nothing else to download.
- **A plain URL** (`https://example.com/chart.png`). Convenient while drafting,
  but the student's browser fetches it live, so it needs internet and the link
  must stay reachable. Swap it for an embedded file before sending the test out.

### Adding pictures in the editor

You will rarely type any of the above by hand. In the visual editor:

- A part and every question group have a **📷 Add picture** button. Clicking it
  opens a small window: paste (Ctrl+V), drag a file in, choose a file, or reuse
  a picture the test already has, and write the caption. Once a picture is set,
  a slim chip beside the button shows which one it is — click either to change
  or remove it. Nothing else takes up room while a part has no picture.
- **Inside the passage**, paste or drag a picture straight into the text: it
  lands as its own paragraph where the caret is. Click the chip to take it out
  again (the picture stays in the test).
- Every picture is **shrunk to 1600px on its longest side and re-encoded as
  JPEG** on the way in (the original is kept if it was already smaller), then
  **hashed**: paste the same picture twice and the second paste just points at
  the first one. The window says what it added, and warns above 500 KB.
- **📷 View pictures** (in the top bar) opens a window listing every picture in the test with
  its thumbnail, id, size, and what uses it. From there you can rename the id
  (every reference follows), replace the file, jump to a use, or delete one that
  nothing points at.
- A `labelling` group's button says **📷 Add the diagram — needed**, because
  that type has nowhere to put its answer boxes without one.

The editor never asks you to describe a picture for screen readers. The
**caption** is what a screen reader reads out, so write one where it matters. A
description already in a test file (`alt:`) is kept, saved back, and used ahead
of the caption — it just isn't one more box to fill in.

### Old tests: `display: list`

`display: list` on a `labelling` group (answer boxes in a numbered list *below*
the picture) has been retired — it did the same job as an ordinary completion
or matching group with a picture on it, with its own separate code path.

Old tests keep working: when one loads, each `display: list` group is converted
in place and the app tells you what it did.

| Was | Becomes |
|---|---|
| `display: list` + `input: type` | a `completion` group with the picture above it |
| `display: list` (word bank) | a `matching` group with the picture above it |

Question numbering, answer keys, and grading are untouched. Two details worth a
look afterwards: `at:` coordinates are dropped (nothing sits on the picture any
more), and any question whose `Q.` stem was blank — allowed in the old list
mode, because the picture printed the question — gets a `Gap 1`, `Gap 2`
placeholder you will probably want to rewrite. Save the test to keep the
conversion; the warning appears on every load until you do.

Old `labelling` groups that put their boxes *on* the picture are not touched,
and `image:` still parses everywhere `figure:` does.

### The shared `options:` block (matching / labelling)

Placed once per group, right after the meta lines:

```
### Questions: matching
reusable: false
instructions: Match each researcher with the correct finding.
options:
A. Finding one
B. Finding two
C. Finding three

Q. Kramer
A. B
W. Para 3.
```

A blank line ends the `options:` block.

**Option letters are read forgivingly.** Write them as `A.` here and as `A)`
under a `Q.` in an `mcq`, which is what the editor writes back. But either
spelling is accepted in either place, and a lowercase letter (`e.`, `e)`) is
read as `E` — an AI listing options often slips mid-list. In an `mcq`, a dotted
line is only taken as an option while the options are still being listed: it
must be the next letter, and come before the `A.` answer line, so `A.`, `W.`
and `E.` keep their meanings.

### Typed answering (`input: type`)

`summary_drag`, `labelling`, and `flow_chart` all default to a **word-bank**
answer model: a bank of lettered tiles the student drags (or click-to-places)
into drop zones, with a group-level `options:` list as the bank's contents.

Add `input: type` as a group-level meta line (right after `instructions:`, or
anywhere before `answers:`) to switch the group to **typed** answers instead —
a text box at each blank, graded like `completion` (case-insensitive,
whitespace-trimmed, accepts any one of a `|`-separated alternatives list, and
respects the group's `limit:`). In typed mode:

- **Omit the `options:` block** — there's no bank, so it's not read.
- Each blank's answer becomes an accepted-answers list instead of a letter:
  in an `answers:` line, alternatives within one blank are separated by `/`
  (blanks themselves still separated by `|`); on a `labelling` question's own
  `A.` line, alternatives are separated by `|` (matching the `completion`
  format, since each label is a single Q./A. pair, not a shared `answers:` line).
- `reusable:` no longer applies (there's no bank to consume from).

```
### Questions: summary_drag
input: type
limit: NO MORE THAN TWO WORDS
summary: The kākāpō is a heavy, ___ parrot from New Zealand. When threatened it ___.
answers: flightless / can't fly | freezes / stays still
```

```
### Questions: labelling
input: type
figure: hive-diagram

Q. Chamber where nectar collects
at: 62, 40
A. nucleus | cell nucleus
```

Switching the toggle in the visual editor's "How students answer" control
resets that group's answer keys (the shape changes from letter to accepted-
list or back), since the old values can't mean anything under the new mode.

### Questions: summary_drag

A summary paragraph with gaps the student fills by dragging lettered phrases
from a bank into each blank. Same answer model as `matching` (one option
letter per blank), but there are **no `Q.`/`A.` lines** — instead use a
`summary:` line (mark each gap with `___`, three or more underscores) and an
`answers:` line (one letter per gap, in order).

```
### Questions: summary_drag
reusable: false
instructions: Complete the summary. Drag the correct phrase into each gap.
options:
A. flightless
B. freezes
C. mammals
D. predator-free
E. hunts
F. crowded

summary: The kākāpō is a heavy, ___ parrot from New Zealand. When threatened it ___. Introduced ___ nearly wiped it out, so every bird was moved to ___ islands.
answers: A | B | C | D
```

Notes:

- The number of `___` gaps must equal the number of letters in `answers:`
  (the validator checks this).
- Put **more options than gaps** to add distractors (here E and F are unused).
- With `reusable: false` (default) each phrase can fill only one gap; set
  `reusable: true` to let a phrase be used in more than one gap.
- The summary is one logical line. In the visual editor it can span several
  lines; on export to Markdown it is flattened to a single `summary:` line.
- In the visual editor, the number of answer selectors follows the number of
  `___` gaps you type automatically — you don't manage numbering by hand.

### Questions: table_completion

A grid where cells hold text with fill-in blanks the student **types** into
(graded like `completion`, with an optional word `limit:`). There are **no
`Q.`/`A.` lines** — instead give a `columns:` header line, one `row:` line per
row (cells split by `|`), and an `answers:` line with one accepted answer per
blank in **reading order** (left-to-right within a row, then top-to-bottom
across rows). Use `/` for alternative accepted answers within a blank.

**Blanks may appear anywhere inside a cell**, written as `___` (three or more
underscores). A cell may contain any number of blanks mixed freely with text —
mid-sentence, several in one cell, or none at all — which is how real Cambridge
tables embed numbered gaps in prose. A cell that is exactly `___` (the whole
cell) is one blank, exactly as before.

```
### Questions: table_completion
limit: NO MORE THAN ONE WORD
instructions: Complete the table below.
columns: City | Positive aspects | Negative aspects | % of help received
row: Rio de Janeiro | friendly inhabitants; more ___ lifestyle | People don't have so much ___ . Has reputation for ___ . | 93%
row: Amsterdam and New York | richer | People have little ___ . People don't pay attention to ___ . | Amsterdam: 53%; New York: 44%
answers: relaxed | money | crime | time | strangers
```

Here the first row's *Positive aspects* cell has one inline blank and its
*Negative aspects* cell has two; the second row's *Negative aspects* cell has
two; the other cells have none. That is **five** blanks, numbered in reading
order, mapped to the five `answers:` entries in that same order. A whole-cell
`___` (as in `row: London | ___`) still works and counts as one blank.

Notes:

- The number of `___` blanks (across all cells, inline included) must equal the
  number of entries in `answers:` (the validator checks this and names the
  group), and every `row:` must have the same number of cells as `columns:`.
- Alternatives for one blank use `/`, e.g. `answers: 1650 | London / the City`.
- **Literal underscores:** to keep a run of underscores as text instead of a
  blank, escape it with a backslash — `\___` renders as a literal `___` and is
  not counted or graded.
- **Several lines in one cell:** a `row:` is one line of the file, so write `\n`
  where a cell's text should break — `row: reduced | • use ___ \n • bring a ___`
  is one cell with two lines (the same `\n` rule as every other text field, see
  "Headings and line breaks"; `\\n` keeps a literal backslash-n, and column
  headings break too). In the visual editor just press **Enter** — or
  Ctrl+Enter, Ctrl+Shift+Enter or Alt+Enter — inside the cell; the editor writes
  the `\n` for you.
- In the visual editor you build the grid directly: add/remove columns and
  rows, and **type `___` into a cell** wherever a blank should go — the accepted
  answer boxes below follow the total blank count automatically. Numbering is
  handled for you.

### Questions: flow_chart

A vertical chain of step-boxes joined by `↓` arrows — for describing a process
or sequence. Some steps contain a `___` blank the student fills by **dragging
from a word bank** (default) or, with `input: type`, by **typing**. There are
**no `Q.`/`A.` lines** — instead give one `step:` line per box (in chain
order; `___` marks a blank) and an `answers:` line, one entry per blank in
reading order (top step to bottom, left-to-right within a step).

```
### Questions: flow_chart
instructions: Complete the flow chart below.
options:
A. nitrogen
B. bacteria
C. ammonia

step: Plants absorb ___ from the soil.
step: It is converted into ___ by bacteria in the roots.
answers: A | C
```

Typed instead of word-bank — omit `options:`, add `input: type`:

```
### Questions: flow_chart
input: type
limit: NO MORE THAN TWO WORDS
step: Plants absorb ___ from the soil.
step: It is converted into ___ by bacteria in the roots.
answers: nitrogen | ammonia
```

Notes:

- The number of `___` blanks across all `step:` lines must equal the number
  of entries in `answers:` (the validator checks this).
- Word-bank mode: `answers:` holds one option letter per blank; `reusable:`
  applies the same as `summary_drag` (default `false` — each phrase fills one
  blank only).
- Typed mode: `answers:` holds one accepted-answer entry per blank,
  alternatives within a blank separated by `/`; `reusable:` doesn't apply.
- In the visual editor, steps have their own add/remove/reorder controls, and
  the answer editors below follow the blank count automatically.

### Form vs Table completion — which to use

Both types produce **typed, word-limit-graded blanks** (one point per blank,
case-insensitive, alternatives allowed). They differ only in **layout**, so
pick by how you want the fields to sit on the page:

| You want… | Use | How it looks |
|---|---|---|
| A field **label with its blank below it**, one numbered item per field (the standard IELTS form look) | `form` | `[n]  Surname:` on one line, the answer box on the next line under it |
| Label and blank **side-by-side on the same row**, in a grid with column headers | `table_completion` | a real grid — a label cell and a blank cell in the same row |

Important: `form` is the **same engine as `completion`** — there is no special
two-column form widget. The field label is simply each question's stem, and the
answer box always renders on its own line *below* the stem. The `___` you put in
a `form` stem (e.g. `Surname: ___`) is cosmetic; the graded box is the one under
it. So if you need the label and the blank on the *same* line, that's
`table_completion`, not `form`.

`form`, `note` and `completion` are identical in grading and layout — they exist
as separate names only so the right one shows up in the editor's type dropdown
and reads correctly to the student. Choose whichever label fits the task.

**Headings inside a form.** There's no separate heading line between questions.
To group fields under headings, either put the heading in the group's
`instructions:` line, or start a **new group** (still `form`) per section — e.g.
one `form` group for "Personal details" and another for "Booking details". Both
groups keep numbering continuous across the test automatically.

```
### Questions: form
limit: NO MORE THAN ONE WORD OR A NUMBER
instructions: Complete the form below.

Q. Surname: ___
A. Fletcher

Q. Date of birth: ___
A. 12 May 1990 | 12/05/1990
```

### Structured notes (`note` with headings and context lines)

A plain `note` group is just sentence completion under a different label — a
flat list of numbered blanks. But the classic IELTS **note-completion** task
(common in Listening) is a *structured* note: sub-headings, some detail lines
that carry a numbered gap, and other detail lines that are just context with
**no gap at all**. A `note` group supports this with two extra line prefixes,
usable **only inside a `note` group** and mirroring the `Q./A./W.` convention:

| Line | Renders as | Numbered? | Graded? |
|---|---|---|---|
| `H. <text>` | a **bold, flush-left heading** | no | no |
| `T. <text>` | an **indented context line** (a "–" bullet, no answer box) | no | no |
| `Q./A./W.` | the usual numbered blank (an inline box at the `___`) | yes | yes |

Lines render **in source order**, so you interleave them exactly as they should
appear. Only `Q.` lines consume a number; `H.`/`T.` lines never do.

```
### Questions: note
limit: NO MORE THAN TWO WORDS AND/OR A NUMBER
instructions: Complete the notes below.

H. Dining table:
Q. ___ shape
A. round
T. medium size
Q. ___ old
A. very
T. price: £25.00

H. Dining chairs:
Q. set of ___ chairs
A. four
Q. seats covered in ___ material
A. leather
T. price: £20.00

H. Desk:
T. length: 1 metre 20
Q. 3 drawers. Top drawer has a ___.
A. lock
Q. price: £ ___
A. 15
```

Notes:

- A `note` group with **no `H.`/`T.` lines** behaves exactly as before — a flat
  numbered list, identical to `completion`. The structure is opt-in.
- The numbered blanks are graded like any completion blank (case-insensitive,
  `limit:`-enforced, `|`-separated alternatives on the `A.` line). `T.` and `H.`
  lines are display-only — never scored, never given a number.
- Internally this becomes a group-level `layout` array (heading / text / blank
  tokens); the number of blank tokens must equal the number of questions (the
  validator checks this, and it round-trips back to `H./T./Q.` on export).
- This is the notes *layout* only — there is no audio player yet, so a "listening"
  test still needs its transcript/context in the `### Passage:` block for now.

### Glosses (tap a word to see its meaning)

A **gloss** lets a student tap a word in the passage and see a small box with an
English definition, an example sentence, and (behind a **Vietnamese** button) a
Vietnamese translation. Glossed words have a dotted underline.

**English, Vietnamese, or both.** Each gloss has whichever you give it, and
the box shows just that:

| The gloss has | What students see when they tap the word |
|---|---|
| **Both** | The English definition (and example) first, with a **Vietnamese** button underneath. |
| **English only** | The English definition (and example). No button. |
| **Vietnamese only** | The Vietnamese translation (and the example, if you wrote one). No button. For a class too young to read the English side, leave the English — and usually the example — blank. |

**Glosses show wherever you write them** — in the editor, in **Preview as
student**, and in a test started from the start screen. There is no switch per
part. The one place to turn them off is the export window: **📘 Class work /
homework** keeps them, **📝 Test** turns them off, and the **Glosses** switch
there lets you choose either way. That changes the downloaded file only — the
test in the editor keeps its glosses.

**Answer words** have a switch of their own:

| Switch | Where | When to use it |
|---|---|---|
| **🔑 Show answer words** | On the test screen, in the grey bar above the passage. It only appears **after the test is submitted** (on the results screen, press **Review answers in the passage**). | **Answer checking.** When you go through the answers together, turn it on to show the words the questions are built on. You can use it on your projected screen, and students can use it on their own devices after they submit. It works whether the file's glosses are on or off. |

Students can never see "Show answer words" during the test. (In a test with
`results: hidden`, students never return to the passage after submitting, so
they don't get this switch — you still do, when you open their work.)

**Adding and changing glosses in the editor (the easy way).** You never need
to type any special codes:

- **Add one:** select (highlight) a word or phrase in the passage. A small
  **📖 Add gloss** button pops up over your selection — click it (or
  right-click the selection and choose **📖 Add gloss**). Selecting with the
  keyboard (Shift and the arrow keys) pops the same button. Fill in the English
  definition, the Vietnamese, or both (the
  example is optional), tick **🔑 Answer word** if a question tests that word,
  and click **Save**. **Cancel** leaves the word as it was. If you select only
  part of a word, the whole word is taken.
- **A phrase with a gap** (a collocation with its object in the middle, such as
  *take* ~~the weather~~ *into account*): select the whole stretch, "take the
  weather into account", and choose Add gloss. The form shows each word as a
  button — click **the** and **weather** to leave them out. The gloss becomes
  "take … into account": students see both parts underlined, and tapping
  either part opens the same box. (A word that sits in the gap can't have a
  gloss of its own.)
- **Bold or underline a glossed word** (key or not): click the word and press
  **Ctrl/Cmd+B** or **Ctrl/Cmd+U** (or use the **B** / **U** buttons under
  "Format the word"); it changes at once. You can also select text that includes
  glossed words and press the same keys. A phrase with a gap formats every part. In a file the word may carry the same limited HTML a
  passage allows: `{{<b>declined</b>|giảm|became lower|key}}`. (Bold you put
  *around* a glossed word with the toolbar also works. Formatting *inside* a
  gloss used to be dropped whenever the passage was saved.)
- **Right-click a glossed word** for **Edit gloss** / **Remove gloss**.
- **Change or remove one:** click the underlined word. The same box opens, with
  a **Remove gloss** button (the word itself always stays in the passage).
- **See them all:** click **📖 View glosses** in the top bar. A window opens
  in the middle of the screen listing every gloss in the part, with **Edit**,
  **Go to** (jumps to the word and flashes it) and **✕** (remove). Close it
  with **✕** or Esc, by clicking outside it, or by clicking
  **📖 View glosses** again. **Edit**, **Go to** and **Find in passage**
  close it for you, since each of them hands you back to the passage; **✕**
  does not, so you can tidy several glosses in one go.
  - Words marked in **red** are unfinished (a definition or the Vietnamese is
    missing). Students see them as plain text until you finish them. You also
    get a reminder when you press Preview as student or Export.
  - 💡 **"answer word?"** means the word appears in a question's evidence note
    (`W.`) — a hint that it may be an answer word. You decide.
- **From a word list:** in the 📖 View glosses window, paste your words (one per line,
  or separated by commas) and click **Find in passage**. Each word is found (the
  first time it appears) and marked in red; then click each one to fill it in.
  You're told which words were already glossed and which weren't found. For a
  phrase with a gap, type three dots: `take ... into account`.

In the editor a gloss behaves as one piece: you can't accidentally delete half
of it. To change the word itself, remove the gloss, edit the text, and add the
gloss again.

**Glosses from 🤖 Generate with AI.** The wizard asks whether you have a list
of words to gloss. With a list, the AI glosses exactly those words. Without one,
it asks whether the AI should choose the words itself: pick your students'
level (A1, A2, B1 or B2) and the AI glosses at most 10 words above that level in
each passage, favouring the ones needed to follow the passage, and marks the
words the questions test as `key`. Answer No and the test comes back with no
glosses, for you to add in 📖 View glosses. Either way, check the AI's glosses
in 📖 View glosses before you give the test out.

**How a gloss is written in a file** (for Markdown files, JSON, or the AI
authoring tool — the editor writes this for you). It goes inside the passage
text, in double curly brackets, with the parts separated by `|`:

```
{{word in the passage|Vietnamese translation|English definition|ex: example sentence|key}}
```

- The word, exactly as it appears in the passage, is **required**. So is at
  least one of the next two — the Vietnamese translation and a simple English
  definition. Leave the other one empty but keep its `|`, so each stays in
  its place: `{{declined|giảm|}}` is Vietnamese only, `{{declined||became
  lower}}` is English only.
- `ex:` is **optional**: an example sentence.
- `key` is **optional**: see below.
- The word can be a phrase of several words — it is glossed as one unit.
- To use a `|` inside a definition or example, write `\|`.
- Glosses work **only in the passage**. They don't change how answers are
  written in the questions (where `|` still separates accepted answers).

**A normal gloss:**

```
Farmers had to {{take into account|tính đến|consider something when you make a decision|ex: Please take the weather into account.}} the cost of fuel.
```

Students see "Farmers had to take into account the cost of fuel." with a
dotted line under *take into account* (when Glosses is on for that part).

**A phrase with a gap.** Put the full gloss on the first part, and mark each
later part with `{{+…}}` — a plus sign and the words, nothing else. A `{{+…}}`
belongs to the nearest gloss before it in the same paragraph:

```
Farmers had to {{take|tính đến|consider something when you make a decision|ex: Please take the weather into account.}} the weather {{+into account}} when planning.
```

Students see both *take* and *into account* underlined; tapping either opens
one box headed "take … into account". Don't put another gloss between the
parts (in the gap) — the `{{+…}}` would join that one instead.

**What `key` means.** Add `key` to a word or phrase that a question tests or
paraphrases — the word a student has to find to get the answer. For example,
the passage says prices **declined** and the question says prices **fell**, so
*declined* is a key word:

```
Coffee prices {{declined|giảm|became lower in amount or level|ex: Sales declined after the holiday.|key}} last year.
```

Key glosses stay hidden during the test — the word looks like plain text even
when Glosses is on, so it doesn't give the answer away. They appear (with a
green tint) only when someone turns on **Show answer words** after submitting.

**If a gloss is written wrongly** (for example, a part is missing), the word
shows as plain text and the rest of the page works as normal. You get a warning
when the test loads, the editor counts them — "📖 Glosses (6 found, 2 key,
1 unfinished)" — and the 📖 View glosses window lists each one so you can fix it.

Older files may have a `glosses: on` or `glosses: off` line under a part
heading. It came from a per-part switch that has since gone; the app reads
the line and ignores it, and doesn't write it any more.

### Full worked example of every type

Two sample files ship with the app, and between them they use every feature:

- [`sample-test.md`](sample-test.md) — a three-part **reading** test with all
  eleven reading question types, glosses (including a key word and a split
  phrase), figures at part, passage and group level with one picture used
  twice, a typed-mode labelling group, and the `## Assets` section.
- [`sample-listening.md`](sample-listening.md) — a **listening** test: hidden
  transcripts, a part figure pinned above the questions, a plan-labelling
  group, structured notes and a dropdown matching group.

See [`sample-test.md`](sample-test.md) for a complete file exercising every
question type — including `open`, a dropdown-mode `matching` group, and
figures at all three levels (one of them used twice, stored once) with the
`## Assets` section at the end.

---

## 2. What a test looks like inside

**Markdown is the authoring format.** This section is here for the times you
need to recognise the shape underneath it — reading a validation message,
looking inside an exported student file, or checking what an answer code
carries. You never have to write it.

A test is one object: the settings, then a list of parts, each with its
paragraphs and its question groups, and the pictures once at the end.

```jsonc
{
  "id": "my-test",
  "title": "My Test",
  "time": 20,
  "strand": "reading",             // or "listening"
  "showResults": true,
  "parts": [
    {
      "label": "Part 1",           // the "## " heading
      "passageTitle": "Passage title",
      "figure": { "id": "plan", "caption": "optional" },
      "glosses": true,             // the part's 📖 switch
      "paragraphs": [
        "Text, with {{gloss|VN|EN}} tags left in place.",
        "![A caption](#plan)"      // a paragraph that is only this is a picture
      ],
      "groups": [
        {
          "type": "tfng",          // one of the thirteen types
          "instructions": "…",
          "limit": "NO MORE THAN TWO WORDS",
          "options": [ { "letter": "A", "text": "…" } ],
          "questions": [
            { "stem": "…", "answer": "TRUE", "why": "…" }
          ]
        }
      ]
    }
  ],
  "assets": {
    "plan": { "src": "data:image/jpeg;base64,…", "alt": "…", "width": 520, "height": 340 }
  }
}
```

Field by field, the rules are the ones the Markdown sections above describe —
same names, same meanings. A few things only the model shows:

- Question numbers (`n`) and group ids (`uid`) are assigned on load. Never set
  them by hand; they are recalculated whenever parts or questions move.
- A graded question carries **either** `answer` (a letter, or `TRUE`/`YES`…, or
  an array for `mcq_multi`) **or** `accepted` (a list of acceptable typed
  answers). Typed mode — `"answerMode": "type"` — swaps the first for the
  second and drops the group's `options`.
- `open` questions have neither; they carry an optional `note`, your marking
  note, which students never see.
- Structural types keep their own field: `summary` for `summary_drag`, `steps`
  for `flow_chart`, `columns`/`rows` for `table_completion`, an optional
  `layout` for `note`, and a `zone` per question for `labelling`.

**A `.json` file still loads.** Import or paste one and it is read, migrated
and validated exactly like Markdown, so anything you or an AI generated in
this shape keeps working. There is no JSON sample to keep in step, though:
[`sample-test.md`](sample-test.md) and
[`sample-listening.md`](sample-listening.md) are the samples, and **Export ▾ →
Markdown** is how a test is saved for later editing.

## 3. Validation

On load, the app checks (and shows a clear error panel if any fail):

- Each part has passage text — **except** in a **listening** test
  (`strand: listening`), where the passage is optional (any text present is
  kept as a hidden transcript).
- Every question has an answer (or accepted-answers list) — **except**
  `open`, which must *not* have one (the Markdown parser rejects an `A.`
  line on an `open` question at parse time, naming the line number; the
  JSON path rejects an `answer`/`accepted` field the same way).
- `tfng` answers are one of `TRUE` / `FALSE` / `NOT GIVEN`.
- `ynng` answers are one of `YES` / `NO` / `NOT GIVEN`.
- `matching` / `labelling` / `mcq` / `summary_drag` / `flow_chart` answers
  reference an option that actually exists in that question's (or group's)
  option list — **except** `summary_drag`, `labelling`, and `flow_chart` in
  **typed mode** (`input: type`), which have no options list and are checked
  like `completion` (a non-empty accepted-answers list) instead.
- `summary_drag` groups have a non-empty `summary` whose number of `___` gaps
  equals the number of answer keys.
- `flow_chart` groups have at least one non-empty `step:`, at least one `___`
  gap across all steps, and the gap count equals the number of answer keys.
- `table_completion` groups have `columns` and `rows`, every row has the same
  number of cells as there are columns, and the total number of `___` blanks
  across all cells (inline blanks included, `\___` literals excluded) equals the
  number of answer keys. The mismatch error names the group and reports how many
  blanks were found versus how many answer keys were given.
- `note` groups with a structured `layout` have exactly one `blank` token per
  question (i.e. the number of `Q.` lines equals the number of blanks in the
  interleaved `H./T./Q.` sequence).
- `labelling` groups have a `figure:` (the picture their boxes sit on), and
  every `labelling` question has `at:` / `zone` coordinates (in both word-bank
  and typed mode).
- `display` is only accepted on `matching` groups, with the value `dropdown`.
- Question numbers are contiguous starting at 1, across the whole test
  (`open` questions get a number too, so they can appear in the nav bar).

Fix every listed error and re-load — nothing is graded until validation
passes. A small number of issues are **warnings** rather than errors — the
test still loads, but you'll see a dismissible notice:

- `reusable: false` combined with `display: dropdown` on a `matching` group
  (the flag is simply ignored, since a dropdown's options are always fully
  available).
- A word-bank group that is `reusable: false` (or has no `reusable:` line) whose
  answer key **repeats a letter** or has **more items than options**: a placed
  option is used up, so the key can't be answered. The warning names the file,
  the group and the problem (see "Reusable options"); add `reusable: true`.
  Teacher-only — students never see it.
- A `figure:` line (or `![...](#id)` paragraph) naming a picture that isn't in
  the test yet. The test still loads and the student would see
  `[missing image: id]` in its place — deliberate, so a draft can name its
  pictures before you add them. Add the picture in **📷 Pictures**, or fix the
  name.
- A picture nothing points at — harmless, but it is still carried in every
  export, so it is worth deleting in **📷 Pictures**.
- A picture over 500 KB, which bloats the exported file and the student's
  answer code. Shrink it and use **Replace…**.
- A test that was converted on load (an old `display: list` group). Save it
  to keep the conversion.

---

## 4. Grading rules

- `tfng` / `ynng` / `mcq` / `matching` / `labelling` / `summary_drag` /
  `flow_chart` in **word-bank mode**: exact match against the key (drag-drop
  and dropdown values are always exact letters, graded identically regardless
  of `display` mode). `summary_drag` and `flow_chart` score one point per
  correctly filled gap.
- `mcq_multi`: one point per correct letter selected, out of `count`.
- `completion` / `form` / `note` / `table_completion`, and `summary_drag` /
  `labelling` / `flow_chart` in **typed mode** (`input: type`):
  case-insensitive, whitespace-trimmed match against **any** entry in the
  accepted-answers list. If the response exceeds the word limit in `limit:`,
  it is marked wrong regardless of content, and the results table notes "over
  word limit". Each scores one point per correctly filled blank/question.
- `open`: **never auto-graded, and not part of the scored total at all.** A
  test with 24 items of which 5 are `open` reads "x / 19" — `open` questions
  are excluded from both the raw score and the denominator, and from
  band-score conversion entirely. They don't appear in the main results
  table; instead they get a dedicated **"Written answers (not scored)"**
  section listing the question, the student's response, and your marking
  note (from `W.` / `note`), for you to grade by hand. If a test is made
  *entirely* of `open` groups, the score/band/percentage cards show "—"
  instead of a meaningless 0/0, and the results screen is just that section.

## 5. Band score conversion

Edit the `BAND_TABLE` array near the top of the `<script>` in `index.html`
(section `CONFIG`) to match whichever band-conversion table you use — it's a
simple `{min, band}` list, checked top to bottom against the raw score.

## 6. Your library

Keep your tests as files in one folder and they appear on the start screen
under **Your library**, so you don't import them one at a time:

```
library/
  tests/      your .md and .json tests — this is the library
  handouts/   student copies you export (created when you first use it)
```

### In Chrome or Edge: connect the folder (no extra step)

Press **📁 Connect your library folder** on the start screen and pick your
`library` folder. Everything in `library/tests` appears as a card. Add a file to
that folder, press **↻ Refresh**, and it's there.

- **Pick the folder that holds your tests.** A folder containing a `tests`
  folder is treated as the library; a folder of `.md` files *is* the library.
  Nothing is created or moved when you connect.
- **The folder is remembered.** When you reopen the app, browsers ask once
  before letting a page read your files again: press **🔓 Reconnect**.
- **💾 Save to …** in the editor writes the test back to its own file. It saves
  without fuss, and only asks if the file changed on disk since you opened it.
  A test you built from scratch is saved as a new `.md` named after it, and
  never replaces an existing file without asking.
- **The file name doesn't follow the title.** Renaming the test in the app
  changes what's *inside* the file, not the file's name.
- **Exporting** a student copy asks where it goes: into `library/handouts`,
  a location you choose, or your Downloads folder.
- **↻ Refresh** re-reads the folder; **Disconnect** forgets it (your files stay
  exactly where they are).

### In Firefox, Safari, or on a phone: build the file instead

Those browsers don't let a page read a folder, so bake your tests into a copy
of the app:

```bash
python tools/build_library.py
```

That writes **`simulator.html`** — the app with every test in `library/tests`
inside it. Open that file, and rerun the command whenever you add or change a
test. `index.html` is never touched, and `simulator.html` isn't kept in git.

### Either way

- **A file that isn't a test is skipped** (no `# Test:` line), and it says so.
- **A test with a mistake still shows**, as a card naming the line and the
  problem, so the rest of your library keeps working.
- **Clicking a card opens the test in Review & Edit**, exactly like an import.
- **Students never see your library.** A file you export for students contains
  only that one test.
- Cards show **"Saved progress on this computer"** when an unfinished attempt
  for that test is stored in this browser.

Student work that comes back is separate: each returned file is a whole copy of
the app plus one student's answers. Open one directly, or use **View a
student's answers** with their answer code.

## 7. Exporting for students, and getting their results back

### Teacher: create the student copy

Once a test is loaded (baked-in, imported, or pasted), click **⬇ Export ▾**
at the bottom of the editor and choose **Standalone file for students** (or,
while taking the test, **⬇ Export standalone** in the top bar — under
**⋯ Tools** on a small screen). This downloads a new `.html` file with:

- Your test baked in as the default (loads straight into it — no picker).
- The import/paste UI removed.

Choosing it asks what kind of file you want, because the same test goes out in
two shapes:

- **📘 Class work / homework** — glosses on, no time limit, results shown as
  soon as they submit.
- **📝 Test** — glosses off, a time limit you set, results kept back (they
  get an answer code to send you).

Either preset can be adjusted before you download — the three switches are
right there — and whatever you choose applies to **that file only**. The test
you are editing is untouched, so the same passage can go out as homework on
Monday and as a test on Friday.

Send students that one file; it works fully offline, opened directly from
disk.

### Student: name, attempt, and sending it back

The first time a student opens their copy, they're asked to type their name
before the timer starts. That name travels with everything they do from
then on — it's shown in the top bar, on the results screen, and baked into
whatever file they send back. If they close the tab and reopen the same
file, their in-progress answers resume automatically (via `localStorage` on
their own machine) without asking for the name again.

After they submit, a **⬇ Download completed file** button appears on the
results screen — and, when results are kept back (a 📝 Test), beside
**📋 Export answer code** on the plain "submitted" screen. This downloads a *new* `.html` file — same test, but with
their name, answers, flags, highlights and score baked in as fixed data.
Filename is `<test-id>_<student-name>.html`, e.g. `friendship-siblings_jane-doe.html`.
The student emails/uploads that file back to the teacher.

### Teacher: opening a returned file

Just open the `.html` file the student sent back (double-click it, or drag
it into a browser window). Because the answers are baked into the file
itself — not read from `localStorage` — it doesn't matter whose computer
opens it: it goes straight to the graded results screen, locked, with the
student's name at the top. Use **Review answers in the passage** to see their
answers laid over the original passage and questions, **🖨 Save as PDF** for a
paper or PDF copy of the results and answer key, or **📄 Word report** for a
`.docx` (score, band, part scores, and every answer with its mark and note).
Any `open` questions show up in the "Written answers (not
scored)" section with the student's typed responses and your marking
notes — like every other answer type, these are ordinary saved data, so
they travel with the file automatically.

This means each student's file is self-contained proof of their attempt —
you can collect a folder of them from a whole class without needing a
server or shared account.

**When results are kept back** (a 📝 Test, `results: hidden`), a returned file
opens on the plain "Your answers have been submitted" screen instead, with no
score and no answer key. A **🔑 Teacher: show results** button on that screen
opens the marked work. It keeps a student's own downloaded copy from showing
them their result and the key; it is not a lock, because every test file
carries its own answers. Answer codes pasted into **View a student's answers**
always open the full results.

### Teacher: the answer code, and pictures

The other route back is the **answer code**: a block of text the student
copies from the results screen and pastes into a chat or a document. It is the
only route when a student can't send a file, and it is what **results: hidden**
tests give them instead of a score.

The code carries the whole test as well as the answers, so you can open one
from a cold start screen. Pictures are the exception: a photo doesn't compress,
so carrying it would pass its whole size into the pasted text. One test with a
160 KB diagram produced a **165,674-character** code.

So a test with pictures now sends a code **without** them — ids and alt text
only — which took that same test to **4,702 characters**. When you paste it,
the app puts the pictures back from your own copy of that test: the one open in
the editor, the one on screen, or a test in your library with the same `id:`.

- If no copy is open, the code still opens — answers, score and evidence are all
  there — and a note tells you which pictures couldn't be shown; they read
  `[missing image: id]`. Open the test (from your library or by importing the
  file) and paste the code again to see them.
- If your copy's picture has changed since the student sat the test, the app
  says so rather than pretending it is the same one.
- A test **without** pictures produces exactly the code it always did, and
  every code made before this version still opens, pictures and all.
