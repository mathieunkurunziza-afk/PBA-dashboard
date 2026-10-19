# PBA School Dashboard

A simple, phone-friendly dashboard for education officials with two pages:

- **Project Assignment** (opens first) – downloaded projects, DOS surveys on time, how PBA teachers are assigning projects, Green / Yellow / Red school status, and the Red and Yellow schools that need support.
- **School Competition** – schools that held a competition, schools that reached the target of 40 students (20 S5 + 20 S6), and student numbers.

Lists show 10 rows first, with a "Show all" button. School codes are not shown.

Officials filter from **Province → District → Sector → School**. Tapping a name in a table or bar also drills down.

## How the data flows

```
Google Sheet ("Dashboard feed" tab)
        │  published as CSV
        ▼
GitHub Action (every hour)  ──►  data/active_schools.csv  (the "database" in GitHub)
                                         │
                                         ▼
                         GitHub Pages website (index.html)  ──►  500 officials
```

You keep entering data in the Google Sheet as usual. Within about an hour it appears on the dashboard. Nobody has to touch GitHub after setup.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole dashboard (one page, no installation needed). Built from `src/dashboard.html` by `python3 build.py` |
| `data/active_schools.csv` | The data the dashboard reads. Starts as a small **sample**; the Action replaces it with the full sheet |
| `data/meta.json` | "Last updated" time, written by the Action |
| `.github/workflows/update-data.yml` | The hourly job that copies the sheet into `data/` |

---

## Setup (one time, about 20 minutes)

### Step 1 – Add a "Dashboard feed" tab in the Google Sheet

This tab holds only the columns the dashboard needs, so you publish nothing else (no DOS/HT attendance, etc.).

1. Open **2026_2027 Performance metrics Working Plan**.
2. Add a new tab and name it **Dashboard feed**.
3. In cell **A1**, paste:

   ```
   ={'Active schools'!A:D, 'Active schools'!K:K, 'Active schools'!M:U}
   ```

   (If your sheet uses `;` in formulas, use `={'Active schools'!A:D \ 'Active schools'!K:K \ 'Active schools'!M:U}`.)

   It copies: Province, District, Sector, School_Name, School level competition, S5, S6, Total students, Downloaded projects, DOS survey, and the four PBA teacher columns. It updates automatically when *Active schools* changes.

> The dashboard finds columns by their **header name**, not position. Please don't rename these headers in *Active schools*. Adding new columns elsewhere is fine.

### Step 2 – Publish that tab as CSV

1. **File → Share → Publish to web**.
2. Under *Link*, choose the **Dashboard feed** tab (not "Entire document") and **Comma-separated values (.csv)**.
3. Click **Publish** and copy the link. It ends in `output=csv`.

> Anyone with this link can download the *Dashboard feed* tab. It holds school-level numbers only, no names of students or teachers.

### Step 3 – Create the GitHub repository

1. On GitHub, click **New repository**. Name it e.g. `pba-dashboard`, set it to **Public**, and create it.
2. Click **Add file → Upload files** and drag in `index.html`, `README.md` and the `data` folder. Click **Commit changes**.
3. The workflow file is inside a hidden folder, so create it by hand: **Add file → Create new file**, type the name `.github/workflows/update-data.yml`, paste the contents of that file, and commit.

### Step 4 – Give GitHub the sheet link

1. In the repository: **Settings → Secrets and variables → Actions → New repository secret**.
2. Name: `SHEET_CSV_URL`. Value: the link from Step 2. Save.

### Step 5 – Load the real data now

1. Open the **Actions** tab. If asked, click **I understand… enable workflows**.
2. Click **Update dashboard data → Run workflow**.
3. After about 30 seconds you should see a green tick ✅. `data/active_schools.csv` now has all your schools.

If it shows a red ✕, open it. The message says what's wrong, for example the wrong tab published. The old data is never replaced by a broken file.

### Step 6 – Turn on the website

1. **Settings → Pages**.
2. *Source*: **Deploy from a branch**. *Branch*: `main`, folder `/ (root)`. Save.
3. After 1–2 minutes the address appears at the top, e.g. `https://YOUR-ORG.github.io/pba-dashboard/`.

---

## Sharing with officials

Send the website address. Officials can also bookmark **their own area**: the address changes as they filter, for example:

```
https://YOUR-ORG.github.io/pba-dashboard/#page=assignment&province=East&district=Kirehe
```

Sending each district its own link means they land directly on their district.

## Changing settings

Open `index.html` on GitHub, click the pencil ✏️, and edit the **SETTINGS** block at the top:

| Setting | Meaning |
|---|---|
| `DATA_URL` | Where data comes from (see below) |
| `TITLE`, `SUBTITLE` | Text at the top |
| `GREEN_ABOVE` / `RED_BELOW` | School colour rule (default: Green > 80%, Red < 50%) |
| `COUNT_SOME_AS_ASSIGNED` | `true` = a teacher who assigned in *some* classes counts as "assigned" for the colour rule. `false` = only teachers who assigned in *all* classes count |
| `AUTO_REFRESH_MINUTES` | How often an open page reloads the data |

### Want it faster than hourly?

Set `DATA_URL` to the published CSV link from Step 2 instead of `data/active_schools.csv`. The dashboard then reads the Google Sheet directly, and changes show within about 5 minutes. The GitHub copy (and its Action) is then only a backup.

## How numbers are calculated

- **Held a competition**: *School level competition* is 1 (or Yes).
- **Students**: *Total students* (S5 + S6) of schools that held a competition.
- **Downloaded projects**: "Yes" = downloaded. Blank = **Not yet done**.
- **DOS survey on time**: "Yes" = on time. Anything else = **Not yet**.
- **School status** (only when *School total PBA teachers* is filled):
  share assigned = (all classes + some classes) ÷ total teachers.
  Green if more than 80%, Red if less than 50%, otherwise Yellow.
  Schools with no teacher numbers are **Not yet reported**.
- **Schools that need support**: Red and Yellow schools (Red first).
- **Competition target**: a school reaches it with at least 40 students; the card also says how many have 20+ in both S5 and S6.

## Things to know

- GitHub's hourly schedule can run a few minutes late on busy days.
- GitHub pauses scheduled jobs in a repository that has had no activity for 60 days. If the data stops updating, open **Actions** and re-enable the workflow.
- A public repository means the website and its data file are public. A private site needs a paid GitHub plan (GitHub Enterprise Cloud for login-protected Pages).
