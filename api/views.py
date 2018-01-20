from rest_framework import viewsets


class ServiceViewSet(viewsets.ViewSet):
    def create(self, request, service, version):
        raise NotImplementedError

    def retrieve(self, request, service, version):
        raise NotImplementedError

    def update(self, request, service, version, id):
        raise NotImplementedError

    def delete(self, request, service, version, id):
        raise NotImplementedError
