import db, models
from datetime import datetime
from auth import AuthHandler

auth_handler = AuthHandler()

db.create_db_and_tables()

with db.Session(db.engine) as s:

    # --- Роли ---
    role_admin = models.Role(name="Администратор")
    role_user = models.Role(name="Пользователь")
    role_manager = models.Role(name="Менеджер")

    # --- Категории ---
    categories = [
        models.Category(name="Смартфоны"),
        models.Category(name="Ноутбуки"),
        models.Category(name="Планшеты"),
        models.Category(name="Наушники"),
        models.Category(name="Колонки"),
        models.Category(name="Умные часы"),
        models.Category(name="Телевизоры"),
        models.Category(name="Фотоаппараты"),
        models.Category(name="Игровые приставки"),
        models.Category(name="Мониторы"),
        models.Category(name="Клавиатуры"),
        models.Category(name="Мыши"),
    ]

    # --- Статусы заказов ---
    statuses = [
        models.Status(name="Создан"),
        models.Status(name="Обрабатывается"),
        models.Status(name="Отправлен"),
        models.Status(name="Доставлен"),
        models.Status(name="Отменен"),
    ]

    # --- Товары с их характеристиками ---
    products_data = [
        # Смартфоны
        {
            "name": "Смартфон Apple iPhone 15 Pro Max 256GB",
            "description": "Флагманский смартфон Apple с титановым корпусом и мощным процессором A17 Pro",
            "category": "Смартфоны",
            "price": 119990,
            "quantity": 10,
            "images": [
                ("https://example.com/iphone15_1.jpg", True),
                ("https://example.com/iphone15_2.jpg", False)
            ],
            "specs": {
                "Диагональ экрана": "6.7\"",
                "Процессор": "Apple A17 Pro",
                "Оперативная память": "8 ГБ",
                "Встроенная память": "256 ГБ",
                "Основная камера": "48 МП",
                "Аккумулятор": "4422 мАч"
            }
        },
        {
            "name": "Смартфон Samsung Galaxy S24 Ultra 512GB",
            "description": "Мощный смартфон с ИИ-функциями и 200-мегапиксельной камерой",
            "category": "Смартфоны",
            "price": 134990,
            "quantity": 10,
            "images": [
                ("https://example.com/samsung_s24_1.jpg", True),
                ("https://example.com/samsung_s24_2.jpg", False)
            ],
            "specs": {
                "Диагональ экрана": "6.8\"",
                "Процессор": "Snapdragon 8 Gen 3",
                "Оперативная память": "12 ГБ",
                "Встроенная память": "512 ГБ",
                "Основная камера": "200 МП",
                "Аккумулятор": "5000 мАч"
            }
        },
        {
            "name": "Смартфон Xiaomi 14T Pro 256GB",
            "description": "Доступный флагман с мощной камерой и быстрой зарядкой",
            "category": "Смартфоны",
            "price": 64990,
            "quantity": 10,
            "images": [
                ("https://example.com/xiaomi_14t_1.jpg", True)
            ],
            "specs": {
                "Диагональ экрана": "6.67\"",
                "Процессор": "MediaTek Dimensity 9300+",
                "Оперативная память": "12 ГБ",
                "Встроенная память": "256 ГБ",
                "Основная камера": "50 МП",
                "Аккумулятор": "5000 мАч"
            }
        },
        # Ноутбуки
        {
            "name": 'Ноутбук Apple MacBook Pro 16" M3 Pro',
            "description": "Профессиональный ноутбук для работы с видео и графикой",
            "category": "Ноутбуки",
            "price": 269990,
            "quantity": 10,
            "images": [
                ("https://example.com/macbook_pro_1.jpg", True),
                ("https://example.com/macbook_pro_2.jpg", False)
            ],
            "specs": {
                "Диагональ экрана": "16.2\"",
                "Процессор": "Apple M3 Pro",
                "Оперативная память": "18 ГБ",
                "Встроенная память": "512 ГБ SSD",
                "Видеокарта": "Встроенная",
                "Операционная система": "macOS"
            }
        },
        {
            "name": 'Ноутбук ASUS ROG Zephyrus G16',
            "description": "Игровой ноутбук с мощной видеокартой и высокочастотным дисплеем",
            "category": "Ноутбуки",
            "price": 189990,
            "quantity": 10,
            "images": [
                ("https://example.com/asus_g16_1.jpg", True)
            ],
            "specs": {
                "Диагональ экрана": "16\"",
                "Процессор": "Intel Core i9-14900HX",
                "Оперативная память": "32 ГБ",
                "Встроенная память": "1 ТБ SSD",
                "Видеокарта": "NVIDIA RTX 4070",
                "Операционная система": "Windows 11"
            }
        },
        {
            "name": 'Ноутбук Lenovo ThinkPad X1 Carbon Gen 12',
            "description": "Легкий и надежный бизнес-ноутбук с отличной автономностью",
            "category": "Ноутбуки",
            "price": 159990,
            "quantity": 10,
            "images": [
                ("https://example.com/thinkpad_1.jpg", True)
            ],
            "specs": {
                "Диагональ экрана": "14\"",
                "Процессор": "Intel Core Ultra 7",
                "Оперативная память": "16 ГБ",
                "Встроенная память": "512 ГБ SSD",
                "Видеокарта": "Встроенная",
                "Операционная система": "Windows 11"
            }
        },
        # Планшеты
        {
            "name": 'Планшет Apple iPad Pro 13" M4',
            "description": "Мощный планшет для творчества и работы с новым процессором M4",
            "category": "Планшеты",
            "price": 129990,
            "quantity": 10,
            "images": [
                ("https://example.com/ipad_pro_1.jpg", True)
            ],
            "specs": {
                "Диагональ экрана": "13\"",
                "Процессор": "Apple M4",
                "Оперативная память": "8 ГБ",
                "Встроенная память": "256 ГБ",
                "Поддержка Apple Pencil": "Да"
            }
        },
        {
            "name": 'Планшет Samsung Galaxy Tab S9 Ultra',
            "description": "Планшет с большим экраном для работы и мультимедиа",
            "category": "Планшеты",
            "price": 114990,
            "quantity": 10,
            "images": [
                ("https://example.com/galaxy_tab_1.jpg", True)
            ],
            "specs": {
                "Диагональ экрана": "14.6\"",
                "Процессор": "Snapdragon 8 Gen 2",
                "Оперативная память": "12 ГБ",
                "Встроенная память": "512 ГБ",
                "Поддержка S Pen": "Да"
            }
        },
        # Наушники
        {
            "name": 'Наушники Apple AirPods Max',
            "description": "Полноразмерные наушники премиум-класса с шумоподавлением",
            "category": "Наушники",
            "price": 64990,
            "quantity": 10,
            "images": [
                ("https://example.com/airpods_max_1.jpg", True)
            ],
            "specs": {
                "Тип": "Полноразмерные",
                "Беспроводные": "Да",
                "Активное шумоподавление": "Да",
                "Время работы": "20 ч"
            }
        },
        {
            "name": 'Наушники Sony WH-1000XM5',
            "description": "Лучшие наушники с шумоподавлением по версии многих экспертов",
            "category": "Наушники",
            "price": 39990,
            "quantity": 10,
            "images": [
                ("https://example.com/sony_xm5_1.jpg", True)
            ],
            "specs": {
                "Тип": "Полноразмерные",
                "Беспроводные": "Да",
                "Активное шумоподавление": "Да",
                "Время работы": "30 ч"
            }
        },
        # Колонки
        {
            "name": 'Колонка Sonos Era 100',
            "description": "Умная беспроводная колонка с отличным звуком",
            "category": "Колонки",
            "price": 28990,
            "quantity": 10,
            "images": [
                ("https://example.com/sonos_era_1.jpg", True)
            ],
            "specs": {
                "Беспроводная": "Да",
                "Wi-Fi": "Да",
                "Bluetooth": "Да",
                "Мощность": "30 Вт"
            }
        },
        {
            "name": 'Колонка JBL Charge 5',
            "description": "Портативная водозащищенная колонка с мощным звуком",
            "category": "Колонки",
            "price": 15990,
            "quantity": 10,
            "images": [
                ("https://example.com/jbl_charge_1.jpg", True)
            ],
            "specs": {
                "Беспроводная": "Да",
                "Bluetooth": "Да",
                "Влагозащита": "IP67",
                "Время работы": "20 ч"
            }
        },
        # Умные часы
        {
            "name": 'Apple Watch Ultra 2',
            "description": "Часы для экстремальных условий с большим экраном",
            "category": "Умные часы",
            "price": 84990,
            "quantity": 10,
            "images": [
                ("https://example.com/apple_watch_ultra_1.jpg", True)
            ],
            "specs": {
                "Диагональ экрана": "1.92\"",
                "GPS": "Да",
                "Пульсометр": "Да",
                "Влагозащита": "WR100",
                "Время работы": "36 ч"
            }
        },
        {
            "name": 'Samsung Galaxy Watch 6 Classic',
            "description": "Классические умные часы с вращающимся безелем",
            "category": "Умные часы",
            "price": 42990,
            "quantity": 10,
            "images": [
                ("https://example.com/galaxy_watch_1.jpg", True)
            ],
            "specs": {
                "Диагональ экрана": "1.5\"",
                "GPS": "Да",
                "Пульсометр": "Да",
                "Влагозащита": "50 м",
                "Время работы": "40 ч"
            }
        },
        # Телевизоры
        {
            "name": 'Телевизор Samsung QN90C 65" Neo QLED',
            "description": "Качественный телевизор с технологией Neo QLED и 4K",
            "category": "Телевизоры",
            "price": 219990,
            "quantity": 10,
            "images": [
                ("https://example.com/samsung_tv_1.jpg", True)
            ],
            "specs": {
                "Диагональ": "65\"",
                "Разрешение": "4K (3840x2160)",
                "Тип матрицы": "Neo QLED",
                "Частота обновления": "120 Гц",
                "Smart TV": "Tizen"
            }
        },
        {
            "name": 'Телевизор Sony Bravia XR A80L 55" OLED',
            "description": "Телевизор с OLED-экраном и идеальным черным цветом",
            "category": "Телевизоры",
            "price": 189990,
            "quantity": 10,
            "images": [
                ("https://example.com/sony_tv_1.jpg", True)
            ],
            "specs": {
                "Диагональ": "55\"",
                "Разрешение": "4K (3840x2160)",
                "Тип матрицы": "OLED",
                "Частота обновления": "120 Гц",
                "Smart TV": "Google TV"
            }
        },
        # Игровые приставки
        {
            "name": 'Игровая приставка Sony PlayStation 5 Slim',
            "description": "Обновленная версия популярной игровой консоли",
            "category": "Игровые приставки",
            "price": 59990,
            "quantity": 10,
            "images": [
                ("https://example.com/ps5_slim_1.jpg", True)
            ],
            "specs": {
                "Встроенная память": "1 ТБ SSD",
                "Поддержка 4K": "Да",
                "Поддержка 8K": "Да",
                "Беспроводной контроллер": "DualSense"
            }
        },
        {
            "name": 'Игровая приставка Xbox Series X',
            "description": "Мощная игровая консоль с поддержкой 4K и быстрой загрузкой",
            "category": "Игровые приставки",
            "price": 56990,
            "quantity": 10,
            "images": [
                ("https://example.com/xbox_series_x_1.jpg", True)
            ],
            "specs": {
                "Встроенная память": "1 ТБ SSD",
                "Поддержка 4K": "Да",
                "Поддержка 8K": "Да",
                "Беспроводной контроллер": "Xbox Wireless"
            }
        },
        # Мониторы
        {
            "name": 'Монитор LG UltraGear 27GP950-B 27" 4K',
            "description": "Игровой монитор с высокой частотой обновления и 4K",
            "category": "Мониторы",
            "price": 89990,
            "quantity": 10,
            "images": [
                ("https://example.com/lg_ultragear_1.jpg", True)
            ],
            "specs": {
                "Диагональ": "27\"",
                "Разрешение": "4K (3840x2160)",
                "Частота обновления": "144 Гц",
                "Время отклика": "1 мс",
                "Интерфейсы": "HDMI, DisplayPort, USB"
            }
        },
        {
            "name": 'Монитор Dell U2723QE 27" 4K',
            "description": "Профессиональный монитор для дизайнеров с отличной цветопередачей",
            "category": "Мониторы",
            "price": 72990,
            "quantity": 10,
            "images": [
                ("https://example.com/dell_u2723qe_1.jpg", True)
            ],
            "specs": {
                "Диагональ": "27\"",
                "Разрешение": "4K (3840x2160)",
                "Частота обновления": "60 Гц",
                "Тип матрицы": "IPS",
                "Интерфейсы": "HDMI, DisplayPort, USB-C"
            }
        },
        # Клавиатуры
        {
            "name": 'Механическая клавиатура Keychron K8 Pro',
            "description": "Беспроводная механическая клавиатура с подсветкой",
            "category": "Клавиатуры",
            "price": 12990,
            "quantity": 10,
            "images": [
                ("https://example.com/keychron_k8_1.jpg", True)
            ],
            "specs": {
                "Тип": "Механическая",
                "Беспроводная": "Да",
                "Подсветка": "RGB",
                "Тип переключателей": "Gateron G Pro"
            }
        },
        # Мыши
        {
            "name": 'Игровая мышь Logitech G Pro X Superlight',
            "description": "Суперлегкая беспроводная мышь для киберспорта",
            "category": "Мыши",
            "price": 15990,
            "quantity": 10,
            "images": [
                ("https://example.com/logitech_gpro_1.jpg", True)
            ],
            "specs": {
                "Тип": "Игровая",
                "Беспроводная": "Да",
                "Сенсор": "HERO 25K",
                "Вес": "63 г"
            }
        },
    ]

    # --- Характеристики (глобальные спецификации) ---
    specification_names = set()
    for product in products_data:
        for spec_name in product["specs"].keys():
            specification_names.add(spec_name)
    
    # Создаём спецификации
    specifications = {}
    for spec_name in specification_names:
        spec = models.Spec(name=spec_name)
        specifications[spec_name] = spec
        s.add(spec)

    # Добавляем роли
    for role in [role_admin, role_user, role_manager]:
        s.add(role)

    # Добавляем категории
    for cat in categories:
        s.add(cat)

    # Добавляем статусы
    for status in statuses:
        s.add(status)

    # Создаём товары (Product), изображения (Image) и связи с характеристиками (ProductSpecs)
    category_dict = {cat.name: cat for cat in categories}

    products = []
    images_list = []
    product_specs_list = []

    for product_data in products_data:
        category = category_dict[product_data["category"]]
        
        product = models.Product(
            name=product_data["name"],
            description=product_data["description"],
            category=category,
            price=product_data["price"],
            quantity=product_data["quantity"]
        )
        products.append(product)
        s.add(product)
        
        # Изображения
        for img_url, is_main in product_data["images"]:
            img = models.Image(
                image_link=img_url,
                is_main=is_main,
                product=product
            )
            images_list.append(img)
            s.add(img)
        
        # Характеристики товара (ProductSpecs)
        for spec_name, spec_value in product_data["specs"].items():
            spec = specifications.get(spec_name)
            if spec:
                product_spec = models.ProductSpecs(
                    product=product,
                    spec=spec,
                    value=spec_value
                )
                product_specs_list.append(product_spec)
                s.add(product_spec)

    # Делаем flush, чтобы получить ID созданных объектов
    s.flush()

    # --- Пользователи ---
    users = [
        models.User(
            login="Admin",
            password=auth_handler.get_password_hash("Admin"),
            email="admin@admin.admin",
            role=role_admin
        ),
        models.User(
            login="Sergey",
            password=auth_handler.get_password_hash("Sergey123"),
            email="sergey@example.ru",
            role=role_user
        ),
        models.User(
            login="Elena",
            password=auth_handler.get_password_hash("Elena2024"),
            email="elena@example.ru",
            role=role_user
        ),
        models.User(
            login="Mikhail",
            password=auth_handler.get_password_hash("Misha654"),
            email="mikhail@example.ru",
            role=role_user
        ),
        models.User(
            login="Manager",
            password=auth_handler.get_password_hash("Manager123"),
            email="manager@example.ru",
            role=role_manager
        ),
        models.User(
            login="Alex",
            password=auth_handler.get_password_hash("Alex789"),
            email="alex@example.ru",
            role=role_user
        ),
        models.User(
            login="Maria",
            password=auth_handler.get_password_hash("Maria456"),
            email="maria@example.ru",
            role=role_user
        ),
        models.User(
            login="Dmitry",
            password=auth_handler.get_password_hash("Dmitry321"),
            email="dmitry@example.ru",
            role=role_user
        ),
    ]

    for user in users:
        s.add(user)

    s.flush()

    # --- Заказы (Orders) ---
    # Создаём заказы для пользователей
    orders = [
        # Заказы Sergey
        models.Order(
            user=users[1],
            is_available=False,
            status=statuses[0],  # Создан
            address="г. Москва, ул. Тверская, д. 15, кв. 78",
            date=datetime.now()
        ),
        models.Order(
            user=users[1],
            is_available=False,
            status=statuses[3],  # Доставлен
            address="г. Москва, ул. Арбат, д. 10, кв. 45",
            date=datetime.now()
        ),
        # Заказы Elena
        models.Order(
            user=users[2],
            is_available=False,
            status=statuses[1],  # Обрабатывается
            address="г. Санкт-Петербург, Невский пр., д. 50, кв. 12",
            date=datetime.now()
        ),
        # Заказы Mikhail
        models.Order(
            user=users[3],
            is_available=False,
            status=statuses[2],  # Отправлен
            address="г. Казань, ул. Баумана, д. 25, кв. 8",
            date=datetime.now()
        ),
        # Заказы Alex
        models.Order(
            user=users[5],
            is_available=True,  # Активный заказ (корзина)
            status=None,
            address=None
        ),
        # Заказы Maria
        models.Order(
            user=users[6],
            is_available=False,
            status=statuses[4],  # Отменен
            address="г. Новосибирск, ул. Ленина, д. 5, кв. 33",
            date=datetime.now()
        ),
    ]

    for order in orders:
        s.add(order)

    s.flush()

    # --- Корзина (Cart) ---
    cart_items = [
        # Заказ Sergey #1 (Создан)
        models.Cart(order=orders[0], product=products[0], count=1),  # iPhone 15 Pro Max
        models.Cart(order=orders[0], product=products[3], count=1),  # MacBook Pro
        
        # Заказ Sergey #2 (Доставлен)
        models.Cart(order=orders[1], product=products[1], count=2),  # Samsung S24 Ultra
        
        # Заказ Elena (Обрабатывается)
        models.Cart(order=orders[2], product=products[8], count=1),  # Sony WH-1000XM5
        models.Cart(order=orders[2], product=products[10], count=1),  # JBL Charge 5
        
        # Заказ Mikhail (Отправлен)
        models.Cart(order=orders[3], product=products[5], count=1),  # Lenovo ThinkPad
        models.Cart(order=orders[3], product=products[15], count=1),  # LG Monitor
        
        # Активный заказ Alex (корзина)
        models.Cart(order=orders[4], product=products[2], count=1),  # Xiaomi 14T Pro
        models.Cart(order=orders[4], product=products[6], count=1),  # iPad Pro
        models.Cart(order=orders[4], product=products[17], count=1), # Keychron K8 Pro
        
        # Отмененный заказ Maria
        models.Cart(order=orders[5], product=products[13], count=1),  # Samsung QN90C
    ]

    for cart_item in cart_items:
        s.add(cart_item)

    s.flush()

    # --- Комментарии (Comments) ---
    comments = [
        models.Comments(
            product=products[0],
            user=users[1],
            rate=5,
            text="Отличный телефон! Камера просто потрясающая, батареи хватает на весь день."
        ),
        models.Comments(
            product=products[0],
            user=users[2],
            rate=4,
            text="Дорого, но качество того стоит. Спустя месяц использования - полет нормальный."
        ),
        models.Comments(
            product=products[1],
            user=users[3],
            rate=5,
            text="Лучший Android-смартфон! Искусственный интеллект реально помогает в работе."
        ),
        models.Comments(
            product=products[3],
            user=users[5],
            rate=5,
            text="MacBook Pro - это мощь! Рендерит видео за секунды, экран просто шикарен."
        ),
        models.Comments(
            product=products[4],
            user=users[6],
            rate=4,
            text="Отличный игровой ноутбук, но тяжеловат. Для дома - идеально."
        ),
        models.Comments(
            product=products[8],
            user=users[1],
            rate=5,
            text="Лучшее шумоподавление, которое я пробовал. В самолете спасает отлично."
        ),
        models.Comments(
            product=products[9],
            user=users[2],
            rate=5,
            text="Отличная портативная колонка! Звук мощный, бас глубокий. Влагозащита работает."
        ),
        models.Comments(
            product=products[12],
            user=users[3],
            rate=4,
            text="Телевизор отличный, но цена кусается. Картинка просто сказка."
        ),
        models.Comments(
            product=products[14],
            user=users[5],
            rate=5,
            text="PS5 Slim - компактная и мощная. Игры летают, загрузка мгновенная."
        ),
        models.Comments(
            product=products[17],
            user=users[6],
            rate=5,
            text="Лучшая клавиатура для программирования! Механика и беспроводная связь - топ."
        ),
    ]

    for comment in comments:
        s.add(comment)

    s.flush()
    s.add(models.Table(name="Product"))
    s.add(models.Table(name="Order"))
    s.add(models.Table(name="User"))
    s.add(models.Table(name="Comment"))
    s.add(models.Table(name="ProductSpecs"))

    # --- Коммит всех изменений ---
    s.commit()

    print("База данных успешно заполнена электронными товарами!")
    print(f"Создано товаров: {len(products)}")
    print(f"Создано пользователей: {len(users)}")
    print(f"Создано заказов: {len(orders)}")
    print(f"Создано комментариев: {len(comments)}")