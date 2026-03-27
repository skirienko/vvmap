[out:xml][timeout:300];
relation
  ["boundary"="administrative"]
  ["admin_level"="6"]
  ["wikidata"="Q4112963"];
map_to_area->.vlad;

(
  way(area.vlad)["highway"]["name"];
  way(area.vlad)["bridge"="yes"]["name"];
  relation(id:7063164,
    2247428,
    7310557,
    1933752,
    3372537
  );
);
out body;
>;
out skel qt;
