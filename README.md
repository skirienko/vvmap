### A map of Vladivostok for a particular purpose

## Download from OSM
https://overpass-api.de/api/map?bbox=131.75,42.9,132.4944,43.3497

```bash
# download fresh map from OSM mirror
curl --output map.osm "https://overpass-api.de/api/map?bbox=131.75,42.9,132.4944,43.3497"

python3 extract_streets.py
```