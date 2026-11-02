from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    image = models.ImageField(upload_to='buildings/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Корпус'
        verbose_name_plural = 'Корпуса'


class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name='Корпус')
    room_number = models.CharField(max_length=10, verbose_name='Номер комнаты')
    capacity = models.IntegerField(verbose_name='Количество мест')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='rooms/', blank=True)

    def __str__(self):
        return f'{self.building.name} - Комната {self.room_number}'

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Guest(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='ФИО')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name='Гость')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    num_people = models.IntegerField(verbose_name='Количество человек')

    def __str__(self):
        return f'{self.guest.full_name} - {self.room}'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


class Stay(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name='Гость')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    num_people = models.IntegerField(verbose_name='Количество человек')

    def __str__(self):
        return f'{self.guest.full_name} - {self.room}'

    class Meta:
        verbose_name = 'Проживание'
        verbose_name_plural = 'Проживания'