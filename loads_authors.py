import connect
import json

from mongoengine.errors import ValidationError, NotUniqueError
from models import Authors


try:
    with open("authors.json", "r", encoding="utf-8") as file:
        data = json.load(file)

except FileNotFoundError:
    print("❌ Файл authors.json не знайдений")
    exit()

except json.JSONDecodeError:
    print("❌ Помилка: JSON-файл пошкоджений або має неправильний формат")
    exit()


for el in data:

    try:
        author_name = el["fullname"]

        author = Authors.objects(fullname=author_name).first()

        if author:
            print(f"⚠️ Автор '{author_name}' вже існує")
            continue

        Authors(
            fullname=author_name,
            born_date=el["born_date"],
            born_location=el["born_location"],
            description=el["description"]
        ).save()

        print(f"✅ Автор '{author_name}' доданий")

    except KeyError as e:
        print(f"❌ У записі відсутнє поле: {e}")
        continue

    except (ValidationError, NotUniqueError) as e:
        print(f"❌ Помилка при збереженні автора '{el.get('fullname', 'невідомий')}': {e}")
        continue

    except Exception as e:
        print(f"❌ Невідома помилка: {e}")
        continue