# encoding: utf-8
import pytest

from ckan.tests import factories
from ckan.plugins import toolkit


@pytest.mark.ckan_config("ckan.plugins", "datastore")
@pytest.mark.usefixtures(u'clean_db', u'clean_index',
                         u'clean_datastore', u'with_plugins')
def test_create(self, app):
    pass
