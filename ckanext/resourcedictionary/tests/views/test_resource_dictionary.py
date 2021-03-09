# encoding: utf-8
import six
import pytest

from ckan.tests import factories
import ckan.tests.helpers as h
from ckan.lib.helpers import url_for


@pytest.mark.usefixtures(u'clean_db', u'clean_index')
def test_create_new_resource_dictionary_successfully(app):

    user = factories.Sysadmin()
    env = {u'REMOTE_USER': six.ensure_str(user[u'name'])}

    context = {
        u'user': six.ensure_str(user[u'name']),
        u'ignore_auth': True
    }
    users = [{
                u'name': six.ensure_str(user[u'name']),
                u'capacity': 'admin'
            }]

    organization = h.call_action(u'organization_create',
                                 context,
                                 name='organization',
                                 users=users)

    package = h.call_action(u'package_create',
                            context,
                            name=u'package',
                            owner_org=organization[u'id'])

    resource = h.call_action(u'resource_create',
                             context,
                             name=u'resource',
                             package_id=package[u'id'])

    post_data = {
        u'field__1__id': u'Name',
        u'info__1__type': u'text',
        u'info__1__type_override': u'',
        u'info__1__label': u'Name Label',
        u'info__1__notes': u'Name Field Description',
        u'field__2__id': u'Lastname',
        u'info__2__type': u'text',
        u'info__2__type_override': u'',
        u'info__2__label': u'Lastname Label',
        u'info__2__notes': u'Lastname Field Description',
    }

    url = url_for(u'resource_dictionary.dictionary',
                  id=package[u'id'],
                  resource_id=resource[u'id'])

    res = app.post(
        url,
        data=post_data,
        extra_environ=env
    )
    assert 200 == res.status_code
    assert 'Data dictionary updated.' in res.body


@pytest.mark.usefixtures(u'clean_db', u'clean_index')
def test_create_resource_dictionary_invalid_entries_missing_id_error(app):

    user = factories.Sysadmin()
    env = {u'REMOTE_USER': six.ensure_str(user[u'name'])}

    context = {
        u'user': six.ensure_str(user[u'name']),
        u'ignore_auth': True
    }
    users = [{
                u'name': six.ensure_str(user[u'name']),
                u'capacity': 'admin'
            }]

    organization = h.call_action(u'organization_create',
                                 context,
                                 name='organization',
                                 users=users)

    package = h.call_action(u'package_create',
                            context,
                            name=u'package',
                            owner_org=organization[u'id'])

    resource = h.call_action(u'resource_create',
                             context,
                             name=u'resource',
                             package_id=package[u'id'])

    post_data = {
        u'field__1__id': u'',
        u'info__1__type': u'text',
        u'field__2__id': u'Lastname',
        u'info__2__type': u'text',
    }

    url = url_for(u'resource_dictionary.dictionary',
                  id=package[u'id'],
                  resource_id=resource[u'id'])

    res = app.post(
        url,
        data=post_data,
        extra_environ=env
    )
    assert 'The form contains invalid entries' in res.body


@pytest.mark.usefixtures(u'clean_db', u'clean_index')
def test_create_resource_dictionary_invalid_entries_missing_type_error(app):

    user = factories.Sysadmin()
    env = {u'REMOTE_USER': six.ensure_str(user[u'name'])}

    context = {
        u'user': six.ensure_str(user[u'name']),
        u'ignore_auth': True
    }
    users = [{
                u'name': six.ensure_str(user[u'name']),
                u'capacity': 'admin'
            }]

    organization = h.call_action(u'organization_create',
                                 context,
                                 name='organization',
                                 users=users)

    package = h.call_action(u'package_create',
                            context,
                            name=u'package',
                            owner_org=organization[u'id'])

    resource = h.call_action(u'resource_create',
                             context,
                             name=u'resource',
                             package_id=package[u'id'])

    post_data = {
        u'field__1__id': u'Name',
        u'info__1__type': u'',
        u'field__2__id': u'Lastname',
        u'info__2__type': u'text',
    }

    url = url_for(u'resource_dictionary.dictionary',
                  id=package[u'id'],
                  resource_id=resource[u'id'])

    res = app.post(
        url,
        data=post_data,
        extra_environ=env
    )
    assert 'The form contains invalid entries' in res.body


@pytest.mark.usefixtures(u'clean_db', u'clean_index')
def test_create_new_resource_dictionary_resource_not_found_error(app):

    user = factories.Sysadmin()
    env = {u'REMOTE_USER': six.ensure_str(user[u'name'])}

    post_data = {
        u'field__1__id': u'Name',
        u'info__1__type': u'text',
        u'info__1__type_override': u'',
        u'info__1__label': u'Name Label',
        u'info__1__notes': u'Name Field Description',
        u'field__2__id': u'Lastname',
        u'info__2__type': u'text',
        u'info__2__type_override': u'',
        u'info__2__label': u'Lastname Label',
        u'info__2__notes': u'Lastname Field Description',
    }

    url = url_for(u'resource_dictionary.dictionary',
                  id=u'package-not-found',
                  resource_id=u'7a50a2c8-7af5-46bc-b87d-272978c58a78')

    res = app.post(
        url,
        data=post_data,
        extra_environ=env
    )
    assert 404 == res.status_code
    assert 'Resource not found' in res.body
