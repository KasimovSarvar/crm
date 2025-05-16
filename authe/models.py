from django.db import models
from abstraction.base_model import BaseModel

USER_ROLE = (
    (1, 'SuperUser'),
    (2, 'HR'),
    (3, 'Accountant'),
    (4, 'Admin')
)

USER_STATUS = (
    (0, 'Blocked'),
    (1, 'Active')
)


class User(BaseModel):
    username = models.CharField(max_length=100, verbose_name='Имя пользователя', unique=True)
    password = models.CharField(max_length=255, verbose_name='Пароль')
    full_name = models.CharField(max_length=100, verbose_name="Полное имя")
    role = models.IntegerField(choices=USER_ROLE, default=4, verbose_name="Роль")
    fixed_salary = models.FloatField(default=0, verbose_name="Фиксированная зарплата")
    phone_number = models.CharField(max_length=14, verbose_name="Номер телефона")
    status = models.IntegerField(choices=USER_STATUS, default=1, verbose_name="Статус")
    lead_number = models.PositiveIntegerField(default=0, verbose_name="Количество лидов")
    login_time = models.DateTimeField(null=True, blank=True, verbose_name='Время входа')

    def __str__(self):
        return self.username

