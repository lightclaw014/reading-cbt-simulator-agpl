# Reading CBT Simulator

A computer-delivered reading test that runs in one HTML file — no install, no
account, no server. Teachers write a test in a plain text file, students take it
in their browser exactly as they would in the real computer-delivered exam, and
everything is marked on the spot.

**Try it:** open the hosted page, or download `index.html` and double-click it.

Nothing is uploaded. Tests, answers and progress stay in the browser on the
computer they were typed on.

## What it does

**For students**
- The familiar two-pane screen: passage on the left, questions on the right, a
  draggable divider, a timer and the question bar along the bottom.
- Every common question type: True/False/Not Given, Yes/No/Not Given, multiple
  choice (one or several answers), sentence, form, note and table completion,
  matching, diagram labelling, summary completion, flow-charts, and open-ended
  questions that are not auto-marked.
- Highlighting with notes, text zoom, flags, and answers that survive a
  refresh.
- On submit: a score, an estimated band, and a question-by-question review with
  the evidence for each answer.

**For teachers**
- **Write tests in Markdown** (see [AUTHORING.md](AUTHORING.md)) or build them
  in the app, with a full editor for every question type.
- **🤖 Generate with AI** — answer a few quick questions and get a ready-made
  prompt for ChatGPT, Claude or Gemini that turns your passage (and, if you
  have them, your own questions, answer key and words to gloss) into a test
  file. No word list? The AI can choose up to 10 words per passage to gloss,
  pitched at your students' level. Paste the AI's reply straight back into
  the app.
- **Glosses** — tap a word in the passage for an English definition, a
  Vietnamese translation, or both, with an example. Words the questions test
  stay hidden until you turn on *Show answer words* after the test, for going
  through answers together.
- **Your library** — keep your tests in one folder and they appear on the start
  screen. In Chrome and Edge the app reads the folder directly; other browsers
  use a one-command build step.
- **Give a test to students** as a single file that works offline, and read
  their work back from a file or a short answer code.
- **Listening layout** for a single-column, no-passage test.

## Getting started

1. **Download `index.html`** (or open the hosted page) and open it.
2. Press **Start** on the sample test, then **👁 Preview as student** to see
   the student's view.
3. Press **Create new test**, or **Import test file** with `sample-test.md` to
   see how a test file becomes a test.
4. To give it to a class: open your test, then **⬇ Export ▾ → Standalone file
   for students**, and send that file. They double-click it; it works offline.

## Writing a test

A test is a text file. The whole format is in
[AUTHORING.md](AUTHORING.md); the shortest possible version:

```markdown
# Test: Bees
time: 20

## Part 1
### Passage: How bees navigate
Bees find their way home using the position of the sun...

### Questions: tfng
instructions: Do the following statements agree with the passage?

Q. Bees rely on landmarks alone.
A. FALSE
W. Para 1 — the passage says they use the sun's position.
```

Load it with **Import test file**, or keep it in your library folder.

## Your library

Put your tests in a folder:

```
library/
  tests/      your .md and .json tests
  handouts/   copies you export for students
```

- **Chrome / Edge:** press **📁 Connect your library folder** and pick it. The
  tests appear on the start screen, read from your computer. Your files are
  never uploaded, and the app remembers the folder for next time.
- **Firefox / Safari / phones:** those browsers don't let a page read a folder,
  so run `python tools/build_library.py` to write `simulator.html` — the app
  with your tests inside — and open that instead.

## Privacy

There is no server and no account. Tests, answers, highlights and progress live
in the browser's own storage on that computer. A student's work reaches you only
when they send you a file or paste their answer code.

One thing to know: a test file contains its answer key, because marking happens
offline in the browser. Anyone who has a student copy can read the answers from
it, so don't publish those files on the web.

## Contributing and licence

Issues and pull requests are welcome. The app is deliberately one file with no
build step and no dependencies — `index.html` is the source of truth, and it
must keep working when opened straight from disk.

**Licence: GNU AGPL-3.0-or-later** — see [LICENSE](LICENSE). In short: you may
use, study and change it freely, including in your classroom. If you change it
and share it, or run a changed copy for others to use over a network, you must
share your changes under the same licence, with the copyright notice kept.

Versions up to and including v0.13.1 were released under the MIT licence and
remain available under it. From v0.14.0 the app is AGPL.
