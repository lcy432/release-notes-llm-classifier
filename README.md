# WLIURA S26 — App Update History Dataset

A dataset of mobile app version histories with LLM-classified update
categories, built as the test task for the WLIURA S26 Research Assistant
position with Prof. Bo Bian (UBC Sauder School of Business, Finance Division).

**Final dataset:** 85 rows (10 apps × 2 platforms × multiple versions),
covering releases from 2008-07-11 to 2026-05-06.

📊 [View the methodology and findings summary →](SUMMARY.md)

📁 [Final spreadsheet (Excel) →](output/app_updates.xlsx)

---

## What this is

Each row is a single `(app, platform, version)` observation with 13 fields
specified in the task brief:

| # | Field | Source |
|---|---|---|
| 1 | `app_name` | Manually selected |
| 2 | `platform` | iOS or Android |
| 3 | `developer` | iTunes API / Google Play |
| 4 | `store_category` | iTunes API / Google Play |
| 5 | `version` | Source-dependent |
| 6 | `release_date` | Source-dependent (UTC, normalized) |
| 7 | `is_current` | Whether this is the live version |
| 8 | `initial_release` | iTunes API only (Android proxying not used) |
| 9 | `release_notes` | Original disclosure text |
| 10 | `categories` | **LLM-classified** (closed set of 10) |
| 11 | `llm_summary` | **LLM-generated** standardized summary, 5-15 words |
| 12 | `confidence` | LLM self-rated, for downstream auditing |
| 13 | `source_url` | Direct link to the source page |
| + | `data_quality_note` | Provenance and known limitations per row |

## Repository layout
.
├── SUMMARY.md                    # Methodology, findings, limitations (the deliverable)
├── README.md                     # This file
├── data/
│   ├── raw/
│   │   ├── current_versions.csv          # iTunes API + google-play-scraper output
│   │   ├── dataset_pre_llm.csv           # All 90 rows before LLM classification
│   │   └── llm_results_partial.csv       # LLM checkpoint (resume-safe)
│   └── processed/
│       └── app_updates_labeled.csv       # Final labeled dataset
├── output/
│   ├── app_updates.xlsx                  # The deliverable spreadsheet
│   └── figures/
│       ├── 01_coverage_and_confidence.png
│       ├── 02_update_timeline.png
│       └── 03_category_per_app.png
└── notebooks/
├── 02_collect_data.ipynb     # Data collection (iTunes / Wayback / APKMirror / Google Play)
├── 03_llm_classify.ipynb     # Prompt design + DeepSeek classification
└── 04_descriptive_stats.ipynb # Plots used in SUMMARY.md

## Key engineering choices

- **Network fetches use retry with exponential backoff embedded in the
  fetch function itself**, not as separate compensation logic — making
  collection re-runnable and idempotent.
- **Disk checkpoints every 10 LLM calls**: the batch classifier writes
  partial results to CSV every 10 rows. A network interruption costs
  at most 10 calls, and re-running the cell automatically skips already
  classified rows.
- **Stratified temporal sampling** for Android historical versions: pull
  ~500 candidates from APKMirror, sample 6 per app evenly across the date
  range. Avoids over-representing dense recent clusters.
- **Defensive JSON parsing of LLM output**: model responses are tolerated
  even when they include markdown code fences or leading/trailing prose.
  Schema validation downgrades any unrecognized category to `other`
  rather than crashing.
- **Multi-pattern HTML parsing for archived pages**: App Store page HTML
  changed significantly between 2008-2026. Three fallback regex patterns
  cover most snapshot eras without crashing on the rest.
- **`.env` for API keys, `.gitignore` configured to exclude it.**

## Data sources used

| Source | Status | Coverage |
|---|---|---|
| iTunes Lookup API (`itunes.apple.com/lookup`) | Official, public | 10/10 iOS apps |
| `google-play-scraper` (Python package) | Web scraping, gentle | 10/10 Android apps |
| Wayback Machine CDX API | Public, archival | iOS history 6/10 apps |
| APKMirror (BeautifulSoup) | Web scraping; Cloudflare-blocked for 5/10 | Android history 5/10 apps |
| Google Play web HTML | Web scraping | Android current `release_notes` backfill |

We deliberately did not use Apple's undocumented AMP `versionHistory` endpoint,
preferring the fully-public Wayback Machine for transparency.

## Reproducing

1. `pip install openai pandas requests google-play-scraper openpyxl python-dotenv beautifulsoup4 matplotlib`
2. Create `.env` with `DEEPSEEK_API_KEY=sk-...`
3. Run notebooks in order: `02_collect_data.ipynb` → `03_llm_classify.ipynb`
   → `04_descriptive_stats.ipynb`
4. Outputs land in `output/`

LLM classification cost ≈ ¥0.05 (USD ~$0.01) at DeepSeek-V3 prices for the
full 41-row run.

## Headline finding (see SUMMARY.md for the full discussion)

Across 50 category-label instances spanning 2008-2026, `ai_features` and
`privacy_data_policy` were assigned **zero times**. This includes ChatGPT,
whose six classified Android updates contain only "Minor fixes and
improvements" boilerplate. **App release-notes text appears to function more
as a brand-voice channel than as a regulatory-disclosure channel**, with
direct implications for empirical research designs that treat
release-notes language as a proxy for actual privacy or AI changes.

## License & attribution

This is a one-off academic exercise. The collected data is sourced from
public app stores and the Internet Archive. Per-source ToS apply. The code
is provided as-is.

---

*Submitted by Chengyu Liu, BSc Statistics @ UBC, May 7, 2026.*