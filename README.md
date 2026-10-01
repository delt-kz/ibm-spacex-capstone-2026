# IBM Applied Data Science Capstone: Falcon 9 landings

Reproducible analysis of IBM Skills Network's historical SpaceX course datasets, with a 47-slide PDF report.

## Files

- `SpaceX_API_and_Web_Sources.ipynb`: course API snapshot and published web-source CSV. A live Wikipedia scrape returned HTTP 403 here; the notebook records this limitation.
- `Capstone_Analysis.ipynb`: data checks, SQL examples, exploratory summaries, four classifiers and held-out results.
- `Folium_Launch_Sites.ipynb`: site markers and proximity results.
- `make_maps.py`, `launches.csv`, `osm_vafb.json`: code and source data for three Folium maps.
- `folium_florida.html`, `folium_outcomes.html`, `folium_proximity.html`: interactive map outputs.
- `spacex_dashboard.py`: site selector, payload slider, success pie and payload scatter.
- `Data Science Capstone Project Report.pdf`: final presentation submitted to IBM Mark.

## Reproduce

Install `requirements.txt`; run the notebooks. `python make_maps.py` regenerates the Folium maps and `proximity.json` from the included IBM launch CSV and OpenStreetMap extract. Other notebooks fetch cited public IBM datasets.

## Results and limits

The 90-row modelling sample contains 60 successful landings. Decision tree, logistic regression and SVM each score 77.8% on an 18-row holdout. The decision tree has the highest five-fold cross-validation score, 87.6%. The sample is small and historical; it is not an operational forecast.

At VAFB SLC 4E, the mapped coastline is about 1.35 km away, the nearest main railway 1.27 km, and the nearest major mapped road 5.63 km. These are straight-line estimates from OpenStreetMap/Overpass geometries (28 July 2026 snapshot), not causal factors or road distances.

The project was prepared with AI assistance and should be reviewed by the learner before academic submission.
