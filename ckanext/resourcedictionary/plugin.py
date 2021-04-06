import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.resourcedictionary.views.resource_dictionary \
    import resource_dictionary
from ckanext.resourcedictionary.logic.action.create \
    import resource_dictionary_create


class ResourcedictionaryPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets',
                             'resourcedictionary')

        # Add `dictionary_fields` resource extra field in config
        # in order to add resource dictionary fields in SOLR index
        config_[u'ckan.extra_resource_fields'] = u'dictionary_fields ' \
                                                 u'dictionary_labels ' \
                                                 u'dictionary_notes'

    # IBlueprint

    def get_blueprint(self):
        return [resource_dictionary]

    # IActions

    def get_actions(self):
        return {
            u'resource_dictionary_create':
                resource_dictionary_create
        }
