# IBM Applied Data Science Capstone: Falcon 9 landings

This repository contains a reproducible analysis of IBM Skills Network's historical SpaceX course datasets and a report in the official 47-slide template.

## Files

- `SpaceX_API_and_Web_Sources.ipynb`: frozen SpaceX API response and the published web-source CSV. Live Wikipedia scraping returned HTTP 403 in this environment; the notebook states that limitation.
- `Capstone_Analysis.ipynb`: data checks, SQL examples, exploratory summaries, four classifiers and held-out results.
- `Folium_Launch_Sites.ipynb` and `spacex_sites.html`: interactive site markers and reference circles.
- `spacex_dashboard.py`: site selector, payload range slider, success pie and payload scatter view.
- `Data Science Capstone Project Report.pdf`: final presentation for IBM Mark.

## Reproduce

Install `requirements.txt`, then run the notebooks in the order listed above. Each notebook downloads the cited public IBM course dataset. The report uses a 90-row modelling sample, a separate 101-row SQL sample, and a 56-row dashboard sample.

## Result and limits

The 90-row sample has 60 successful first-stage landings. Three of four classifiers reach 77.8% test accuracy on an 18-row holdout. The small historical sample cannot support an operational forecast. Railway, highway and coastline distances are not available in the course CSV, so the report does not claim them.

This project was prepared with AI assistance and should be reviewed by the learner before academic submission.
