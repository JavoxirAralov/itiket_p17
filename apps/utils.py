from django.core.validators import RegexValidator


def phone_number_validator(value):
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}$',
        message="Phone number must be entered in the format: '+999999999'."
                "Up to 15 digits allowed."
    )
    return phone_regex
