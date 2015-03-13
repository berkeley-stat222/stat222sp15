### @export "mydict"
mydict = {
    "parents": [{"name": "mom",
                "number": "555-123-4567"},
               {"name": "dad",
                "number": "555-123-4567"}],
    "colleagues": {"name": "advisor",
                   "number": "555-123-4567"}
}
               
### @export "pprint"
mydict
import pprint
pprint.pprint(mydict)

### @export "xml"
from dict2xml import dict2xml
print(dict2xml(mydict))

### @export "json"
import json
print(json.dumps(mydict, indent=4, sort_keys=True))

### @export "yaml"
import yaml
print(yaml.dump(mydict))

### @export "savejson"
import json
with open("data.json", "w") as outfile:
    json.dump(mydict, outfile, indent=4, sort_keys=True)

### @export "prepcsv"
mydict["colleagues"] = [mydict["colleagues"]]
mylist = [(e["name"], e["number"], k) for k, v in mydict.items() for e in v]

### @export "savecsv"
import csv
with open("data.csv", "w") as outfile:
    csv_out = csv.writer(outfile)
    csv_out.writerow(["name", "number", "relation"])
    for row in mylist:
        csv_out.writerow(row)
