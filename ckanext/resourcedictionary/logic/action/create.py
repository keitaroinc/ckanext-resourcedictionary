# encoding: utf-8
import logging

import ckan.logic as logic
from ckan.plugins.toolkit import (
    ObjectNotFound, NotAuthorized, get_action, _, request,
    abort, render, c, h
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


def _check_actions(fields, new_fields, total_records):
    u'''Helper function that checks which actions
    should be executed during the POST request.

    :param fields: `list`, list of existing fields.
    :param new_fields: `list`, list of new fields.
    :param total_records: `int`, number of records.

    :return: `tuple`, (`boolean`, `boolean`)
    '''
    perform_delete = False
    perform_create = False

    # If the resource does not have datastore records
    # it is safe to delete the datastore table for the selected resource
    # and recreate it with the new options
    if fields and not total_records:
        perform_delete = True

    # Create initial datastore table
    if not fields and new_fields:
        perform_create = True

    # Compare fields with new_field
    if fields and new_fields:
        if total_records:
            # If datastore resource has records
            # only adding new fields or
            # updating existing fields info is allowed
            if len(fields) <= len(new_fields):
                perform_create = True
                for i in range(len(fields)):
                    if fields[i][u'id'] != new_fields[i][u'id']:
                        perform_create = False
        else:
            # If datastore resource has no records
            # it will be marked for deletion in the deletion check above
            # and here we are allowing to be recreated with the new options
            perform_create = True

    return perform_delete, perform_create


def resource_dictionary_create(context, data_dict):
    '''Creates or updates resource data dictionary.

    '''
    _check_access('datastore_create', context, data_dict)

    resource_id = data_dict[u'resource_id']
    new_fields = data_dict[u'fields']
    resource_datastore_info = _get_resource_datastore_info(resource_id)
    fields = resource_datastore_info.get(u'fields', [])
    total_records = resource_datastore_info.get(u'total_records', 0)

    perform_delete, perform_create = _check_actions(
        fields,
        new_fields,
        total_records,
    )
    res = {u'message': _(u'Data dictionary contains records '
                         u'therefore requested changes can not be applied.')}
    # If the resource does not have any records in the datastore
    # then it is safe to delete the table and
    # create it again with the new settings in the step below
    if perform_delete:
        res = get_action(u'datastore_delete')(
            None, {
                u'resource_id': resource_id,
                u'force': True
            }
        )
        log.info(_(u'Data dictionary removed.'))

    if perform_create:
        res = get_action(u'datastore_create')(
            None, {
                u'resource_id': resource_id,
                u'force': True,
                u'fields': new_fields
            }
        )
        log.info(_(u'Data dictionary saved.'))

    return res