import csv
import os
from datetime import datetime

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rashody.csv")
FIELDS = ["date", "amount", "category", "description"]


def load():
    """Читает все расходы из файла rashody.csv."""
    if not os.path.exists(FILE):
        return []
    expenses = []
    with open(FILE, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            expenses.append({
                "date": row["date"],
                "amount": row["amount"],
                "category": row["category"],
                "description": row["description"],
            })
    return expenses


def save(expense):
    """Дописывает один расход в конец файла."""
    new_file = not os.path.exists(FILE)
    with open(FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(expense)


def money(value):
    return f"{int(value):,}".replace(",", " ") + " ₸"


def print_table(expenses):
    if not expenses:
        print("  (нет расходов)")
        return
    for e in expenses:
        print(f"  {e['date']}  {money(e['amount']):>12}  {e['category']:<12} {e['description']}")


def total(expenses):
    return sum(int(e["amount"]) for e in expenses)


def for_month(expenses, year, month):
    # Ошибка 3 исправление: добавляем ведущий ноль для месяцев 1-9
    prefix = f"{year}-{month:02d}"
    return [e for e in expenses if e["date"].startswith(prefix)]


def by_category(expenses):
    categories = sorted({e["category"] for e in expenses})
    # Ошибка 2 исправление: создаем отдельный список для каждой категории
    groups = {cat: [] for cat in categories}
    for e in expenses:
        groups[e["category"]].append(e)
    return groups


def top(expenses, n=3):
    # Ошибка 1 исправление: преобразуем amount в int для правильной числовой сортировки
    return sorted(expenses, key=lambda e: int(e["amount"]), reverse=True)[:n]


def ask_int(prompt, low, high):
    while True:
        text = input(prompt).strip()
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
        print(f"  Введите целое число от {low} до {high}.")


def add_expense():
    while True:
        date_text = input("Дата (ГГГГ-ММ-ДД, пусто — сегодня): ").strip()
        if not date_text:
            date_text = datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            break
        except ValueError:
            print("  Неверная дата. Пример: 2026-10-21")
    amount = ask_int("Сумма (целое число): ", 1, 10_000_000)
    category = input("Категория: ").strip() or "Другое"
    description = input("Описание: ").strip()
    save({"date": date_text, "amount": amount, "category": category, "description": description})
    print("  Расход сохранён.")


def main():
    while True:
        print()
        print("===== УЧЁТ РАСХОДОВ =====")
        print("1 — Добавить расход")
        print("2 — Все расходы")
        print("3 — Расходы за месяц")
        print("4 — Итоги по категориям")
        print("5 — Три самых крупных расхода")
        print("0 — Выход")
        choice = input("Выберите пункт: ").strip()
        expenses = load()

        if choice == "1":
            add_expense()
        elif choice == "2":
            print_table(expenses)
            print(f"  ИТОГО: {money(total(expenses))}")
        elif choice == "3":
            year = ask_int("Год: ", 2000, 2100)
            month = ask_int("Месяц (1-12): ", 1, 12)
            selected = for_month(expenses, year, month)
            print_table(selected)
            print(f"  ИТОГО за {month:02d}.{year}: {money(total(selected))}")
        elif choice == "4":
            for category, items in by_category(expenses).items():
                print(f"  {category:<12} {len(items):>3} шт.  {money(total(items)):>12}")
        elif choice == "5":
            print_table(top(expenses))
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("  Нет такого пункта.")


if __name__ == "__main__":
    main()