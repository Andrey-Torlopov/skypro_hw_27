import csv
import json


def csv_to_json(csv_filepath, json_filepath, model):
    result = []
    with open(csv_filepath, encoding='utf-8') as csvf:
        for row in csv.DictReader(csvf):
            record = {"model": model, "pk": row["id"]}
            record["fields"] = row
            del row["id"]
            if "price" in row:
                row["price"] = int(row["price"])

            if "is_published" in row:
                row["is_published"] = row["is_published"] == "TRUE"

            result.append(record)

    with open(json_filepath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(result, ensure_ascii=False))


def convert_csv():
    csv_to_json("ads.csv", "ads.json", "ads.ad")
    csv_to_json("categories.csv", "categories.json", "ads.category")


if __name__ == "__main__":
    convert_csv()
