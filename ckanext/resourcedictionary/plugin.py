import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.resourcedictionary.views.resource_dictionary \
    import resource_dictionary


class ResourcedictionaryPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'resourcedictionary')

    # IBlueprint

    def get_blueprint(self):
        return [resource_dictionary]