# این فایل رو داخل اپ خودت بذار، مثلا: yourapp/templatetags/persian_filters.py
# مطمئن شو یه فایل __init__.py خالی هم داخل پوشه‌ی templatetags هست.

from django import template

register = template.Library()

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ENGLISH_DIGITS = "0123456789"

_TRANSLATION_TABLE = str.maketrans(ENGLISH_DIGITS, PERSIAN_DIGITS)


@register.filter(name="to_persian_digits")
def to_persian_digits(value):

    if value is None:
        return ""
    return str(value).translate(_TRANSLATION_TABLE)