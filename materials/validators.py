from rest_framework.serializers import ValidationError

part_url = 'youtube.com'

def url_validator(url):
    if part_url not in url:
        raise ValidationError('Возможна ссылка только на youtube.com')
