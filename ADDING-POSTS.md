# How to add a new post

Everything on the site is driven by **one file**: `_data/notebooks.yml`.
Add an entry there + drop your Pluto HTML in `notebooks/`, and it shows up on
both the **Home** page ("Latest entries") and the **Posts** tab automatically.

---

## Steps

### 1. Export your Pluto notebook to HTML

In Pluto, top-right menu → **Export** → **Static HTML**.
Save the file with a short, lowercase, dash-separated name, e.g. `markov-chains.html`.

### 2. Put the HTML in the `notebooks/` folder

```
notebooks/markov-chains.html
```

### 3. Add an entry to `_data/notebooks.yml`

Open `_data/notebooks.yml` and add a block at the **top** (newest first — the top
entry is the one shown as "Latest" on the home page):

```yaml
- title: "Markov Chains"
  date: 2026-07-01
  description: "Short description of what the notebook does — one or two sentences."
  url: /notebooks/markov-chains.html
  tags: [markov, probability, pluto]
```

Field guide:

| Field              | What to put                                                        |
|--------------------|--------------------------------------------------------------------|
| `title`            | Display title, in quotes.                                          |
| `date`             | `YYYY-MM-DD`. Controls ordering and the date shown on the cards.   |
| `description`      | Short blurb — one or two sentences. Shown under the title.         |
| `description_file` | *Optional.* Use instead of `description` for longer text (see below). |
| `url`              | `/notebooks/<your-file>.html` (must match the file from step 2).   |
| `tags`             | List of words, no `#`. They render as `#tag`.                      |

### Longer descriptions (optional)

For a short blurb, just use `description:` as above. If you want to write a
longer description — several sentences, multiple paragraphs, or Markdown — put
the text in its own file so the YAML stays clean.

1. Create a Markdown file under `_includes/descriptions/`, e.g.
   `_includes/descriptions/markov-chains.md`:

   ```markdown
   A longer write-up of what the notebook explores. You can use **Markdown**
   here — multiple paragraphs, emphasis, links — and it renders under the
   title on the cards.
   ```

2. In `_data/notebooks.yml`, drop the `description:` line and point to the file
   with `description_file:` (just the filename, no folder):

   ```yaml
   - title: "Markov Chains"
     date: 2026-07-01
     description_file: markov-chains.md
     url: /notebooks/markov-chains.html
     tags: [markov, probability, pluto]
   ```

Rules:

- If `description_file` is set it wins; otherwise `description` is used.
- The path is relative to `_includes/descriptions/` — give the filename only.
- Content is rendered as Markdown.

The **Bayesian Chess** entry uses this form — see
`_includes/descriptions/bayesian-chess.md` for a working example.

### 4. Commit and push

```
git add notebooks/markov-chains.html _data/notebooks.yml
# also add the description file if you made one:
# git add _includes/descriptions/markov-chains.md
git commit -m "add Markov chains notebook"
git push
```

Wait ~1 minute for GitHub Pages to rebuild, then hard-refresh (Ctrl+Shift+R).

---

## Notes

- **Order = newest at top.** The first entry in `_data/notebooks.yml` is the
  featured "Latest" post on the home page.
- **The home page updates itself.** You do NOT edit `index.html` or
  `notebooks.html` — they both read from `_data/notebooks.yml`.
- **Clicking a card opens the Pluto HTML directly** on the site
  (`/notebooks/<file>.html`) — no redirect to GitHub.
- One existing entry (Cross Entropy Method) points at a hand-written article
  (`/posts/cross-entropy-method/`) instead of a raw Pluto file. For your normal
  Pluto notebooks, just use the `/notebooks/...html` form shown above.

---

## Editing site text (home + about)

All wording on the **home page** (hero label, title, intro, tags) and the
**about page** (title, paragraphs, info cards, closing line) lives in one file:
`_data/content.yml`. Edit that file — no HTML needed. Markdown (`**bold**`,
`[links](url)`, `` `code` ``) works inside the about paragraphs.

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
```

> Installed to `C:\Ruby33-x64`. If `ruby -v` isn't found, reopen the terminal or
> add `C:\Ruby33-x64\bin` to your PATH.

### Every time you want to preview

```powershell
bundle exec jekyll serve --livereload
```

Open **http://localhost:4000**. Edits to `_data/*.yml`, `assets/css/`, layouts,
and pages rebuild automatically and the browser reloads. Stop with `Ctrl+C`.

### Recommended workflow

1. Work on a `dev` branch, not `main`.
2. Preview locally with `jekyll serve` until it looks right.
3. Merge `dev` → `main` (or push `dev` + open a PR). **That** push triggers the
   GitHub Pages deploy — `main` is always the live site.
