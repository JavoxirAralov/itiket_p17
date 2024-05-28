from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from django.contrib.admin.sites import site

import apps
from apps.models import Location, City, Country, Event, Session, Order, Category, PromoCode, Promotion, Courier, User, \
    Venue
from apps.serializers import VenueModelSerializer

admin.site.unregister(Group)

# class BaseAdmin(admin.ModelAdmin):
#     admin_priority = 20
#
#     def get_app_list(self, request):
#         app_dict = self._build_app_dict(request)
#         for app_name in app_dict.keys():
#             app = app_dict[app_name]
#             model_priority = {
#                 model['object_name']: getattr(
#                     site._registry[apps.get_model(app_name, model['object_name'])],
#                     'admin_priority',
#                     20
#                 )
#                 for model in app['models']
#             }
#             app['models'].sort(key=lambda x: model_priority[x['object_name']])
#             yield app
#
#     admin.AdminSite.get_app_list = get_app_list

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


# @admin.register(City)
# class CityAdmin(ModelAdmin):
#     pass


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
class CertificatesAdmin(ModelAdmin):
    pass


@admin.register(Category)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(PromoCode)
class CertificatesAdmin(ModelAdmin):
    pass


@admin.register(Promotion)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Courier)
class CertificatesAdmin(TranslatableAdmin):
    pass


@admin.register(Venue)
class VenueModelAdmin(TranslatableAdmin):
    pass
