### @export "prepcsv"
mydict["colleagues"] = [mydict["colleagues"]]
mylist = [(e["name"], e{"number"], k) for k, v in mydict.items() for e in v]

### @export "savecsv"
import csv
with open("data.csv", "w") as outfile:
    csv_out = csv.writer(outfile)
    csv_out.writerow(["name", "number", "relation"])
    for row in mylist:
        csv_out.writerow(row)
