*Version demo1.1*

**Big Image Viewer** - проект, созданный командой Chicken Bacon Onion для просмотра больших изображений с минимальной задержкой

---

Как запустить:
1. ```pip install -r requirements.txt```
2. ```python manage.py makemigrations```
3. ```python manage.py migrate```
4. ```python manage.py runserver```

---

Как использовать:

На главной странице загрузите изображение, а затем перейдите по появившейся ссылке.

---

На данный момент реализовано:

- Разбиение изображения на тайлы и их динамическая подгрузка.
- Оптимизация для быстрой отдачи изображения, учитывая размерные параметры и выбранный масштаб.
- Поддержка нескольких уровней детализации для оптимизации трафика и ускорения просмотра на разных масштабах.
- Базовый пользовательский интерфейс (нуждается в доработках)

___

- *Команда Chicken Bacon Onion планирует и дальше развивать проект после окончания хакатона*
- *Большинство улучшений уже находится на стадии разработки*