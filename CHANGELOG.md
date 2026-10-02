# Changelog

All notable changes to the IELTS Reading Simulator, newest first.
Each version is also a **tag** on GitHub — open the repository's **"Tags"**
page to view or restore any of them.

## v0.14.1 — "A better prompt" — 2026-10-02

### Changed
- **The 🤖 Generate with AI prompt now teaches the AI every current feature**, so
  a pasted reply loads cleanly. New: one field = one line of the file with `\n` for
  a line break (and never `\n` in the passage); when to write `reusable: true`
  (and that the default is false), with a classification example and a cue in
  each word-bank section; passage formatting (`<b>`, `<u>` only); formatted
  glossed words (`{{<b>word</b>|…}}`); the optional `E.` evidence line; and the
  full label list (`title:`, `reusable:`, `display:`, `columns:`, `row:`, `E.`,
  `H.`, `T.`). A self-check fails if the prompt ever stops mentioning a label the
  parser reads.

## v0.14.0 — "Licence" — 2026-10-02

### Changed
- **The app is now licensed under the GNU Affero General Public License v3.0
  or later** (`LICENSE`, and a notice at the top of `index.html`). Anyone may use
  it, including for teaching; anyone who changes it and shares it, or runs a
  changed copy for others over a network, must make their changes available
  under the same licence.
- **Earlier versions (v0.13.1 and before) were released under the MIT licence
  and stay available under it.** A licence already granted can't be withdrawn;
  AGPL applies from this version onward.
- `tools/publish.py` now ships `LICENSE` with the app.

## v0.13.1 — "Formatted glosses" — 2026-10-02

### Fixed
- **A glossed word could not be bold or underlined** — key or not. The editor
  wrote each gloss from its plain text, so any formatting inside the word was
  dropped whenever the passage was saved, and the toolbar can't reach inside a
  gloss. Formatting now survives the save, and the gloss form has **B** / **U**
  buttons ("Format the word") that apply to every part of a split phrase.
  **Ctrl/Cmd+B** and **+U** work too: with the gloss form open, and on a
  selection in the passage that touches glossed words.

## v0.13.0 — "Line breaks everywhere" — 2026-10-01

### Added
- **`\n` is a line break in every text field**, not just table cells: instructions,
  limits, stems, option text, flow-chart steps, summaries, table headings and
  cells, notes headings/lines, and the `W.` note in the results. One shared
  `formatText()` escapes the text, then draws the break; the table's own
  handling is gone, so there is a single code path.
- **`title:` on a group** — an optional bold heading above its content (flow
  chart, table, notes, summary, diagram). A **Title** box in the editor.
- **Warning for a use-once word bank that can't be answered**: `reusable: false`
  (or absent) with a repeated letter in the key, or more items than options.
  Names the file, group and problem; teacher-only; never blocks loading.
- `regression-test.md`, also run by `?selfcheck`: every group type, a `\n` in every
  text field, a `title:` on every group, reusable and non-reusable banks.
- Editor: the **Reusable** checkbox now also appears on word-bank `labelling`.

### Changed
- **The editor's text fields are multi-line boxes** (instructions, title, limit,
  stems, options, summary, steps, column headings, evidence notes) with the table
  cells' keys: Enter, Shift+Enter, Ctrl/Alt/Cmd+Enter. The editor writes the `\n`.
- `reusable: true` already kept options in the bank; it is now covered by checks
  (copies place, move and clear independently; repeated letters score).
- A table's `columns:` headings can break too.

## v0.12.1 — "Forgiving option letters" — 2026-10-01

### Fixed
- **A test from the AI could fail to load over one option letter.** A list that
  ran `A.` `B.` `C.` `D.` and then slipped to a lowercase `e.` stopped the whole
  test with "Unrecognised line inside a questions block". Option letters are now
  read forgivingly: upper or lower case, and `A.` or `A)` in either the shared
  `options:` block or under a `Q.`, all stored as the canonical uppercase letter.
  In an `mcq` a dotted line counts as an option only while the options are still
  being listed — it must be the next letter and come before the answer — so the
  `A.` answer, the `W.` note and the `E.` evidence line keep their meanings.
  A line that still can't be an option now says where options go for that type,
  instead of only refusing it.

## v0.12.0 — "Your mark" — 2026-09-30

### Added
- **The version, and your mark, bottom-left.** A small pale line ("v0.12.0 · lightclaw014")
  on the start screen, the test's page, the part editor and the results screen,
  where it never covers a button and gives way to the test screen a student sits
  (the question numbers live in that corner). It is left off students' exported
  files and off the printed PDF. `APP_VERSION` holds the number, and
  `tools/publish.py` now refuses to publish if it differs from the newest release
  in this changelog; `APP_WATERMARK` holds the text after it.

## v0.11.0 — "Handing it back" — 2026-09-30

### Fixed
- The self-check for the AI wizard still looked for level A2 after the level
  row changed to A1, so it failed once the page was loaded fresh.

### Added
- **The marked work as a PDF or a Word file.** Two buttons on the results
  screen: **🖨 Save as PDF** (the browser's own print with Save as PDF as the
  printer) and **📄 Word report** (a `.docx`: student, attempt, estimated band,
  raw score, part scores, then every answer with the correct answer, a ✓ ✗ ○
  mark and the teacher's note, and the written answers). The PDF route needed
  the print stylesheet brought up to date: it was still written for the old
  results table, and the app's one-screen-tall shell would have printed a
  single page. The Word file is built in the page with no library (a small zip
  writer plus WordprocessingML), adding a few KB; it was checked by opening it
  in Word. There are no fonts embedded, so Vietnamese comes out right in both.
  They are on the teacher's view of a returned code or file as well as the
  student's own.
- **Download completed file in Test mode.** A test with results kept back now
  offers **⬇ Download completed file** next to the answer code on the
  "submitted" screen, so a student has both ways back to the teacher. Because a
  returned file used to open with the full score and answer key, a file from a
  test with results kept back now opens on the plain submitted screen, with a
  **🔑 Teacher: show results** button to the marked work. A deterrent rather
  than a lock: every test file carries its own answers. Pasted answer codes and
  ordinary tests are unchanged.
- **A table cell can hold more than one line.** In the editor a cell is a text
  box that grows: Enter (or Ctrl+Enter, Ctrl+Shift+Enter, Alt+Enter) starts a
  new line. In a file the break is written `\n`, and students see the lines
  stacked in the cell. Files that already had `\n` typed into a cell (the AI
  writes it that way) now show the break instead of the two characters, and the
  AI prompt tells it to write `\n` for a two-line cell.
- **A1 in the AI gloss level.** The wizard's level row now runs A1, A2, B1, B2,
  for classes below IELTS 3.0. B1 is still the default.

## v0.10.0 — "The AI picks the glosses" — 2026-09-30

### Added
- **🤖 Generate with AI can choose the words to gloss.** Answer No to "Do you
  have a list of words to gloss?" and the wizard asks whether the AI should
  choose them. Say Yes and pick your students' level — **A2**, **B1** (the
  default) or **B2**. The prompt then has the AI gloss at most 10 words or
  phrases above that level in each passage: the ones a student needs to follow
  the passage or answer the questions, not every rare word. Words the questions
  test are glossed and marked `key`, so students see them only after the test.
  Say No and the test comes back without glosses, to add yourself in
  📖 View glosses.
  - The Oxford Text Checker tip that appeared after "No list" is gone.

## v0.9.0 — "Evidence and the AI wizard" — 2026-09-29

### Fixed
- **A gloss added in the editor vanished in Preview as student** but was
  there in the exported file. Each part had its own 📖 Glosses switch,
  off by default and tucked inside the View glosses window; Preview followed
  it, while the export window ignored it and set glosses by its own toggle.
  The per-part switch is gone: glosses show wherever they are written, and
  the export window's **Glosses** switch is the one way to turn them off,
  for the downloaded file. The part card's "switched off" line went with it.
  Older files' `glosses: on` / `off` lines still load and are ignored.
- **Two questions looked current at once.** The blue outline only ever moved
  when a nav number was pressed, so it stayed parked on the last one chosen
  there while the student answered somewhere else. Answering a question — by
  mouse or by keyboard — now makes it the current one, and the nav bar follows.
  It marks the question, it doesn't scroll to it: it is already under their hand.
- Pressing a question's own **Evidence** button no longer yanks the question
  pane: it scrolls only when the question isn't already on screen.
- A verdict strip on a **matching** question sat beside the drop zone as a
  third column, squeezing it. It breaks to its own line under the question now.
- **Preview as student did nothing** when pressed on a test's own page. The
  editor is two screens now, and leaving it only closed one of them — the
  hub covers the whole window, so the preview started underneath it, out of
  sight. Clicking Back then uncovered whatever had been left there, which is
  why an old results screen appeared below the start screen. Every way out of
  the editor closes both screens now. Opening a student's answers had the
  same hole.
- **Preview or Export stopped by a mistake in the test looked like a dead
  button** on the test's page: the list of what to fix was written to the part
  screen, hidden behind it. It shows on whichever screen you pressed it from.

### Changed
- **Begin test is gone.** It started a real attempt of your own test from the
  editor, which **👁 Preview as student** already does without saving
  anything — and a preview always has a way back. The ◀ Leave test and
  ◀ Back to the test buttons that went with it are gone too.
- **Preview as student and Export are on every part's screen**, in the same
  bar at the bottom as on the test's page, so you can finish a part and export
  without going back to ◀ Test overview. Preview from a part opens the test at
  that part, and "← Back to the test" returns you to it.

### Added
- **A gloss can be Vietnamese only, English only, or both.** In the gloss
  form either definition may be left blank, and students see whichever the
  gloss has — useful for a class too young to read the English definition.
  With both, nothing changes: English first, Vietnamese behind a button. A
  gloss counts as unfinished only when both are missing. In a file the
  empty one keeps its place: `{{declined|giảm|}}`, `{{declined||became lower}}`.
- **🤖 Generate with AI is now a wizard.** Three quick yes/no questions — your
  own questions? the answer key? a list of words to gloss? — build the one
  prompt that fits, instead of a single prompt with two optional sections left
  for you to fill in or delete correctly. "◀ Change answers" goes back without
  losing what you picked.
  - Converting your own questions keeps every question, option and answer as
    written and only chooses the closest type; a question that fits none is
    written as open with a note starting **`UNCONVERTED:`**. Without an
    answer key, the AI works each answer out itself and starts that note with
    **`CHECK:`**. The test's page lists every question flagged either way, so
    a converted test never quietly ships with a guessed answer.
  - Gloss instructions now say to tag *every* occurrence of a listed word
    and keep English definitions to 12 common words or fewer.
  - If your passage is a picture or PDF, the prompt now tells the AI to copy
    the text exactly rather than retype it from a description.
- **Pasting an AI's reply tolerates the reply.** "Here's your test:", a
  closing remark, or a ` ``` ` fence around the whole thing used to fail with
  "Content outside any section." Every import path (paste, file, drag-and-drop)
  now looks for a fenced block or a `# Test:` line first and loads just that.
- **The answer key sits under the score**, on the same page: every item,
  grouped by part, two columns — number, the answer, what was written (struck
  through when wrong), ✓ ✗ ○, and **Evidence**. The number bubbles carry the
  verdict in colour, so the shape of a test reads before a word of it does.
  It replaces the wide six-column table, which needed three screens for forty
  items, and the overview/detail toggle that went with it.
  - **Print results** and **Review incorrect only** are gone. Ctrl+P still
    prints, and the key now fits on one page rather than three.
- **An evidence window** from the answer key: the paragraph the answer came
  from, painted, beside the question, what was written, the correct answer and
  the note — with "Open it in the passage" to go there properly. In the review
  screen the passage is already on show, so Evidence keeps painting it in
  place; a window there would cover what you are reading.
- **One review, not two.** The results screen had **Review answers in the
  passage** and **Detailed results** side by side: one showed the passage
  without saying what was right, the other said what was right without the
  passage. There is one button now — **Review your answers** — and it opens
  the test as it was sat, with a strip under every question giving the verdict
  (✓ / ✗ / ○, never colour alone), the answer that was missed, and an
  **Evidence** button. The part banner carries that part's tally, the question
  numbers along the bottom are tinted by result, and **≡ Table view** reaches
  the old table — still the thing that filters to the incorrect ones and
  prints. The strips are a layer over the rendered questions, so a question
  type added later is marked without touching this code.
- **Evidence review.** After submitting, every row of the detailed results
  table is clickable: it goes back into the locked test at that part and paints
  the words the question was answered from, with a chip naming the question and
  a way back to the table. Where a note only names a paragraph, that paragraph
  is outlined instead; where there is nothing to go on, it says so rather than
  guessing. This is the "where should I have looked?" moment — scanning
  practice while the test is still fresh.
  - It works on tests you already have, because it reads the `W.` notes you
    already write: a quotation in the note is found in the passage, and
    "Para 3" points at paragraph 3. An optional **`E.` line** gives the exact
    words for questions whose note paraphrases instead of quoting.
  - **A listening test reveals its transcript** once the test is over, so the
    evidence can be pointed at there too. During the test it stays hidden.

## v0.8.0 — "The teacher's side" — 2026-09-25

### Added
- **Exporting asks what kind of file you want.** The same test goes out in two
  shapes, so **Standalone file for students** now opens a window offering
  **📘 Class work / homework** (glosses on, no time limit, results shown) and
  **📝 Test** (glosses off, timed, results kept back). The two stack on the
  left with the three switches beside them, so choosing one shows you what it
  means and you can adjust before downloading. It applies to that file only — the
  test you are editing never changes, so one passage can be homework on Monday
  and a test on Friday.
- **A test can have no time limit** (`time: 0`). The clock is absent and
  nothing submits itself; the student stops when they are done.

### Changed
- **Markdown is the authoring format; JSON is just the shape underneath.**
  `sample-test.json` is gone and AUTHORING.md's JSON section is now a short
  reference for reading a validation message or an exported file, rather than
  a second format to keep in step. Importing or pasting a `.json` test still
  works exactly as before, and the library still reads `.json` files.

### Added
- **The start screen's cards are the sample files.** The app used to carry a
  separate built-in sample — two parts, no glosses, no pictures — which had
  quietly fallen years behind `sample-test.md`. Both sample files are now
  embedded and parsed on first use, so opening a card gives you the test with
  every feature in it, and `python tools/sync_sample.py` copies the files in
  after you edit them. A part's picture also shows in the passage while you
  are reading it, where students see it.
- **The samples now cover everything.** `sample-test.md` gains a third part
  with the four question types it was missing — Yes/No/Not Given, form
  completion, flow-chart completion and a typed diagram-labelling group —
  plus a split-phrase gloss. A second file, `sample-listening.md`, covers what
  a reading test cannot: the listening layout, hidden transcripts, a part
  figure pinned above the questions, and plan labelling.
- **A test now opens on its own page, not in the editor.** That page holds
  everything about the test as a whole — its name, time, Reading/Listening,
  Show results — and a card for each part showing what it holds: the question
  numbers, the types, whether it has a picture, how many glosses and whether
  they are switched on, and anything unfinished. Renaming, reordering
  (by dragging a card), adding and deleting parts all happen there, next to
  **Begin test**, **Preview as student**, **Export** and **Save to library**.
  Each card reads as a list: the passage and its word count, how many
  questions in how many groups, a line per group (Q1–3 · True / False / Not
  Given), then the picture, the glosses and anything unfinished. Beside the
  test's name sits its shape — "2 parts · 30 questions · Reading · 25 min" —
  and under the cards, **Before you send it out** lists what the validator
  found, plus the reminders worth having (written answers aren't scored;
  results are hidden).
- **A file with two `## Part 1` headings** no longer shows two parts both
  called Part 1: automatic labels renumber when a test loads, as they already
  did when you added or deleted a part.
- **The passage toolbar's − / size / + are a view setting now.** They used to
  resize the words you had selected and store that in the test as inline
  `font-size` spans, which made a passage read unevenly for students, hid
  itself until you clicked the right word, and duplicated the **A− / A+** that
  students already have during a test. They now set how big the passage looks
  while you write — this machine only, remembered between sessions, never part
  of the test. ↺ goes back to the size students see. A file that already
  carries `font-size` spans still renders them.
- **The passage editor is three sections**, in the order students meet them:
  the part's picture (a dashed “＋ Add a picture” strip until there is one),
  the title as a field of its own, and the passage text. The title used to be
  a heading inside the same text box, where a stray Enter could turn it into a
  paragraph or delete it; it now has nowhere else to go. Reading the part is
  unchanged — one passage, no boxes.
- **A part opens as a preview of itself**, and each pane is edited on its own.
  Hovering the passage or the questions tints that pane and fades in
  **✏ Edit passage** / **✏ Edit questions** in its corner; ✓ Done goes back to
  reading. The two are independent, so a passage can be rewritten with its
  questions still in view, and the passage can no longer be typed into by
  accident. The top bar's **Preview | Edit questions** switch is gone — each
  pane carries its own control.
- **Opening a part gives a screen with nothing on it but the writing** — the
  passage, the questions, and the two tool windows. Its part tabs only move
  between parts now, and the settings row, the part controls and the action
  bar are gone from it. A new test goes straight there, since a blank test has
  nothing to review.
- **Name your parts.** **✏ Rename part** in the part bar — or a double-click on
  a tab — turns the tab into a text box: call a part "Section 2 —
  Accommodation" instead of "Part 2". The name is the part's `## ` heading, so
  it round-trips through Markdown and shows in the student's part strip.
  Unnamed parts still number themselves, and a name you chose is no longer
  overwritten when you add or delete a part. Blank falls back to "Part n", a
  leading `#` is stripped, and `Assets` is refused (it starts the pictures
  section of a test file).

- The editor's windows and popovers now fade in the way the rest of the app
  already did — the Glosses and Pictures windows, the picture window, the
  asset picker, the gloss form and its right-click menu — and the listening
  picture panel folds instead of snapping. A full-screen window fades on the
  way out too, but gives up its clicks the moment you close it, so the editor
  underneath is live while the pixels finish; small popovers still close in
  one frame. Nothing on the student's test screen moves.

### Changed
- **Drag a part tab to move the part**, with its passage and its questions; the
  numbering follows. A line shows where it will land. The old
  **Reorder: ◀ Move / Move ▶** buttons are gone, and so is the **Rename part**
  button — the tab offers both now. Dragging is mouse-only: there is no
  keyboard or touch equivalent.
- **Hovering the part you are on turns its tab into a text box**, the way a
  document title does, and clicking it starts the rename — so the feature
  announces itself instead of hiding behind a button.
- **The editor's part banner is gone** ("Part 1 — Read the text and answer
  questions 1–12"): the part's name is on its tab and the numbers are on the
  questions. A listening part keeps that row, because the transcript
  disclosure and its picture button live there, but without the sentence.
  The student's own part banner is unchanged.

## v0.7.0 — "Pictures" — 2026-09-24

### Added
- **Pictures anywhere in a test, stored once.** A picture now belongs to the
  test rather than to one question group, and three places can show it: a whole
  **part** (`figure:` under `## Part 1`), a spot **inside the passage** (a
  paragraph that is only `![caption](#id)`), or a **question group** of any type
  (`figure:` under `### Questions:`). Reading and listening both. The same
  picture used in five places is stored once — in the Markdown, the JSON, an
  exported student file and a returned attempt alike. One test in the library
  went from 323 KB to 165 KB just by being loaded and saved again.
  - The images live in an **`## Assets`** section at the end of the Markdown, so
    the base64 no longer buries the test. Each entry has an id, `alt` text and
    the `src`; everything else refers to the id.
  - **Listening parts** show their picture in a panel pinned above the
    questions, which collapses and zooms and remembers that per part.
  - Any picture opens full-screen on click (or Enter).
- **Adding a picture: paste it, drop it, or pick it.** All three go through the
  same pipeline — shrunk to 1600 px on the longest side, re-encoded as JPEG
  (the original is kept when it was already smaller), then hashed, so pasting
  the same picture twice just points at the first copy. The app warns past
  500 KB.
- **📷 Pictures**, a fourth view in the editor: every picture in the test with
  its thumbnail, id, size and what uses it. Rename an id and every reference
  follows; replace the file, jump to a use, or delete one that nothing points
  at. **Use another…** reuses a picture the test already has.
- **One button, one little window.** Everything about a picture — paste, drop,
  choose, reuse, caption, replace, remove — happens in a small window, opened by
  a single **📷 Add picture** button. The part's button sits on the passage
  toolbar beside **📖 Add gloss** (and, for a listening part, in the part banner,
  since the toolbar folds away with the transcript); once a picture is set, that
  picture becomes the button's own icon. Each question group has the same
  button, with a chip beside it naming what is set. No more permanent drop-box
  per part and per group.
- The editor no longer asks you to describe a picture for screen readers: the
  caption does that job. A description already in a test file is kept, saved
  back, and used ahead of the caption.

### Changed
- **`labelling` means one thing now: answer boxes on a picture.** It requires a
  `figure:`, and each question still needs its `at: x, y`.
- **`display: list` is retired** — it did the same job as an ordinary group with
  a picture above it. Old tests are converted as they load: a typed one becomes
  **completion**, a word-bank one becomes **matching**, the picture moves to the
  group's `figure:`, and the app says what it did. Numbering, answer keys and
  grading are untouched; `at:` coordinates are dropped, and a question that had
  no stem (the picture printed it) gets a `Gap n` placeholder to rewrite.
- **A `figure:` naming a picture that isn't there yet loads with a warning**
  rather than failing, so an AI-written draft can name its pictures before you
  add them; the student would see `[missing image: id]` in its place. The
  AI prompt now teaches this.
- The old `image:` line still parses everywhere `figure:` does, and becomes an
  asset on load.

- **The answer code no longer carries the pictures.** A photo doesn't compress,
  so it used to pass its whole size into the pasted text: one test with a 160 KB
  diagram made a 165,674-character code. That same test now makes a **4,702**-
  character one. Pasting it back puts the pictures in again from your own copy
  of the test — the one in the editor, the one on screen, or one in your library
  with the same id. Without a copy the code still opens (answers, score and
  evidence all there) and says which pictures it couldn't show; if your copy's
  picture changed since the student sat the test, it says that too. A test with
  no pictures makes exactly the code it always did, and every code made before
  this version still opens.

- **Glosses and Pictures are windows now, not views.** Both open in the middle
  of the screen; closing one puts the panes back exactly as they were. In the
  glosses window, **Edit**, **Go to** and **Find in passage** close it on the
  way, because each hands you back to the passage — removing a gloss doesn't.
  The top bar's switch is just **Preview | Edit questions** again.
- **The 📖 Add gloss toolbar button is gone.** It could only tell you to select
  something first. Selecting a word — with the mouse or with Shift and the
  arrow keys — still pops the same button over the selection, and right-click
  still offers it.

### Fixed
- A picture is no longer written into the saved highlight snapshot, so
  highlighting a passage with figures does not bloat `localStorage`.
- A baked-in library (`tools/build_library.py`) now migrates old tests as it
  reads them, like every other load path.

### For the curious
- `index.html?selfcheck` runs sixteen checks over the parser, the migrations,
  the asset plumbing and the answer code, and prints a pass/fail list. A normal
  load never runs it.

## v0.6.0 — "Your library" — 2026-09-23

### Added
- **Your library** — keep your tests in one folder (`library/tests`) and they
  appear on the start screen; a card opens one in Review & Edit like any
  import. A file that isn't a test is skipped; a test with a mistake shows as a
  card naming the line and the problem. Cards mark tests with saved progress on
  that computer, and a search box appears past eight tests. Exported student
  files never carry the library.
  - **Chrome / Edge:** **📁 Connect your library folder** reads the folder
    live — no build step — and is remembered between visits (browsers ask once
    per session, hence **🔓 Reconnect**). **💾 Save to …** writes the open test
    back to its file, asking only if it changed on disk meanwhile. Exporting a
    student copy asks where it goes: `library/handouts`, a chosen location, or
    Downloads. Connecting creates nothing: a folder holding `tests` is the
    library, a folder of `.md` files is itself the library.
  - **Other browsers:** `python tools/build_library.py` bakes `library/tests`
    into `simulator.html`, leaving `index.html` untouched.

## v0.5.1 — "UI touch-up + compact question editor" — 2026-09-22

### Changed
- **Works on small laptops, projectors and phones** — the test screen's top-bar
  tools (Clear highlights, Notes, Start over, Export) fold into a **⋯ Tools**
  menu below 900 px; the ← → buttons move into the bottom bar (they used to
  cover the Flag buttons); the question-number strip scrolls and keeps the
  current number in view.
- **Editor** — the top bar is two rows so nothing is cut off, and the
  right-hand view is one **Preview | Edit questions | Glosses** switch. The two
  downloads sit under one **⬇ Export ▾** button; the part-tabs bar wraps.
- **Results** — the estimated band leads; actions are grouped, and
  "Back to test (locked)" is now **Review answers in the passage** (the way to
  Show answer words). The detailed table shows readable type names, marks
  unanswered questions "○ skipped", and shows the option text for letter
  answers, with a heading row per part.
- **Start screen** — each create/import card is a single button (it used to
  repeat its name as a second button); "2 part(s)" reads "2 parts".
- **Question editor (✏ Edit questions)** — compact rows: question text in the
  normal font (it showed in a typewriter font), then one line with the answer
  and the evidence note. T/F/NG and Y/N/NG answers are a three-button toggle,
  letter answers are letter buttons, typed answers are small "accepted" chips
  with "+ alternative". The evidence note is a one-line preview you click to
  edit. One "⋯" menu per question (move / delete) and per group (move, change
  type — now confirmed before answers are reset — delete). Only one group is
  open at a time; the others show as one-line summaries
  ("Q6–8 · Matching · 3 questions · B, A, C"). "Jump to" is one sticky row.
  While editing questions the passage narrows to about a third of the width.
  A multi-answer group's "n of N chosen" turns red until the count is right.

### Fixed
- The passage toolbar no longer leaves a gap above it when the editor passage
  scrolls.

## v0.5.0 — "Glosses, listening layout + new question layouts" — 2026-09-22

### Added
- **Glosses** — tap a passage word for a popup with an English definition, an
  example and (behind a button) a Vietnamese translation. Written in the
  passage as `{{word|VN|EN|ex: example|key}}`; turned on per part with the new
  **📖 Glosses** checkbox in the editor (`glosses: on` in Markdown). Off by
  default; with it off the passage renders exactly as before.
- **🔑 Show answer words** — a per-part answer-checking switch in the part
  banner, available only after submission. Reveals `key` glosses (the words the
  items test). Built as a general reveal control so evidence highlights can
  join it later. View-only: never saved or included in the answer code.
- **Gloss editing without codes** — in the editor, glossed words show as
  underlined units instead of `{{…}}` text. Select a word and click
  **📖 Add gloss**, or click a glossed word, to fill in a small form
  (definition, Vietnamese, example, 🔑 answer word). A new **📖 Glosses** view
  lists every gloss in the part (Edit / Go to / remove), flags unfinished ones,
  suggests answer words from the `W.` evidence notes, and can mark a pasted
  word list in the passage. Unfinished or mis-written glosses now raise a
  warning on load and before Begin/Export.
- **Quicker gloss adding + phrases with a gap** — selecting passage text pops
  up a floating **📖 Add gloss** button, and right-click offers Add gloss (or
  Edit / Remove on a glossed word). A half-selected word snaps to the whole
  word. For a collocation with its object in the middle, select the whole
  stretch and click the object's words in the form to leave them out: the gloss
  becomes "take … into account", saved as `{{take|…}} the weather {{+into account}}`.
  Students see every piece underlined and one popup for the phrase. The word
  list accepts `take ... into account` too.
- **🤖 Generate with AI knows glosses** — the copy-paste prompt now ends with an
  optional "Words to gloss" slot and teaches the AI the gloss format (normal,
  `key`, and `{{+…}}` split phrases) with the same rules as the authoring skill:
  gloss only listed words, meaning in this passage, never change the passage,
  mark `key` from the `W.` evidence. No list → no tags.
- **Listening layout** — `strand: listening` (or the 🎧 Reading / Listening
  dropdown in the editor) gives students a single column with no passage pane;
  any passage is kept as a hidden transcript, collapsed in the editor.
- **Hide results from students** — `results: hidden` (the 📊 Show results
  checkbox): on submit, students see a confirmation and an answer code instead
  of their score; you still see full results when you open their work.
- **Flow-chart completion** — a new question type: a vertical chain of step
  boxes with `___` blanks (`step:` lines), answered from a word bank or by typing.
- **Typed answering for labelling and flow-chart** — `input: type` now works on
  `labelling` and `flow_chart` as well as `summary_drag`.
- **Labelling: answer boxes in a list** — `display: list` puts the boxes in a
  numbered list below the image (no `at:` coordinates), for images that already
  print the questions. Images can be **embedded** from a local file so they
  travel inside the exported HTML.
- **Structured notes** — `H.` (heading) and `T.` (context line) lines in a
  `note` group give the IELTS notes look.
- **Table blanks anywhere in a cell** — any number of `___` inside a cell's text
  (`\___` for a literal).

### Fixed
- The editor no longer splits a hard-wrapped Markdown paragraph into one
  paragraph per line (e.g. `sample-test.md` Part 1 had become 18 paragraphs
  instead of 3), and a gloss tag can no longer be split across paragraphs.

## v0.4.1 — "Inline completion boxes + nav scroll fix" — 2026-07-19

### Fixed
- **Sentence/form/note completion answer boxes now render inline**, right where
  the `______` marker sits in the prompt (box goes at the end if there's no
  marker). Editor shows a tip explaining the `______` marker + word limit.
- **Clicking a navigation number now reliably scrolls to that question.** The
  old `scrollIntoView` could scroll the wrong container in the app's nested-
  scroll layout and leave the pane unmoved; a new pane-relative `scrollToQuestion`
  fixes it in every part.

## v0.4.0 — "New completion types + a critical passage-save fix" — 2026-07-19

### Added
- **Table completion** — a new question type: type answers into blank cells of a
  grid, with a full grid editor (columns/rows, tick a cell as a blank, set
  accepted answers).
- **Form completion** and **Note completion** — new choices in the type dropdown
  (they use the sentence-completion engine; put the field label in each prompt).
- **Summary completion — typed mode** — a "How students answer" toggle lets a
  summary be filled by *typing* (accepted answers + word limit) as well as by
  dragging phrases from a word bank.

### Fixed
- **Critical — passage edits could be lost.** The editor now saves the *whole*
  passage (not just `<p>` elements, which the browser doesn't always produce
  while editing) and **auto-saves as you type**, with a **"Saved ✓"** indicator
  in the passage toolbar. Switching part tabs can no longer drop edits.
- Completion answer boxes now sit inline and no longer stretch the line or shift
  text while typing.
- Clicking a navigation number reliably scrolls to that question.
- The "current question" blue outline no longer lingers on the previously
  selected box (it now clears from table cells and typed-blank inputs too).
- Removed stray full stops from the sample's matching prompts.

## v0.3.1 — "Shorter answer codes & distribution help" — 2026-07-19

### Added
- **📤 How to distribute**: a button beside "Generate with AI" opens a
  step-by-step guide for sending a finished test to students and getting their
  answers back.

### Changed
- **Shorter answer codes**: a student's answer code is now gzip-compressed
  before encoding (typically 3–5× smaller) while staying self-contained. Falls
  back to an uncompressed code on any browser without `CompressionStream`, and
  the importer reads either kind.
- Removed the redundant "View a student's answers" button from the editor — the
  home screen's "Review a student's work" section is now the single entry point.

## v0.3.0 — "Home-screen review, AI-assisted authoring & polish" — 2026-07-19

Makes the tool easier for non-technical teachers to pick up.

### Added
- **Review from the home screen**: a new "Review a student's work" section with
  **👀 View a student's answers** — paste a student's code to open their attempt
  in the test layout, with no test to load first.
- **Self-contained answer codes**: a student's code now carries the test as well
  as their answers, so any teacher can view it from a cold start.
- **🤖 Generate with AI**: a button on the "Create or import a test" heading opens
  a guided pop-up with a ready-made, format-perfect prompt (covering all nine
  question types) to paste into ChatGPT / Claude / Gemini, plus numbered step
  cards showing exactly what to do.

### Changed
- **Home screen reorganised** into three clearly labelled sections: *Take a test*
  / *Create or import a test* / *Review a student's work*.

### Polish
- Gentle entrance animation for every pop-up (backdrop fade + panel rise); the
  numbered step cards fade and slide in; hover / press / keyboard-focus feedback
  on the start-screen controls. Everything respects "reduce motion".

## v0.2.0 — "Paste-code submission & in-app review" — 2026-07-19

A lighter way for students to hand in their work — no emailing files around.

### Added
- **Student "📋 Export answer code"** on the results screen: produces a short
  code (name + answers + highlights + notes) the student copies and pastes
  wherever you ask — e.g. a shared Google Doc. If the browser blocks automatic
  copying (common on a double-clicked file), the code is pre-selected so
  Ctrl+C always works.
- **Teacher "📥 View a student's answers"** in the editor: paste a student's
  code to reopen their attempt in the normal test layout — their answers,
  highlights and notes — with the score recalculated live. A "Viewing [name]"
  banner with "← Back to editor" frames the read-only view.
- Answer codes are tagged with the test id; pasting a code from a different
  test warns you (with a "View anyway") instead of showing mismatched answers.

### Notes
- The score is never stored in the code — it's recomputed from the answers when
  you view it, so it's always correct.
- The existing "Download completed file" option is unchanged and still there.

## v0.1.0 — "Initial snapshot" — 2026-07-19

First backed-up version: a complete, single-file (double-click to run)
computer-delivered IELTS reading simulator.

### Included
- Full test-taking experience: two-pane layout, timer, per-question flags,
  four-colour text highlighting on both panes, anchored notes, text zoom, and
  an Inspera-style bottom navigation bar.
- Question types: True/False/Not Given, Yes/No/Not Given, multiple choice
  (single and several answers), sentence/note completion, matching (drag or
  dropdown), diagram labelling, summary completion (drag), and open-ended
  (not graded).
- Teacher authoring: visual editor with add/delete/reorder of parts, groups
  and questions; rich-text passage editing; "Create new test" from scratch
  with editable title and time; import or paste Markdown/JSON.
- Results: two-tier screen (per-part overview + detailed per-question review),
  estimated band, a written-answers section, and completed-file export.
- Restrained motion/interaction polish and keyboard focus states throughout.
