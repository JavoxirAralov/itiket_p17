from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, DateTimeField, CharField, EmailField, ForeignKey, CASCADE, IntegerField, \
    BooleanField, ManyToManyField, PositiveIntegerField, DecimalField
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField


class CreatedBaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class StartEndBaseModel(Model):
    start_date = DateTimeField(auto_now_add=True)
    end_date = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    gender = BooleanField(default=True, null=True)
    city = ForeignKey('City', on_delete=models.CASCADE, blank=True, null=True)
    image = ResizedImageField()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Country(Model):
    name = CharField(max_length=70, unique=True)
    code = CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class City(Model):
    name = CharField(max_length=255)
    country = ForeignKey('Country', CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Event(StartEndBaseModel):
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    venue = ForeignKey('Venue', CASCADE)
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='event',
                              default='event/event_default/default.jpg')
    price = PositiveIntegerField(default=0)
    title = CharField(max_length=70)
    city = ForeignKey('City', CASCADE)
    category = ForeignKey('Category', CASCADE)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Promotion(Model):
    name = CharField(max_length=255)
    event = ManyToManyField('Event', blank=True, related_name='promotions')

    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def __str__(self):
        return self.name


class Session(StartEndBaseModel):
    name = CharField(max_length=70)
    price = PositiveIntegerField(default=0)
    event = ForeignKey('Event', CASCADE)
    order = ForeignKey('Order', CASCADE)

    def __str__(self):
        return self.name


class Location(Model):
    index = IntegerField()
    city = ForeignKey('City', CASCADE)
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
    is_deleted = BooleanField(default=False)
    order = ManyToManyField('Order', related_name='locations')

    def __str__(self):
        return str(self.index)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class Order(Model):
    firstname = CharField(max_length=70)
    lastname = CharField(max_length=70)
    phone = CharField(max_length=70)
    email = EmailField(unique=True)
    promo = ForeignKey('PromoCode', CASCADE)
    event = ForeignKey('Event', CASCADE)
    location = ForeignKey('Location', CASCADE, related_name='orders')
    courier = ForeignKey('Courier', CASCADE)

    def __str__(self):
        return self.firstname


class Category(Model):
    name = CharField(max_length=255)
    slug = CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Basket(Model):
    event = ForeignKey('Event', CASCADE)
    count = PositiveIntegerField(default=0)
    date = DateTimeField(auto_now_add=True)


class Like(Model):
    name = ForeignKey('User', on_delete=CASCADE)
    like = BooleanField(default=False)
    event = ForeignKey('Event', CASCADE)


class Venue(Model):
    banner = ResizedImageField(size=[1000, 320], crop=['middle', 'center'], upload_to='venues_banner')
    title = CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='venues',
                              default='venues/venues_default/default.jpg')
    location = ForeignKey('apps.Location', CASCADE)
    phone = CharField(max_length=70)
    address = CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Venue'
        verbose_name_plural = 'Venues'


class PromoCode(StartEndBaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Courier(Model):
    title = CharField(max_length=70)
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    street = CharField(max_length=100)
    building = CharField(max_length=100)
    house_number = CharField(max_length=100)
    index = CharField(max_length=100)
    country = ForeignKey('Country', CASCADE)
    city = ForeignKey('City', CASCADE)
