from pyramid.configuration import Configurator
from som.models import get_root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=get_root, settings=settings)
    config.begin()
    config.add_view('som.views.my_view',
                    context='som.models.MyModel',
                    renderer='som:templates/mytemplate.pt')
    config.add_static_view('static', 'som:static')
    config.end()
    return config.make_wsgi_app()

