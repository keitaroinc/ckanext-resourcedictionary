# encoding: utf-8
import logging

from flask import Blueprint
from flask.views import MethodView

import ckan.lib.navl.dictization_functions as dict_fns
from ckan.logic import (
    tuplize_dict,
    parse_params,
)
import ckan.model as model
from ckan.plugins.toolkit import (
    ObjectNotFound, NotAuthorized, ValidationError,
    get_action, _, request,
    abort, render, c, h, g
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

        try:
            datastore_resource = get_action(u'datastore_search')(
                None, {
                    u'resource_id': resource_id,
                    u'limit': 1
                }
            )
            fields = [f for f in datastore_resource[u'fields'] if not f[u'id'].startswith(u'_')]
            total_records = datastore_resource[u'total']

        except ObjectNotFound:
            # Continue even if no datastore record is found for the
            # current resource
            fields = []
            total_records = 0

        return {
            u'pkg_dict': pkg_dict,
            u'resource': resource,
            u'fields': fields,
            u'total_records': total_records
        }

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

        context = dict(model=model,
                       user=g.user,
                       auth_user_obj=g.userobj)

        data = dict_fns.unflatten(tuplize_dict(parse_params(request.form)))
        form_fields = data.get(u'field', [])
        form_fields_info = data.get(u'info', [])

        fields = [{u'id': f[u'id'],
                   u'type': fi[u'type'],
                   u'info': fi if isinstance(fi, dict) else {}
                   } for f, fi in zip(form_fields, form_fields_info)]

        data_dict = {
            u'resource_id': resource_id,
            u'fields': fields
        }

        try:
            get_action(u'resource_dictionary_create')(context, data_dict)
        except ValidationError as e:
            extra_vars = self._prepare(id, resource_id)
            extra_vars[u'errors'] = e.error_dict
            extra_vars[u'error_summary'] = e.error_summary
            return render(u'dictionary/dictionary.html', extra_vars)

        h.flash_success(
            _(u'Data dictionary updated.')
        )

        return h.redirect_to(
            u'resource_dictionary.dictionary', id=id, resource_id=resource_id
        )


resource_dictionary.add_url_rule(
    u'/dataset/<id>/dictionary/<resource_id>',
    view_func=ResourceDictionaryView.as_view(str(u'dictionary'))
)
