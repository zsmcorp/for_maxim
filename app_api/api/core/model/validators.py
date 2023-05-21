import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    message = _(
        'File size %(size)s is not allowed. '
        'Allowed size are: %(allowed_size)s.'
    )
    code = 'invalid_size'

    def __init__(self, max_size, message=None, code=None):
        self.max_size = max_size
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        size = value.size
        if size > self.max_size:
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    'size': size,
                    'allowed_size': self.max_size
                }
            )

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.max_size == other.max_size
                and self.message == other.message
                and self.code == other.code
        )


@deconstructible
class AccountIdentityPhoneValidator(validators.RegexValidator):
    regex = r'^[0-9]{1,3}?([0-9]{2,3})([0-9]{7})$'
    # +
    # X* country code
    #   7 - RF
    # X* operator or state code
    #   9XX - RF
    # XXX XX XX - abonent number
    # any characters except digits must be removed
    message = _(
        'Enter a valid phone number. This value may contain only digits.'
    )
    flags = re.ASCII
