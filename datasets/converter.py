import csv
import json

# Ads Id,name,author_id,price,description,is_published,image,category_id
# Category # id,name
# Location id,name,lat,lng
# User id,first_name,last_name,username,password,role,age,location_id


def csv_to_json(filepath, model) -> None:
    result = []
    with open(f'{filepath}.csv', encoding='utf-8') as csv_file:
        for row in csv.DictReader(csv_file):
            record = {"model": model, "pk": row["id"]}
            record["fields"] = row
            del row["id"]
            if "price" in row:
                row["price"] = int(row["price"])

            if "is_published" in row:
                row["is_published"] = row["is_published"] == "TRUE"

            if "age" in row:
                row["age"] = int(row["age"])

            if "location_id" in row:
                row["location"] = [row["location_id"]]
                del row["location_id"]

            result.append(record)

    with open(f'{filepath}.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))


def convert_csv() -> None:
    # csv_to_json("ad", "ads.ad")
    # csv_to_json("category", "ads.category")
    # csv_to_json("location", "users.location")
    csv_to_json("user", "users.user")


if __name__ == "__main__":
    convert_csv()
