# encoding: utf-8
import logging

from flask import Blueprint
from flask.views import MethodView

import ckan.lib.navl.dictization_functions as dict_fns
from ckan.logic import (
    tuplize_dict,
    parse_params,
)
from ckan.plugins.toolkit import (
    ObjectNotFound, NotAuthorized, get_action, _, request,
    abort, render, c, h
)

log = logging.getLogger(__name__)
resource_dictionary = Blueprint(u'resource_dictionary', __name__)


class ResourceDictionaryView(MethodView):

    def _prepare(self, id, resource_id):
        u'''Helper function that gets the available
        info for the requested resource.

        :param id: `string`, dataset id.
        :param resource_id: `string`, resource id.

        :return: `dict`, dictionary with resource info
        '''
        try:
            # resource_edit_base template uses these
            pkg_dict = get_action(u'package_show')(None, {u'id': id})
            resource = get_action(u'resource_show')(None, {u'id': resource_id})
        except (ObjectNotFound, NotAuthorized):
            abort(404, _(u'Resource not found'))

        fields = []
        records = 0
        try:
            datastore_resource = get_action(u'datastore_search')(
                None, {
                    u'resource_id': resource_id,
                    u'limit': 1
                }
            )
            fields = [f for f in datastore_resource[u'fields'] if not f[u'id'].startswith(u'_')]
            records = datastore_resource[u'total']

        except (ObjectNotFound, NotAuthorized):
            # Continue even if no datastore record is found for the
            # current resource
            log.info('No datastore record found for resource with id {}.'.format(resource_id))
            pass

        return {
            u'pkg_dict': pkg_dict,
            u'resource': resource,
            u'fields': fields,
            u'records': records
        }

    def _check_actions(self, fields, records, new_fields):
        u'''Helper function that checks which actions
        should be executed during the POST request.

        :param fields: `list`, list of existing fields.
        :param records: `int`, number of records.
        :param new_fields: `list`, list of new fields.

        :return: `tuple`, (`boolean`, `boolean`)
        '''
        perform_delete = False
        perform_create = False

        # If the resource does not have datastore records
        # it is safe to delete the datastore table for the selected resource
        # and recreate it with the new options
        if fields and not records:
            perform_delete = True

        # Create initial datastore table
        if not fields and new_fields:
            perform_create = True

        # Compare fields with new_field
        if fields and new_fields:
            if records:
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

    def get(self, id, resource_id):
        u'''Data dictionary view: show field labels and descriptions'''

        data_dict = self._prepare(id, resource_id)

        # global variables for backward compatibility
        c.pkg_dict = data_dict[u'pkg_dict']
        c.resource = data_dict[u'resource']

        return render(u'dictionary/dictionary.html', data_dict)

    def post(self, id, resource_id):
        u'''Data dictionary view: create and edit fields,
        field labels and descriptions'''
        data_dict = self._prepare(id, resource_id)
        fields = data_dict[u'fields']
        records = data_dict[u'records']
        data = dict_fns.unflatten(tuplize_dict(parse_params(request.form)))
        new_fields = data.get(u'field')
        new_info = data.get(u'info')

        perform_delete, perform_create = self._check_actions(
            fields,
            records,
            new_fields
        )

        # If the resource does not have any records in the datastore
        # then it is safe to delete the table and
        # create it again with the new settings in the step below
        if perform_delete:
            get_action(u'datastore_delete')(
                None, {
                    u'resource_id': resource_id,
                    u'force': True
                }
            )
            h.flash_success(
                _(u'Data dictionary removed.')
            )

        if perform_create:
            get_action(u'datastore_create')(
                None, {
                    u'resource_id': resource_id,
                    u'force': True,
                    u'fields': [{
                        u'id': f[u'id'],
                        u'type': fi[u'type'],
                        u'info': fi if isinstance(fi, dict) else {}
                    } for f, fi in zip(new_fields, new_info)]
                }
            )
            h.flash_success(
                _(u'Data dictionary saved.')
            )

        if not perform_delete and not perform_create:
            h.flash_notice(_(
                u'Sorry, performed action is not allowed. '
                u'Editing dictionary field names and types for resources '
                u'that contain actual data in the datastore is not allowed. '
                u'Only info columns are editable in this scenario'
                u' (`Type Override`, `Label` and `Description`)'
            ))

        return h.redirect_to(
            u'resource_dictionary.dictionary', id=id, resource_id=resource_id
        )


resource_dictionary.add_url_rule(
    u'/dataset/<id>/dictionary/<resource_id>',
    view_func=ResourceDictionaryView.as_view(str(u'dictionary'))
)