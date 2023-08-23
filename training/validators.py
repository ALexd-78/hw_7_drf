import re
from rest_framework.exceptions import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = 'youtube.com'
        tmp_val = dict(value).get(self.field)
        if reg not in tmp_val:
            raise ValidationError('Field "link_to_video" is not ok')