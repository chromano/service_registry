from unittest import mock

import pytest

from api.models import Service
from api.views import ServiceViewSet

@pytest.mark.django_db
def test_create_service():
    view = ServiceViewSet()

    request = mock.Mock()
    request.data = {'url': 'http://192.168.1.1'}

    with mock.patch('api.signals.service_created') as p_signal:
        response = view.create(request, 'serviceA', '0.0.1')
        assert response.status_code == 201

        p_signal.send.assert_called_with(
            sender=Service, id=mock.ANY, name='serviceA', version='0.0.1',
            url='http://192.168.1.1')

        assert Service.objects.all().count() == 1


@pytest.mark.django_db
def test_create_duplicated_service():
    view = ServiceViewSet()

    service = Service(name='serviceA', version='0.0.1',
                      url='http://192.168.1.1')
    service.save()

    request = mock.Mock()
    request.data = {'url': service.url}

    with mock.patch('api.signals.service_created') as p_signal:
        response = view.create(request, 'serviceA', '0.0.1')
        assert response.status_code == 409

        p_signal.send.assert_not_called()

    assert Service.objects.all().count() == 1
    assert response.data['id'] == service.id


@pytest.mark.django_db
def test_create_service_missing_data():
    view = ServiceViewSet()

    request = mock.Mock()
    request.data = {}

    with mock.patch('api.signals.service_created') as p_signal:
        response = view.create(request, 'serviceA', '0.0.1')
        assert response.status_code == 400

        p_signal.send.assert_not_called()

    assert Service.objects.all().count() == 0


@pytest.mark.django_db
def test_list_service_by_name_and_version():
    view = ServiceViewSet()

    request = mock.Mock()

    response = view.list(request, 'serviceA', '0.0.1')
    assert response.data == []

    service = Service(name='serviceA', version='0.0.1',
                      url='http://192.168.1.1')
    service.save()

    response = view.list(request, 'serviceA', '0.0.1')
    assert response.data == [
        {
            'id': service.id,
            'name': service.name,
            'version': service.version,
            'url': service.url
        },
    ]


@pytest.mark.django_db
def test_list_service_by_name():
    view = ServiceViewSet()

    request = mock.Mock()

    response = view.list(request, 'serviceA')
    assert response.status_code == 200
    assert len(response.data) == 0

    Service(name='serviceA', version='0.0.1', url='http://192.168.1.1').save()
    Service(name='serviceA', version='0.0.2', url='http://192.168.1.1').save()

    response = view.list(request, 'serviceA')
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_service():
    view = ServiceViewSet()

    service = Service(name='serviceA', version='0.0.1',
                      url='http://192.168.1.1')
    service.save()

    request = mock.Mock()
    request.data = {'url': 'http://192.168.1.2'}

    with mock.patch('api.signals.service_updated') as p_signal:
        response = view.update(request, 'serviceA', '0.0.1', service.id)
        assert response.status_code == 204

        p_signal.send.assert_called_with(
            sender=Service, id=service.id, name='serviceA', version='0.0.1',
            url='http://192.168.1.2')


@pytest.mark.django_db
def test_update_service_not_found():
    view = ServiceViewSet()

    request = mock.Mock()
    request.data = {'url': 'http://192.168.1.2'}

    with mock.patch('api.signals.service_updated') as p_signal:
        response = view.update(request, 'serviceA', '0.0.1', 1)
        assert response.status_code == 404

        p_signal.send.assert_not_called()


@pytest.mark.django_db
def test_update_service_missing_data():
    view = ServiceViewSet()

    service = Service(name='serviceA', version='0.0.1',
                      url='http://192.168.1.1')
    service.save()

    request = mock.Mock()
    request.data = {}

    with mock.patch('api.signals.service_updated') as p_signal:
        response = view.update(request, 'serviceA', '0.0.1', service.id)
        assert response.status_code == 400

        p_signal.send.assert_not_called()


@pytest.mark.django_db
def test_delete_service():
    view = ServiceViewSet()

    service = Service(name='serviceA', version='0.0.1',
                      url='http://192.168.1.1')
    service.save()

    request = mock.Mock()

    with mock.patch('api.signals.service_deleted') as p_signal:
        response = view.delete(request, 'serviceA', '0.0.1', service.id)
        assert response.status_code == 204

        p_signal.send.assert_called_with(
            sender=Service, id=service.id, name='serviceA', version='0.0.1',
            url='http://192.168.1.1')


@pytest.mark.django_db
def test_delete_service_not_found():
    view = ServiceViewSet()

    request = mock.Mock()

    with mock.patch('api.signals.service_deleted') as p_signal:
        response = view.delete(request, 'serviceA', '0.0.1', 1)
        assert response.status_code == 404

        p_signal.send.assert_not_called()
