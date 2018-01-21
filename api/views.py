from rest_framework import status, viewsets
from rest_framework.response import Response

from api import signals
from api.models import Service
from api.serializers import ServiceSerializer


class ServiceViewSet(viewsets.ViewSet):
    def create(self, request, name, version):
        """Create a service ensuring no conflicts.

        The signal "service_created" is emitted upon successful creation.
        """
        qs = Service.objects.filter(
            name=name, version=version, url=request.data.get('url'))
        if not qs.exists():
            url = request.data.get('url')
            serializer = ServiceSerializer(
                data={'name': name, 'version': version, 'url': url})
            if serializer.is_valid():
                service = serializer.save()

                signals.service_created.send(
                    sender=Service, id=service.id, name=service.name,
                    version=service.version, url=service.url)

                return Response(
                    {'id': service.id}, status=status.HTTP_201_CREATED)

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'id': qs.first().id}, status=status.HTTP_409_CONFLICT)

    def list(self, request, name, version=None):
        """List services given the name and optionally the version.
        """
        services = Service.objects.filter(name=name)
        if version is not None:
            services = services.filter(version=version)

        serializer = ServiceSerializer(services, many=True)

        return Response(serializer.data)

    def update(self, request, name, version, pk):
        """Update the service URL.

        Upon successful update, emits the "service_updated" signal.
        """
        try:
            service = Service.objects.get(id=pk)

            url = request.data.get('url')
            serializer = ServiceSerializer(instance=service,
                data={'name': name, 'version': version, 'url': url})
            if serializer.is_valid():
                service = serializer.save()

                signals.service_updated.send(
                    sender=Service, id=service.id, name=service.name,
                    version=service.version, url=service.url)

                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Service.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, name, version, pk):
        """Deletes an existing service.

        If the services does exist and was deleted successfully, emits
        the "service_deleted" signal.
        """
        try:
            service = Service.objects.get(id=pk)

            signals.service_deleted.send(
                sender=Service, id=service.id, name=service.name,
                version=service.version, url=service.url)

            service.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Service.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
