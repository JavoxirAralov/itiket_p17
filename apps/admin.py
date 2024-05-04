from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin

from apps.models import Location, City, Country, Event, Session, Order, Category, PromoCode, Promotion, Courier, User

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ['email']
    list_display = ("email", "first_name", "last_name", "is_staff")

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                'fields': (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(City)
class CityAdmin(TranslatableAdmin):
    pass


@admin.register(Country)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Location)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Event)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Session)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Order)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Category)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(PromoCode)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Promotion)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Courier)
class CertificatesAdmin(TranslatableAdmin):
    pass
