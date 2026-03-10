### A map of Vladivostok for a particular purpose

## Download from OSM
https://overpass-api.de/api/map?bbox=131.75,42.9,132.4944,43.3497

```bash
# download fresh map from OSM mirror
curl --output map.osm "https://overpass-api.de/api/map?bbox=131.75,42.9,132.4944,43.3497"

python3 extract_streets.py
```

ChatGPT suggested URL:
```bash
curl -G https://overpass-api.de/api/interpreter --data-urlencode "data@vladivostok.overpassql" -o vladivostok.osm
```

**MapTiler Cloud** allows you to upload a GeoJSON and get vector tiles out of it.
See https://cloud.maptiler.com/tiles/019cd963-582d-7b02-8fbc-840bd9582951/ 