📌 Loyihaning qisqacha tavsifi
Bu Institut CRM tizimi — institut uchun talabalar, o‘qituvchilar, kurslar va to‘lov jarayonlarini boshqarish uchun ishlab chiqilgan web-ilova. Tizim orqali foydalanuvchilar ma'lumotlarni kiritish, yangilash, ko‘rish va o‘chirish imkoniyatiga ega bo‘ladilar.

📦 Texnologiyalar:
Python 3.12

Django 5

Django REST Framework

PostgreSQL

JWT Authentication

Docker (optional)

📁 Loyihaning katalog tuzilishi:
```
institut_crm/
│
├── crm/                  # Asosiy Django app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── ...
│
├── institut_crm/         # Project sozlamalari
│   ├── settings.py
│   └── urls.py
│
├── manage.py
└── requirements.txt
```
⚙️ O‘rnatish va ishga tushirish:
1. Repository-ni klonlash:
```
git clone https://github.com/username/institut_crm.git
cd institut_crm
```
2. Virtual environment yaratish:
 ```
python -m venv venv
source venv/bin/activate  # yoki Windows uchun: venv\Scripts\activate
```
3. Zarur paketlarni o‘rnatish:
```
pip install -r requirements.txt
```
4. Ma'lumotlar bazasini sozlash:
settings.py faylida PostgreSQL ulanish parametrlarini to‘g‘rilang.

5. Migrations va superuser yaratish:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
6. Loyihani ishga tushirish:
```
python manage.py runserver
🔑 API Endpoints (namuna)
GET /api/students/ — Talabalar ro‘yxatini olish

POST /api/students/ — Yangi talaba qo‘shish

GET /api/teachers/ — O‘qituvchilar ro‘yxatini olish

POST /api/courses/ — Yangi kurs qo‘shish

va boshqalar...

🔒 Authentication
JWT token asosida avtorizatsiya qilinadi.

POST /api/token/ — Login uchun token olish

POST /api/token/refresh/ — Token yangilash

📖 Hissa qo‘shish:
Fork qiling.

Yangi branch yarating: git checkout -b feature/ismingiz

O‘zgarishlaringizni qo‘shing va commit qiling.

Push qiling: git push origin feature/ismingiz

Pull Request yuboring.
```

