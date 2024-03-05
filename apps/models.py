from django.contrib.auth.models import AbstractUser
from django.db.models import Model, DateTimeField, CharField, EmailField, ForeignKey, CASCADE, TextField, IntegerField, \
    BooleanField, DateField, BigIntegerField, ManyToManyField, PositiveIntegerField, DecimalField
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
    city = ForeignKey('apps.City', CASCADE, related_name='cities', default=True, null=True)

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
    country = ForeignKey('apps.Country', CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Event(StartEndBaseModel):
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    venue = ForeignKey('apps.Venue', CASCADE)
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='event',
                              default='event/event_default/default.jpg')
    price = PositiveIntegerField(default=0)
    title = CharField(max_length=70)
    city = ForeignKey('apps.City', CASCADE)
    category = ForeignKey('apps.Category', CASCADE)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Promotion(Model):
    name = CharField(max_length=255)
    event = ManyToManyField('apps.Event', blank=True)

    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def __str__(self):
        return self.name


class Session(StartEndBaseModel):
    name = CharField(max_length=70)
    price = PositiveIntegerField(default=0)
    event = ForeignKey('apps.Event', CASCADE)
    order = ForeignKey('apps.Order', CASCADE)

    def __str__(self):
        return self.name


class Location(Model):
    index = IntegerField()
    city = ForeignKey('apps.City', CASCADE)
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.index

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class Order(Model):
    firstname = CharField(max_length=70)
    lastname = CharField(max_length=70)
    phone = CharField(max_length=70)
    email = EmailField(unique=True)
    promo = ForeignKey('apps.PromoCode', CASCADE)
    event = ForeignKey('apps.Event', CASCADE)
    location = ForeignKey('apps.Location', CASCADE)
    courier = ForeignKey('apps.Courier', CASCADE)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Category(Model):
    name = CharField(max_length=255)
    slug = CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Basket(Model):
    event = ForeignKey('apps.Event', CASCADE)
    count = PositiveIntegerField(default=0)
    date = DateTimeField(auto_now_add=True)


class Like(Model):
    like = BooleanField(default=False)
    event = ForeignKey('apps.Event', CASCADE)


class Venue(Model):
    title = CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='venues',
                              default='venues/venues_default/default.jpg')

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
    country = ForeignKey('apps.Country', CASCADE)
    city = ForeignKey('apps.City', CASCADE)
