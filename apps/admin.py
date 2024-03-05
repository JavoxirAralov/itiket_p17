from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from apps.models import Location, City, Country, Event, Session, Order, Category, PromoCode, Promotion, Courier, User
from django.utils.safestring import mark_safe
admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ( "username", "email", "first_name", "last_name", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
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



@admin.register(Location)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(Promotion)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(City)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(Country)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(Event)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(Session)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(Order)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(Category)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(PromoCode)
class ProductModelAdmin(ModelAdmin):
    pass


@admin.register(Courier)
class ProductModelAdmin(ModelAdmin):
    pass
