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
