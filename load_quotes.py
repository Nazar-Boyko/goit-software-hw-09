import connect
import json

from mongoengine.errors import ValidationError, NotUniqueError
from models import Quotes, Authors


try:
    with open("quotes.json", "r", encoding="utf-8") as file:
        data = json.load(file)

except FileNotFoundError:
    print("❌ Файл quotes.json не знайдений")
    exit()

except json.JSONDecodeError:
    print("❌ Помилка: JSON-файл пошкоджений або має неправильний формат")
    exit()


for el in data:

    try:
        author_name = el["author"]

        author = Authors.objects(fullname=author_name).first()

        if not author:
            print(f"⚠️ Автор '{author_name}' не знайдений. Цитату пропущено.")
            continue

        # Перевірка, чи така цитата вже існує
        existing_quote = Quotes.objects(
            quote=el["quote"]
        ).first()

        if existing_quote:
            print(f"⚠️ Цитата вже існує: {el['quote'][:50]}...")
            continue

        Quotes(
            tags=el["tags"],
            author=author,
            quote=el["quote"],
        ).save()

        print(f"✅ Цитату додано: {el['quote'][:50]}...")

    except KeyError as e:
        print(f"❌ У JSON відсутнє поле: {e}")
        continue

    except (ValidationError, NotUniqueError) as e:
        print(f"❌ Помилка MongoDB: {e}")
        continue

    except Exception as e:
        print(f"❌ Невідома помилка: {e}")
        continue