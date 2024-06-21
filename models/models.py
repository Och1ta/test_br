from django.db import models


class House(models.Model):
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address


class Apartment(models.Model):
    address = models.ForeignKey(House, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    percentage_ownership = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.number


class Resident(models.Model):
    full_name = models.CharField(max_length=255)
    passport_data = models.CharField(max_length=100)
    apartments = models.ManyToManyField(Apartment, through='Ownership')
    cars = models.ManyToManyField('Car', through='CarOwnership', related_name='owners')
    reserved_parking_spots = models.ManyToManyField('ParkingSpot', related_name='residents')

    def __str__(self):
        return self.full_name


class Car(models.Model):
    license_plate = models.CharField(max_length=20)
    brand = models.CharField(max_length=100)
    parking_spot = models.ForeignKey('ParkingSpot', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} ({self.license_plate})"


class CarOwnership(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    parking_spot = models.OneToOneField('ParkingSpot', on_delete=models.SET_NULL, null=True, blank=True)


class Ownership(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    percentage_ownership = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.resident.full_name} - {self.apartment.number}"


class ParkingSpot(models.Model):
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number
