# MetLife Match 91 Tracker

A public static tracker for World Cup 2026 Match 91, the Round of 16 match scheduled for MetLife Stadium on July 5, 2026.

Match 91 is:

- `Winner(Match 76) vs Winner(Match 78)`
- `Match 76 = Group C Winner (C1) vs Group F Runner-up (F2)`
- `Match 78 = Group E Runner-up (E2) vs Group I Runner-up (I2)`

The site is built for ticket holders who want a daily view of which teams are most likely to reach Match 91, with special attention on Brazil, Germany, Japan, Netherlands, Senegal, Norway, France, Ivory Coast, Ecuador, and Morocco.

## Public Site

GitHub Pages should serve the static site from:

`https://aipeterlab.github.io/metlife-match-91-tracker/`

The generated page lives at:

`docs/index.html`

Additional public artifacts:

- `docs/knockout-cn-et.html` - Chinese knockout bracket with all match times in U.S. Eastern Time.
- `docs/knockout-cn-et.svg` - direct SVG image for the corrected knockout bracket.

## What Updates Automatically

The updater regenerates:

- `data/tracker.json`
- `docs/index.html`
- `reports/latest.md`
- `reports/YYYY-MM-DD.md`

It collects or recalculates group standings, completed results, upcoming fixtures, goals for, goals against, goal difference, points, Match 91 projections, team probabilities, top Match 91 combinations, and Brazil path commentary.

## Data Sources

The automation uses FIFA's public match API as the primary source and computes standings from the official match records. If FIFA's API is unavailable, the script falls back to seeded tournament data so the site still builds.

Primary sources listed in each generated report include:

- FIFA World Cup 2026 tournament pages
- FIFA public match API records for competition `17`, season `285023`

Probabilities are model estimates based on current standings, remaining group fixtures, FIFA-ranking-based strength estimates, and simulated Match 76 / Match 78 outcomes. They are not betting advice.

## GitHub Pages Deployment

In the GitHub repository settings:

1. Go to **Settings**.
2. Open **Pages**.
3. Set source to **Deploy from a branch**.
4. Choose the default branch.
5. Choose `/docs` as the publishing folder.

## GitHub Actions Schedule

The workflow is in:

`.github/workflows/hourly-update.yml`

It currently runs every hour at `:23` past the hour. The offset avoids the top of the hour, when GitHub scheduled jobs can be delayed by heavier runner load. It can also be run through `workflow_dispatch`, which is used by the hourly watchdog when GitHub does not emit the native scheduled event. The schedule can be changed back to daily when hourly tracking is no longer needed.

The workflow:

1. Checks out the repository.
2. Installs Python dependencies.
3. Runs `python scripts/update_tracker.py`.
4. Commits changed data, reports, and website files automatically.

## Local Development

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Regenerate everything with live fetching:

```bash
python scripts/update_tracker.py
```

Regenerate from seeded fallback data only:

```bash
python scripts/update_tracker.py --no-fetch
```

Open the local static site:

```bash
python -m http.server 8000 -d docs
```

Then visit:

`http://localhost:8000`

## Project Structure

```text
data/tracker.json                 Generated data payload
docs/index.html                   GitHub Pages site
reports/latest.md                 Latest daily report
reports/YYYY-MM-DD.md             Archived daily reports
scripts/update_tracker.py         Data, simulation, report, and site generator
.github/workflows/hourly-update.yml Hourly automation
```
