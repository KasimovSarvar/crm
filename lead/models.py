from django.db import models

from abstraction.base_model import BaseModel
from authe.models import User

LEAD_STATUS = (
    ('lead', 'Lead'),
    ('possible', 'Possible'),
    ('canceled', 'Canceled'),
    ('closed', 'Closed'),
)

LEAD_TYPE = (
    ('instagram', 'Instagram'),
    ('telegram', 'Telegram'),
    ('sms', 'SMS'),
    ('facebook', 'Facebook'),
    ('other', 'Other'),
)

TYPE_PAYMENT = (
    (0, 'Cash'),
    (1, 'Card'),
    (2, 'Bank'),
    (3, 'Online'),
)

EDUCATION_TYPE_CHOICES = (
    ('bachelor', 'Bachelor'),
    ('magister', 'Magister')
)

PAYMENT_STATUS_CHOICES = (
    ('pending', 'PENDING'),
    ('payed', 'PAYED'),
    ('canceled', 'CANCELED')
)

STUDENT_STUDY_CHOICES = (
    ('grant', 'Grant'),
    ('contract', 'Contract'),
    ('evening', 'Evening'),
    ('extramural', 'Extramural')
)


class Lead(BaseModel):
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Администратор')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    passport_series = models.CharField(max_length=14, blank=True, null=True, verbose_name='Серия паспорта')
    phone_number = models.CharField(max_length=14, verbose_name='Номер телефона')
    status = models.CharField(max_length=10, choices=LEAD_STATUS, default='lead', verbose_name='Статус')
    type = models.CharField(max_length=11, choices=LEAD_TYPE, default='other', verbose_name='Тип')
    is_checked = models.BooleanField(default=False, verbose_name='Проверено')
    is_signing_at = models.DateField(blank=True, null=True, verbose_name='Подписан')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="leads",
                                   verbose_name="Создан каким HR")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'
        ordering = ('created_at',)



class Comment(BaseModel):
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_comment',
                              verbose_name='Администратор')
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, related_name='lead_comment',
                             verbose_name='Лид')

    comment = models.TextField(verbose_name='Коментарий')
    lead_status = models.CharField(max_length=100, blank=True, null=True, verbose_name='Лид статус')

    def save(self, *args, **kwargs):
        if not self.lead_status:
            self.lead_status = self.lead.status
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lead}"

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = 'Коментарии'
        ordering = ('created_at',)



class State(BaseModel):
    name = models.CharField(max_length=150, verbose_name="Название Государства")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Государство'
        verbose_name_plural = 'Государствa'
        ordering = ('created_at',)


class University(BaseModel):
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, verbose_name="Государство",
                              related_name='state_universities')
    name = models.CharField(max_length=150, verbose_name="Название университета")

    def __str__(self):
        return f"{self.state} {self.name}"

    class Meta:
        verbose_name = 'Университет'
        verbose_name_plural = 'Университеты'
        ordering = ('created_at',)


class Faculty(BaseModel):
    name = models.CharField(max_length=250, null=True, verbose_name='Название')
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, null=True, related_name='uni_faculty', verbose_name='Университет')
    education_type = models.CharField(
        max_length=10, choices=EDUCATION_TYPE_CHOICES, default='bachelor', verbose_name='Тип образования')
    grant = models.BooleanField(default=False, verbose_name='Грант')
    contract = models.BooleanField(default=False, verbose_name='Контракт')
    evening = models.BooleanField(default=False, verbose_name='Вечер')
    extramural = models.BooleanField(default=False, verbose_name='Заочный')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
        ordering = ('created_at',)


class Season(BaseModel):
    state = models.ForeignKey(State, on_delete=models.SET_NULL, verbose_name='Государство', blank=True, null=True)
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, verbose_name='Университет', blank=True, null=True)
    name = models.CharField(max_length=150, verbose_name='Название сезона', blank=True, null=True)
    start_date = models.DateTimeField(verbose_name='Начало сезона', blank=True, null=True)
    end_date = models.DateTimeField(verbose_name='Конец сезона', blank=True, null=True)

    closed = models.BooleanField(default=False, verbose_name='Закрыто')

    def __str__(self):
        return f"{self.state} {self.name}"

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'
        ordering = ('created_at',)


class SeasonFacultyLimit(BaseModel):
    season = models.ForeignKey(
        Season, on_delete=models.SET_NULL, null=True, related_name='faculty_limit', verbose_name='Сезон')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, verbose_name='Факультет')
    grant = models.PositiveIntegerField(default=0, verbose_name='Грант')
    contract = models.PositiveIntegerField(default=0, verbose_name='Контракт')
    evening = models.PositiveIntegerField(default=0, verbose_name='Вечер')
    extramural = models.PositiveIntegerField(default=0, verbose_name='Заочный')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Сезонный лимит факультета'
        verbose_name_plural = 'Сезонные границы факультета'
        ordering = ('created_at',)


class Student(BaseModel):
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Администратор")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, verbose_name="Государство", blank=True, null=True)
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, verbose_name="Университет", blank=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, verbose_name='Сезон', blank=True, null=True)
    education_type = models.CharField(max_length=10, choices=EDUCATION_TYPE_CHOICES, default='bachelor')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='student_faculty')
    study_format = models.CharField(max_length=20, choices=STUDENT_STUDY_CHOICES, default='contract')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    passport_series = models.CharField(max_length=12, null=True, blank=True, verbose_name='Серия паспорта')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="students",
                                   verbose_name="Создан каким HR")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ('created_at',)


class Payment(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    check_uploader = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Загрузчик чека', null=True,
                                       blank=True)
    confirmatory = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='confirmatory_user', verbose_name='Подтверждающий')
    type = models.IntegerField(default=3, choices=TYPE_PAYMENT, verbose_name='Способ оплаты')
    uploader_amount = models.FloatField(default=0)
    amount = models.FloatField(verbose_name='Сумма')
    check_file = models.FileField(upload_to='checks', verbose_name='Чек')
    is_payed = models.CharField(max_length=100, default='pending', choices=PAYMENT_STATUS_CHOICES,
                                verbose_name='Оплачено')
    comment = models.CharField(max_length=500, verbose_name='Коментарий')

    def __str__(self):
        return f"{self.student}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ('created_at',)


class CategoryOutlay(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    limit = models.IntegerField(default=0, verbose_name='Процент лимита')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория расхода'
        verbose_name_plural = 'Категории расходов'
        ordering = ('created_at',)


class Outcome(BaseModel):
    accountant = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Бухгалтер')
    category = models.ForeignKey(CategoryOutlay, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    description = models.CharField(max_length=500, verbose_name='Описание')
    amount = models.FloatField(default=0, verbose_name='Сумма')
    type = models.IntegerField(default=0, choices=TYPE_PAYMENT, verbose_name='Тип')

    def __str__(self):
        return f"{self.category} {self.amount}"

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
        ordering = ('created_at',)
