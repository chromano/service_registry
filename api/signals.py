from django.dispatch import Signal

service_created = Signal(providing_args=['id', 'name', 'version', 'url'])
service_updated = Signal(providing_args=['id', 'name', 'version', 'url'])
service_deleted = Signal(providing_args=['id', 'name', 'version', 'url'])
