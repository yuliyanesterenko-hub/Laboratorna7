
import pandas as pd
import matplotlib.pyplot as plt

try:
    df = pd.read_csv("exports.csv")

    # Перевірка стовпців
    if not all(col in df.columns for col in [
        "Country", "Year",
        "Exports of goods and services (% of GDP)"
    ]):
        print("Неправильна структура CSV-файлу.")
        raise SystemExit

    indicator = "Exports of goods and services (% of GDP)"

    # 1. Графік для України та США
    countries = ["Ukraine", "United States"]
    selected = df[df["Country"].isin(countries)]

    if selected.empty:
        print("Не знайдено даних для потрібних країн.")
        raise SystemExit

    for country in countries:
        part = selected[selected["Country"] == country]
        plt.plot(part["Year"], part[indicator],
                 marker="o", label=country)

    plt.title("Exports of goods and services (% of GDP)")
    plt.xlabel("Year")
    plt.ylabel("Indicator value (%)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 2. Стовпчаста діаграма
    country = input("Введіть назву країни англійською: ").strip()

    part = df[df["Country"].str.casefold() == country.casefold()]

    if part.empty:
        print("Такої країни немає у файлі.")
    else:
        part = part.sort_values("Year")
        plt.bar(part["Year"], part[indicator])
        plt.title("Exports - " + part.iloc[0]["Country"])
        plt.xlabel("Year")
        plt.ylabel("Indicator value (%)")
        plt.grid(axis="y")
        plt.show()

    # 3. Кругова діаграма
    year = input("Введіть рік: ").strip()

    part = df[
        (df["Year"].astype(str) == year) &
        (df["Country"].isin(countries))
    ]

    if len(part) != 2:
        print("Немає даних для обох країн за цей рік.")
    elif part[indicator].isna().any() or (part[indicator] < 0).any():
        print("Некоректні дані для діаграми.")
    elif part[indicator].sum() == 0:
        print("Неможливо побудувати кругову діаграму.")
    else:
        plt.pie(
            part[indicator],
            labels=part["Country"],
            autopct="%1.1f%%"
        )
        plt.title("Comparison for " + year)
        plt.show()

except FileNotFoundError:
    print("Файл exports.csv не знайдено.")

except (PermissionError, UnicodeError, pd.errors.ParserError) as e:
    print("Помилка читання файлу:", e)
