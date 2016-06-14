import pytest
from common.session import session
from time import sleep
from navigation.navigation import NavigationTree

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    def closeSession():
        print ("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)
    return web_session

def sleep_test_deployments (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_deployment_view()

def sleep_test_providers (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_providers_view()

def sleep_test_servers (web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_servers_view()


def sleep_test_topology(web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_topology_view()


def sleep_test_datasources(web_session):
    nav = NavigationTree(web_session)
    nav.navigate_to_middleware_datasources_view()


def test_fast_navigation(web_session):
    nav = NavigationTree(web_session)

    nav.jump_to_middleware_datasources_view()
    nav.jump_to_middleware_datasources_view(force_navigation=False)
    nav.jump_to_middleware_datasources_view(force_navigation=True)

    nav.jump_to_middleware_deployment_view()
    nav.jump_to_middleware_deployment_view(force_navigation=True)
    nav.jump_to_middleware_deployment_view(force_navigation=False)

    nav.jump_to_middleware_providers_view()
    nav.jump_to_middleware_servers_view()
    nav.jump_to_topology_view()
