# Verification — 17 November 2026

## Research release

Code/data release: `ebfddb492b8240cfbe593d7ef20fb64c21205355`. All27 release files matched local Git blob hashes. Raw archives are excluded.

[GitHub research checks](https://github.com/Ehsan-Ch/market-risk-atlas/actions/runs/44089959103) succeeded on Python3.11, Python3.12 and Node22. Local checks passed10 Python tests and4 JavaScript tests. The independent export reconciliation checked all3167 forecasts, all model summaries, daily realized volatility and source/protocol digests. All14 source archive SHA256 hashes were verified during the full local build.

## Local browser evidence

Date, model and confidence-level controls changed metrics, chart and event tables. The10January EWMA99 export matched all288 saved observations, every risk estimate and the single threshold breach. Desktop layout and chart were visually inspected. No mobile or exhaustive cross-browser certification is claimed.

## Publication

[GitHub Pages deployment](https://github.com/Ehsan-Ch/market-risk-atlas/actions/runs/44090002468) succeeded for the research release above, served from main/root.

The [public report](https://ehsan-ch.github.io/market-risk-atlas/) loaded all results. Date/model/level controls updated the display. Its12January EWMA99 forecast export reconciled every one of288 rows, timestamps, returns, risk estimates and six threshold breaches with the saved study. The public comparison table showed the expected2.08% exceedance rate and1.111bps quantile loss for that selection. The study overview and chart were visually inspected, and a public screenshot was saved.

## Limits

CI verifies saved outputs and application logic, without downloading all source archives or rerunning the full data build. Verification establishes observed implementation behavior and reproducibility of stored results. It does not establish forecast reliability outside this short historical sample, attainable execution prices or investment performance. See RESEARCH.md.
