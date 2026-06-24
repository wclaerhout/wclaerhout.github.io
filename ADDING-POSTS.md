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

| Field         | What to put                                                        |
|---------------|--------------------------------------------------------------------|
| `title`       | Display title, in quotes.                                          |
| `date`        | `YYYY-MM-DD`. Controls ordering and the date shown on the cards.   |
| `description` | One or two sentences. Shown under the title.                       |
| `url`         | `/notebooks/<your-file>.html` (must match the file from step 2).   |
| `tags`        | List of words, no `#`. They render as `#tag`.                      |

### 4. Commit and push

```
git add notebooks/markov-chains.html _data/notebooks.yml
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
