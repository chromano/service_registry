import json

from behave import *

from api.models import Service


@given('there is an empty ServiceRegistry')
def clear_services(context):
    # the database is already reseted between tests, no need to do anything
    pass


@when('sample services are given')
def create_sample_services(context):
    Service(name='test', version='0.0.1', url='http://192.168.1.50').save()
    Service(name='test', version='0.0.1', url='http://192.168.1.51').save()
    Service(name='test', version='0.0.2', url='http://192.168.1.52').save()
    Service(name='test', version='0.0.2', url='http://192.168.1.53').save()
    Service(name='test2', version='0.0.2', url='http://192.168.1.54').save()
    Service(name='test2', version='0.0.2', url='http://192.168.1.55').save()


@when('I add a service "{service}" with version "{version}" and url "{url}"')
def add_service(context, service, version, url):
    path = f'/api/v1/services/{service}/{version}/'
    context.response = context.test.client.post(path, {'url': url})


@then('I should be notified with a change "{change}"')
def confirm_response(context, change):
    if change == 'created':
        context.test.assertEqual(context.response.status_code, 201)
    elif change in ('changed', 'removed'):
        context.test.assertEqual(context.response.status_code, 204)
    else:
        context.test.assertEqual(context.response.status_text, change)


@when('I search for a service "{service}" with version "{version}"')
def find_services(context, service, version):
    path = f'/api/v1/services/{service}/{version}/'
    context.response = context.test.client.get(path)


@when('I search for a service "{service}" without version')
def find_services_without_version(context, service):
    path = f'/api/v1/services/{service}/'
    context.response = context.test.client.get(path)


@then('I should find count "{count}" services')
@then('I should find count "{count}" instances of service')
def count_services(context, count):
    context.test.assertEqual(context.response.status_code, 200)
    context.test.assertEqual(len(context.response.data), int(count))


@then('the service "{service}" should have the correct type')
def ensure_services_name(context, service):
    for entry in context.response.data:
        context.test.assertEqual(entry['name'], service)


@then('the service "{service}" should have the correct version "{version}"')
def ensure_services_version(context, service, version):
    for entry in context.response.data:
        context.test.assertEqual(entry['version'], version)


@when('I update a service')
def update_service(context):
    path = f'/api/v1/services/foo/1.2.3/'
    url = 'http://127.0.0.1/'
    response = context.test.client.post(path, {'url': url})

    context.test.assertEqual(response.status_code, 201)
    context.test.assertEqual('id' in response.data, True)

    path += f'{response.data["id"]}/'
    url = 'http://192.168.1.1'
    context.response = context.test.client.put(path, json.dumps({
        'name': 'foo',
        'version': '1.2.3',
        'url': url
    }), content_type='application/json')


@when('I remove a service')
def remove_service(context):
    path = f'/api/v1/services/foo/1.2.3/'
    url = 'http://127.0.0.1/'
    response = context.test.client.post(path, {'url': url})

    context.test.assertEqual(response.status_code, 201)
    context.test.assertEqual('id' in response.data, True)
    id = response.data['id']
    context.service_id =  id
    context.response = context.test.client.delete(path + str(id) + '/')


@then('the service should be removed')
def check_service_removed(context):
    response = context.test.client.put(
        context.response.request['PATH_INFO'], {})
    context.test.assertEqual(response.status_code, 404)
