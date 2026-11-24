---
layout: guide
title: How to add content
permalink: /guide/
sitemap: false
---

# How to add content

Everything in the post lists comes from **one file**: `_data/notebooks.yml`.
Put your file in `notebooks/`, add an entry to that list, push to `main`, and it
shows up on the **Home** page ("Latest entries", the three newest) and on the
**Posts** page automatically. You never edit `index.html` or `notebooks.html`.

This page lives at `/guide/`. It is not in the menu and asks search engines not
to index it. The same text is `ADDING-POSTS.md` in the repository.

---

## Quick checklist

1. Put the file in `notebooks/` with a short, lowercase, dash-separated name.
2. Add an entry at the **top** of `_data/notebooks.yml` (newest first).
3. Optional: preview locally (see below).
4. Commit and push to `main`. GitHub Pages rebuilds in about a minute.

---

## A Pluto notebook

In Pluto, top-right menu → **Export** → **Static HTML**. Save it as, for example,
`notebooks/markov-chains.html`, then add:

```yaml
- title: "Markov Chains"
  date: 2026-07-01
  description: "Short description of what the notebook does — one or two sentences."
  url: /notebooks/markov-chains.html
  tags: [markov, probability, pluto]
```

The site builds a readable post at `/notebooks/markov-chains/` from the export.
The notebook is not re-run: text, code, printed output and plots are taken as-is
from the results stored inside the export.

- Code you folded in Pluto stays hidden. The `using ...` cells at the top go into
  a collapsed "Setup code" box.
- Code is shown by default; readers can hide it with the **Hide code** button.
  Raw values a cell returns (arrays, models, tables) sit behind a small
  "show output" link; text, plots and what you print with `println` always show.
- Sliders (`@bind`) only work in the interactive version, which the post links to.

## A PDF (for example written in Typst)

Save it as `notebooks/my-typst-write-up.pdf` and add:

```yaml
- title: "My Typst write-up"
  date: 2026-12-01
  description: "One or two sentences."
  url: /notebooks/my-typst-write-up.pdf
  tags: [typst, notes]
```

The site builds a post at `/notebooks/my-typst-write-up/` that shows every page
as a sharp image under your title, date, tags and description, with
**Download PDF** and **Open full screen** buttons. The PDF itself is not changed.

## An article written directly (Markdown or HTML)

For a post you write straight into the site, like the Cross Entropy Method one,
create `_posts/2026-12-01-my-post.md` (the date in the name is required):

```markdown
---
layout: post
title: "My post"
date: 2026-12-01
tags: [julia]
lede: "Optional intro line shown under the title."
---

Your text in Markdown. Maths works with $$ ... $$ or \( ... \).
```

It is published at `/posts/my-post/`. To list it on Home and Posts as well, add
an entry to `_data/notebooks.yml` with `url: /posts/my-post/`.

---

## The fields in `_data/notebooks.yml`

| Field              | What to put                                                        |
|--------------------|--------------------------------------------------------------------|
| `title`            | Display title, in quotes.                                          |
| `date`             | `YYYY-MM-DD`. Controls ordering and the date shown in lists.       |
| `description`      | Short blurb — one or two sentences. Shown under the title.         |
| `description_file` | *Optional.* Use instead of `description` for longer text (see below). |
| `url`              | `/notebooks/<file>.html` or `.pdf`, or a `/posts/...` address.     |
| `tags`             | List of words, no `#`. Shown as "word · word" and used by the topic buttons on the Posts page. |

### Longer descriptions (optional)

For a longer description — several sentences, multiple paragraphs, or
Markdown — put the text in its own file so the YAML stays clean.

1. Create a Markdown file under `_includes/descriptions/`, e.g.
   `_includes/descriptions/markov-chains.md`.
2. In `_data/notebooks.yml`, drop the `description:` line and point to the file
   with `description_file: markov-chains.md` (just the filename, no folder).

If `description_file` is set it wins; otherwise `description` is used. The
**Bayesian Chess** entry uses this form.

---

## Your profile and research (top of the home page)

The top of the home page shows your name, role, a short bio, a photo and links,
then a **Research** list, then the learning journal. All of it is optional:
anything left empty is simply not shown.

**Profile.** In `_data/content.yml`, under `profile:`:

- `bio`: two or three sentences in your own words. Markdown links work.
- `photo`: put a portrait (roughly 4:5, about 400×500 px) in `assets/img/`,
  for example `assets/img/ward.jpg`, and set `photo: "/assets/img/ward.jpg"`.
  Don't start the file name with `_`, Jekyll skips those.
- `links`: fill in the `url` of each link you want. For email use
  `mailto:you@ugent.be`. For your CV, put the PDF in `assets/` (for example
  `assets/cv.pdf`) and set `url: "/assets/cv.pdf"`. Empty links are hidden.

**Publications.** Copy the same `.bib` you use for your CV to
`research/publications.bib`. The build reads it, newest year first, and prints
your name in bold (set by `me:` in `profile`, your surname). The Research list
and the **Research** menu item only appear once there is at least one entry.
Links come from these fields of each entry:

| Field in the .bib                    | Link shown |
|--------------------------------------|------------|
| `pdf = {/assets/papers/x.pdf}`       | PDF        |
| `doi = {10.1234/abcd}`               | DOI        |
| `url = {...}` (only when no `doi`)   | Link       |
| `eprint` + `archivePrefix = {arXiv}` | arXiv      |
| `code = {https://github.com/...}`    | Code       |

Run `python _tools/build_posts.py` again after changing the `.bib` to see it
in the local preview.

---

## Editing site text (home + about)

All wording on the **home page** (profile, journal label, title, intro) and the **about page**
(title, paragraphs, info cards, closing line) lives in one file:
`_data/content.yml`. Edit that file — no HTML needed. Markdown (`**bold**`,
`[links](url)`, `` `code` ``) works inside the about paragraphs. The `tags` list
under `home` is kept in the file but no longer shown on the page.

---

## Local preview (see changes before pushing)

Preview the whole site on your machine at `http://localhost:4000` before you
push, so GitHub only rebuilds when you actually mean to deploy.

### One-time setup

Ruby + the `github-pages` gem (matches the live build). In an **Administrator
PowerShell**:

```powershell
winget install RubyInstallerTeam.RubyWithDevKit.3.3
# reopen the terminal, then finish the MSYS2 devkit (press Enter for default):
ridk install 3
```

Then, in the repo:

```powershell
gem install bundler
bundle install
pip install msgpack pygments pyyaml pymupdf
```

> Installed to `C:\Ruby33-x64`. If `ruby -v` isn't found, reopen the terminal or
> add `C:\Ruby33-x64\bin` to your PATH.

### Every time you want to preview

```powershell
python _tools/build_posts.py
bundle exec jekyll serve --livereload
```

The first line builds the readable posts for your notebooks and PDFs; run it
again after adding or re-exporting one. Open **http://localhost:4000**. Edits to
`_data/*.yml`, `assets/css/`, layouts and pages rebuild automatically and the
browser reloads. Stop with `Ctrl+C`.

### Recommended workflow

1. Work on a `dev` branch, not `main`.
2. Preview locally until it looks right.
3. Push the branch and open a pull request. GitHub builds it as a check, without
   publishing. Merging into `main` deploys — `main` is always the live site.
