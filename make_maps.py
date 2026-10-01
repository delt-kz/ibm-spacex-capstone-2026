from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).parent

import folium
import pandas as pd


launches = pd.read_csv(ROOT / "launches.csv")
geo = json.loads((ROOT / "osm_vafb.json").read_text(encoding="utf-8"))
site = (34.632093, -120.610829)


def nearest_feature(kind: str):
    lat0, lon0 = site
    km_lon = 111.32 * math.cos(math.radians(lat0))
    km_lat = 110.574
    best = None
    for item in geo["elements"]:
        tags = item.get("tags", {})
        if kind == "coast" and tags.get("natural") != "coastline":
            continue
        if kind == "rail" and not (tags.get("railway") == "rail" and tags.get("usage") == "main"):
            continue
        if kind == "road" and tags.get("highway") not in {"motorway", "trunk", "primary", "secondary"}:
            continue
        points = item.get("geometry", [])
        for first, second in zip(points, points[1:]):
            ax = (first["lon"] - lon0) * km_lon
            ay = (first["lat"] - lat0) * km_lat
            bx = (second["lon"] - lon0) * km_lon
            by = (second["lat"] - lat0) * km_lat
            dx, dy = bx - ax, by - ay
            denominator = dx * dx + dy * dy
            weight = max(0, min(1, -(ax * dx + ay * dy) / denominator)) if denominator else 0
            x, y = ax + weight * dx, ay + weight * dy
            distance = math.hypot(x, y)
            if best is None or distance < best["distance_km"]:
                best = {
                    "distance_km": distance,
                    "latitude": lat0 + y / km_lat,
                    "longitude": lon0 + x / km_lon,
                    "osm_way_id": item["id"],
                    "name": tags.get("name", "unnamed"),
                    "tags": tags,
                }
    return best


features = {kind: nearest_feature(kind) for kind in ("coast", "rail", "road")}
(ROOT / "proximity.json").write_text(json.dumps(features, indent=2), encoding="utf-8")

florida = folium.Map(location=[28.59, -80.59], zoom_start=10, tiles="OpenStreetMap", control_scale=True)
florida_sites = ["CCAFS SLC 40", "KSC LC 39A"]
for name in florida_sites:
    sample = launches[launches.LaunchSite == name]
    lat, lon = float(sample.Latitude.iloc[0]), float(sample.Longitude.iloc[0])
    successes, count = int(sample.Class.sum()), len(sample)
    folium.Marker([lat, lon], popup=f"{name}: {successes}/{count} successful landings",
                  tooltip=name, icon=folium.Icon(color="blue", icon="info-sign")).add_to(florida)
    folium.Circle([lat, lon], radius=2500, color="#0b49cb", weight=2, fill=True,
                  fill_opacity=0.12).add_to(florida)
florida.save(str(ROOT / "folium_florida.html"))

outcomes = folium.Map(location=site, zoom_start=11, tiles="OpenStreetMap", control_scale=True)
counts = launches[launches.LaunchSite == "VAFB SLC 4E"].Class.value_counts().to_dict()
folium.Marker(site, popup=f"VAFB SLC 4E: {counts.get(1, 0)} success / {counts.get(0, 0)} failure",
              tooltip="VAFB SLC 4E", icon=folium.Icon(color="blue", icon="info-sign")).add_to(outcomes)
for index, (_, row) in enumerate(launches[launches.LaunchSite == "VAFB SLC 4E"].iterrows()):
    # Small offsets expose all 13 markers at one launch-pad coordinate.
    angle = index * (2 * math.pi / 13)
    lat = site[0] + 0.008 * math.sin(angle)
    lon = site[1] + 0.009 * math.cos(angle)
    color = "green" if int(row.Class) == 1 else "red"
    folium.CircleMarker([lat, lon], radius=6, color=color, fill=True,
                        fill_opacity=0.85, popup=f"Flight {int(row.FlightNumber)}: {'landing' if color == 'green' else 'no landing'}").add_to(outcomes)
outcomes.save(str(ROOT / "folium_outcomes.html"))

nearby = folium.Map(location=[34.655, -120.57], zoom_start=11, tiles="OpenStreetMap", control_scale=True)
folium.Marker(site, tooltip="VAFB SLC 4E", icon=folium.Icon(color="blue", icon="info-sign")).add_to(nearby)
colors = {"coast": "#0b49cb", "rail": "#168041", "road": "#d67800"}
for kind, feature in features.items():
    dest = [feature["latitude"], feature["longitude"]]
    text = f"{kind.title()}: {feature['distance_km']:.2f} km straight line"
    folium.Marker(dest, tooltip=text, popup=f"{text}; OSM way {feature['osm_way_id']}",
                  icon=folium.Icon(color={"coast": "blue", "rail": "green", "road": "orange"}[kind])).add_to(nearby)
    folium.PolyLine([site, dest], color=colors[kind], weight=4, tooltip=text).add_to(nearby)
nearby.save(str(ROOT / "folium_proximity.html"))
print(json.dumps(features, indent=2))
