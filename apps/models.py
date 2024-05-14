from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, DateTimeField, CharField, EmailField, ForeignKey, CASCADE, IntegerField, \
    BooleanField, ManyToManyField, PositiveIntegerField, DecimalField, SlugField
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

from apps.managers import CustomUserManager
from apps.utils import phone_regex


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
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='event',
                              default='event/event_default/default.jpg')
    email = models.EmailField(unique=True)
    phone = CharField(max_length=25, validators=[phone_regex], help_text='+9989***')
    birthday = DateTimeField(null=True, blank=True)
    username = None
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Country(Model):
    name = CharField(max_length=150, unique=True)
    code = CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class City(Model):
    name = CharField(max_length=255)
    country = ForeignKey('Country', CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Event(StartEndBaseModel, TranslatableModel):
    translations = TranslatedFields(
        description=CKEditor5Field(verbose_name=_('description'), blank=True, null=True, config_name='extends'),
        title=CharField(verbose_name=_('title'), max_length=70)
    )
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='event',
                              default='event/event_default/default.jpg')
    price = PositiveIntegerField(default=0)
    city = ForeignKey('City', CASCADE)
    category = ForeignKey('Category', CASCADE)
    slug = SlugField(max_length=100, editable=False)  # add slug  in  fixture
    venue = ForeignKey('apps.Venue', CASCADE)

    def __dir__(self):
        return self.title

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class Promotion(Model):
    name = CharField(max_length=255)
    event = ManyToManyField('Event', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Promotion')
        verbose_name_plural = _('Promotions')


class Session(StartEndBaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=CharField(verbose_name=_('name'), max_length=100),

    )

    price = PositiveIntegerField(default=0)
    event = ForeignKey('Event', CASCADE)
    order = ForeignKey('apps.Order', CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')


class Location(TranslatableModel):
    translations = TranslatedFields(
        description=CKEditor5Field(verbose_name=_('description'), blank=True, null=True, config_name='extends')
    )
    index = IntegerField()
    city = ForeignKey('City', CASCADE)

    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
    is_deleted = BooleanField(default=False)
    order = ManyToManyField('Order', related_name='locations', blank=True)

    def __str__(self):
        return str(self.index)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')


class Order(Model):
    first_name = CharField(max_length=70)
    last_name = CharField(max_length=70)
    phone = CharField(max_length=25, validators=[phone_regex], help_text='+9989***')
    email = EmailField(unique=True)
    promo = ForeignKey('PromoCode', CASCADE)
    event = ForeignKey('Event', CASCADE)
    location = ForeignKey('Location', CASCADE, related_name='orders')
    courier = ForeignKey('Courier', CASCADE)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=CharField(verbose_name=_('name'), max_length=255),
    )
    slug = SlugField(max_length=100, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Basket(Model):
    event = ForeignKey('Event', CASCADE)
    count = PositiveIntegerField(default=0)
    date = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')


class Favorite(Model):
    favorite = CharField(max_length=255, blank=True)
    user = ForeignKey('User', CASCADE)
    event = ForeignKey('Event', CASCADE)

    def __str__(self):
        return self.favorite

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')


class Venue(TranslatableModel):
    translations = TranslatedFields(
        title=CharField(verbose_name=_('title'), max_length=255),
        description=CKEditor5Field(verbose_name=_('description'), blank=True, null=True, config_name='extends'),
        address=CharField(verbose_name=_('address'), max_length=100, blank=True)
    )
    banner = ResizedImageField(size=[1000, 320], crop=['middle', 'center'], upload_to='venues_banner',
                               default='venues/venues_default/default.jpg')
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='venues',
                              default='venues/venues_default/default.jpg')
    slug = SlugField(max_length=100, editable=False)

    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
    phone = CharField(max_length=25, validators=[phone_regex], help_text='+9989***')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Venue')
        verbose_name_plural = _('Venues')


class PromoCode(StartEndBaseModel):
    name = CharField(verbose_name=_('promo'), max_length=255)

    class Meta:
        verbose_name = _('PromoCode')
        verbose_name_plural = _('PromoCodes')


class Courier(Model):
    title = CharField(max_length=70)
    description = CKEditor5Field(blank=True, null=True, config_name='extends')
    street = CharField(verbose_name=_('street'), max_length=100)

    building = CharField(max_length=100)
    house_number = CharField(max_length=100)  # House number might be  -  74A
    index = CharField(max_length=100)  # Index number might  be  - AB12345
    country = ForeignKey('Country', CASCADE)
    city = ForeignKey('City', CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Courier')
        verbose_name_plural = _('Couriers')
