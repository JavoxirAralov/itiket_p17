from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, DateTimeField, CharField, EmailField, ForeignKey, CASCADE, IntegerField, \
    BooleanField, ManyToManyField, PositiveIntegerField, DecimalField
from django.db.models.fields import DateField
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

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
    phone = CharField(max_length=25, validators=[phone_regex], help_text='+9989***')
    birthday = DateTimeField(null=True, blank=True)

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


class Event(StartEndBaseModel, TranslatableModel):
    translations = TranslatedFields(
        description=CKEditor5Field(verbose_name=_('description'), blank=True, null=True, config_name='extends'),
        title=CharField(verbose_name=_('title'), max_length=70),
    )
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='event',
                              default='event/event_default/default.jpg')
    price = PositiveIntegerField(default=0)
    city = ForeignKey('City', CASCADE)
    category = ForeignKey('Category', CASCADE)
    slug = CharField(max_length=100)  # add slug  in  fixture

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class Promotion(TranslatableModel):
    translations = TranslatedFields(
        name=CharField(verbose_name=_('name'), max_length=255),

    )

    event = ManyToManyField('Event', blank=True, related_name='promotions')

    class Meta:
        verbose_name = _('Promotion')
        verbose_name_plural = _('Promotions')

    def __str__(self):
        return self.name


class Session(StartEndBaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=CharField(verbose_name=_('name'), max_length=100),

    )

    price = PositiveIntegerField(default=0)
    event = ForeignKey('Event', CASCADE)
    order = ForeignKey('Order', CASCADE)

    def __str__(self):
        return self.name


class Location(TranslatableModel):
    translations = TranslatedFields(
        description=CKEditor5Field(verbose_name=_('description'), blank=True, null=True, config_name='extends'),

    )
    index = IntegerField()
    city = ForeignKey('City', CASCADE)

    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
    is_deleted = BooleanField(default=False)
    order = ManyToManyField('Order', related_name='locations')

    def __str__(self):
        return str(self.index)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class Order(TranslatableModel):
    translations = TranslatedFields(
        firstname=CharField(verbose_name=_('firstname'), max_length=70),
        lastname=CharField(verbose_name=_('lastname'), max_length=70),

    )

    phone = CharField(max_length=25, validators=[phone_regex], help_text='+9989***')
    email = EmailField(unique=True)
    promo = ForeignKey('PromoCode', CASCADE)
    event = ForeignKey('Event', CASCADE)
    location = ForeignKey('Location', CASCADE, related_name='orders')
    courier = ForeignKey('Courier', CASCADE)

    def __str__(self):
        return self.firstname


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=CharField(verbose_name=_('name'), max_length=255),
    )
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


class Like(TranslatableModel):
    translations = TranslatedFields(
        name=ForeignKey('apps.User', verbose_name=_('name'), on_delete=models.CASCADE),
    )
    like = BooleanField(default=False)
    event = ForeignKey('Event', CASCADE)


class Venue(TranslatableModel):
    translations = TranslatedFields(
        title=CharField(verbose_name=_('title'), max_length=255),
        description=CKEditor5Field(verbose_name=_('description'), blank=True, null=True, config_name='extends'),
        address=CharField(verbose_name=_('address'), max_length=100, blank=True)
    )
    banner = ResizedImageField(size=[1000, 320], crop=['middle', 'center'], upload_to='venues_banner')
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='venues',
                              default='venues/venues_default/default.jpg')
    # location = ForeignKey('apps.Location', CASCADE)  # TODO: check
    slug = CharField(max_length=100)
    lang = CharField(max_length=10)
    lat = CharField(max_length=10)
    phone = CharField(max_length=25, validators=[phone_regex], help_text='+9989***')
    event = ForeignKey('apps.Event', CASCADE)  # it was chnaged the event and venu ForeginKey, change fixiture also

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Venue'
        verbose_name_plural = 'Venues'


class PromoCode(StartEndBaseModel, TranslatableModel):
    translations = TranslatedFields(
        promo=CharField(verbose_name=_('promo'), max_length=255)  # So Promo cod will be always in English laltar
    )

    def __str__(self):
        return self.promo


class Courier(TranslatableModel):
    translations = TranslatedFields(
        title=CharField(verbose_name=_('title'), max_length=70),
        description=CKEditor5Field(verbose_name=_('description'), blank=True, null=True, config_name='extends'),
        street=CharField(verbose_name=_('street'), max_length=100)
    )
    building = CharField(max_length=100)
    house_number = CharField(max_length=100)  # House number might be  -  74A
    index = CharField(max_length=100)  # Index number might  be  - AB12345
    country = ForeignKey('Country', CASCADE)
    city = ForeignKey('City', CASCADE)
