# encoding: utf-8
import logging

import ckan.logic as logic
from ckan.plugins.toolkit import (
    ObjectNotFound, NotAuthorized, get_action, _
)

log = logging.getLogger(__name__)

_check_access = logic.check_access
_get_action = logic.get_action
ValidationError = logic.ValidationError


def _get_resource_datastore_info(resource_id):
    u'''Helper function that gets the available
    info for the requested resource.

    :param resource_id: `string`, resource id.

    :return: `dict`, dictionary with resource info
    '''

    try:
        rec = get_action(u'datastore_search')(
            None, {
                u'resource_id': resource_id,
                u'limit': 1
            }
        )

        return {
            u'fields': [f for f in rec[u'fields']
                        if not f[u'id'].startswith(u'_')],
            u'total_records': rec[u'total']
        }

    except (ObjectNotFound, NotAuthorized):
        # Continue even if no datastore record is found for the
        # current resource
        return {}


def resource_dictionary_create(context, data_dict):
    '''Creates or updates resource data dictionary.
    '''
    _check_access('datastore_create', context, data_dict)

    resource_id = data_dict[u'resource_id']
    new_fields = data_dict[u'fields']
    resource_datastore_info = _get_resource_datastore_info(resource_id)
    fields = resource_datastore_info.get(u'fields', [])
    total_records = resource_datastore_info.get(u'total_records', 0)

    res = {u'message': _(u'Data dictionary updated.')}

    for f in new_fields:
        if not f[u'type']:
            raise ValidationError({u'fields': [{u'type': _(u'Missing value')}]})
        if not f[u'id']:
            raise ValidationError({u'fields': [{u'id': _(u'Missing value')}]})

    # If the resource does not have any records in the datastore
    # then it is safe to delete the table and
    # create it again with the new settings in the step below
    if fields and not total_records:
        res = get_action(u'datastore_delete')(
            None, {
                u'resource_id': resource_id,
                u'force': True
            }
        )
        log.info(_(u'Data dictionary removed.'))
    if new_fields:
        res = get_action(u'datastore_create')(
            None, {
                u'resource_id': resource_id,
                u'force': True,
                u'fields': new_fields
            }
        )
    log.info(_(u'Data dictionary saved.'))

    return res
