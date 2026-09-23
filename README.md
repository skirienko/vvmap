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
curl -G https://overpass-api.de/api/interpreter -H "Referer: https://vvmap.netlify.app/" --data-urlencode "data@vladivostok.overpassql" -o vladivostok.osm
```

**MapTiler Cloud** allows you to upload a GeoJSON and get vector tiles out of it.
See https://cloud.maptiler.com/tiles/019cd963-582d-7b02-8fbc-840bd9582951/ 

Mirror sites:
* https://overpass.kumi.systems/api/
* https://z.overpass-api.de/api/
* https://maps.mail.ru/osm/tools/overpass/api/
* https://overpass.osm.rambler.ru/cgi/

Source: https://cadshift.com/blog/qgis-overpass-406-not-acceptable-mirror-endpoints/