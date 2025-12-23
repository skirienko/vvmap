[out:xml][timeout:300];
relation
  ["boundary"="administrative"]
  ["admin_level"="6"]
  ["wikidata"="Q4112963"];
map_to_area->.vlad;

(
  way(area.vlad)["highway"]["name"];
  way(area.vlad)["bridge"="yes"]["name"];
);
out body;
>;
out skel qt;

