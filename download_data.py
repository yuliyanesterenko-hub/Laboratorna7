
import requests
import pandas as pd

url = (
    "https://api.worldbank.org/v2/country/UKR;USA/"
    "indicator/NE.EXP.GNFS.ZS"
)

params = {
    "date": "2015:2023",
    "format": "json",
    "per_page": 100
}

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    result = response.json()

    if len(result) < 2 or not result[1]:
        print("Дані не отримано.")
    else:
        rows = []

        for item in result[1]:
            if item["value"] is not None:
                rows.append({
                    "Country": item["country"]["value"],
                    "Year": int(item["date"]),
                    "Exports of goods and services (% of GDP)":
                        item["value"]
                })

        df = pd.DataFrame(rows)
        df.to_csv("exports.csv", index=False, encoding="utf-8-sig")

        print(df)
        print("Дані збережено у файлі exports.csv")

except (requests.RequestException, ValueError) as e:
    print("Не вдалося отримати дані:", e)
