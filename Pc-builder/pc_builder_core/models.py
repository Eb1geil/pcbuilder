from django.db import models


class Motherboard(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)  # Переименовано в model для соответствия JSON
    socket = models.CharField(max_length=50)
    chipset = models.CharField(max_length=50, null=True, blank=True)  # Добавлено поле chipset
    memoryfr = models.IntegerField(null=True, blank=True)  # Добавлено поле memoryfr
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Оставляем Decimal для цены
    ref = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"


class CPU(models.Model):
    brand = models.CharField(max_length=255)
    line = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    socket = models.CharField(max_length=50)
    cores = models.IntegerField(null=True, blank=True)
    threads = models.IntegerField(null=True, blank=True)
    max_frequency = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    base_frequency = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    benchmark = models.IntegerField(null=True, blank=True)
    ref = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.brand} {self.line} {self.model}"


class GPU(models.Model):
    brand = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    rank = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    benchmark = models.IntegerField(null=True, blank=True)
    memory = models.IntegerField(null=True, blank=True)  # GB
    energy = models.FloatField(null=True, blank=True)
    memorytype = models.CharField(max_length=50, null=True, blank=True)
    interface = models.CharField(max_length=50, null=True, blank=True)
    ref = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"


class RAM(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    memory = models.CharField(max_length=50)  # e.g., "8GB"
    frequency = models.CharField(max_length=50)  # e.g., "3200MHz"
    voltage = models.CharField(max_length=10, null=True, blank=True)
    ref = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"


class Storage(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    benchmark = models.IntegerField(null=True, blank=True)
    memory = models.CharField(max_length=50)  # e.g., "12TB"
    ref = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.name}"
