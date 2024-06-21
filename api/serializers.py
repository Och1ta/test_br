from rest_framework import serializers
from models.models import House, Apartment, Resident, Car, ParkingSpot, Ownership, CarOwnership


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    address = serializers.SlugRelatedField(slug_field='address', queryset=House.objects.all())

    class Meta:
        model = Apartment
        fields = '__all__'


class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    parking_spot = ParkingSpotSerializer()

    class Meta:
        model = Car
        fields = ['id', 'license_plate', 'brand', 'parking_spot']

    def create(self, validated_data):
        parking_spot_data = validated_data.pop('parking_spot')
        parking_spot = ParkingSpot.objects.create(**parking_spot_data)
        car = Car.objects.create(parking_spot=parking_spot, **validated_data)
        return car

    def update(self, instance, validated_data):
        instance.license_plate = validated_data.get('license_plate', instance.license_plate)
        instance.brand = validated_data.get('brand', instance.brand)

        parking_spot_data = validated_data.get('parking_spot')
        if parking_spot_data:
            parking_spot_id = parking_spot_data.get('id')
            if parking_spot_id:
                try:
                    parking_spot = ParkingSpot.objects.get(id=parking_spot_id)
                    instance.parking_spot = parking_spot
                except ParkingSpot.DoesNotExist:
                    pass

        instance.save()
        return instance

class ResidentSerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(many=True)
    cars = CarSerializer(many=True)
    reserved_parking_spots = serializers.PrimaryKeyRelatedField(many=True, queryset=ParkingSpot.objects.all())

    class Meta:
        model = Resident
        fields = ['full_name', 'passport_data', 'apartments', 'cars', 'reserved_parking_spots']

    def create(self, validated_data):
        apartments_data = validated_data.pop('apartments', [])
        cars_data = validated_data.pop('cars', [])
        reserved_parking_spots_data = validated_data.pop('reserved_parking_spots', [])

        resident = Resident.objects.create(**validated_data)

        for apartment_data in apartments_data:
            address = apartment_data.pop('address')
            house = House.objects.get(address=address)
            apartment = Apartment.objects.create(address=house, **apartment_data)
            Ownership.objects.create(resident=resident, apartment=apartment, percentage_ownership=apartment_data['percentage_ownership'])

        for car_data in cars_data:
            parking_spot_data = car_data.pop('parking_spot')
            parking_spot = ParkingSpot.objects.create(**parking_spot_data)
            car = Car.objects.create(parking_spot=parking_spot, **car_data)
            CarOwnership.objects.create(resident=resident, car=car, parking_spot=parking_spot)

        resident.reserved_parking_spots.set(reserved_parking_spots_data)
        return resident

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.passport_data = validated_data.get('passport_data', instance.passport_data)

        apartments_data = validated_data.get('apartments', [])
        cars_data = validated_data.get('cars', [])
        reserved_parking_spots_data = validated_data.get('reserved_parking_spots', [])

        # Update apartments
        for apartment_data in apartments_data:
            address_id = apartment_data.pop('address')
            try:
                apartment = Apartment.objects.get(address_id=address_id)
                for key, value in apartment_data.items():
                    setattr(apartment, key, value)
                apartment.save()
            except Apartment.DoesNotExist:
                apartment = Apartment.objects.create(address_id=address_id, **apartment_data)
            Ownership.objects.update_or_create(resident=instance, apartment=apartment, defaults={
                'percentage_ownership': apartment_data['percentage_ownership']})

        print('@@@@@@@@@@@@@@', cars_data)
        for car_data in cars_data:
            car_id = car_data.get('id')
            if car_id:
                try:
                    car = Car.objects.get(id=car_id)
                    car.license_plate = car_data.get('license_plate', car.license_plate)
                    car.brand = car_data.get('brand', car.brand)

                    parking_spot_data = car_data.get('parking_spot', {})
                    parking_spot_id = parking_spot_data.get('id')
                    if parking_spot_id:
                        parking_spot = ParkingSpot.objects.get(id=parking_spot_id)
                        car.parking_spot = parking_spot

                    car.save()

                    # Update CarOwnership if needed
                    CarOwnership.objects.update_or_create(
                        resident=instance, car=car,
                        defaults={'parking_spot': parking_spot}
                    )

                except Car.DoesNotExist:
                    pass  # Handle if car is not found or other exception

        # Update reserved parking spots
        instance.reserved_parking_spots.set(reserved_parking_spots_data)

        instance.save()
        return instance
