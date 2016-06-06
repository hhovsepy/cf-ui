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


def _test_deployments (web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_deployment_view()

def _test_providers (web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_providers_view()

def _test_servers (web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_servers_view()


def _test_topology(web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_topology_view()


def _test_datasources(web_session):
    driver = web_session.web_driver
    nav = NavigationTree(driver)
    nav.navigate_to_middleware_datasources_view()


def test_all_navigations(web_session):
    nav = NavigationTree(web_session.web_driver)

    nav.navigate_to_middleware_deployment_view()
    nav.navigate_to_middleware_servers_view()
    nav.navigate_to_middleware_datasources_view()
    nav.navigate_to_topology_view()

def test_all_navigations_2(web_session):
    NavigationTree(web_session.web_driver).navigate_to_middleware_deployment_view()
    NavigationTree(web_session.web_driver).navigate_to_middleware_servers_view()
    NavigationTree(web_session.web_driver).navigate_to_middleware_datasources_view()
    NavigationTree(web_session.web_driver).navigate_to_topology_view()


def test_tree(web_session):
    print "Start Test suite"
    driver = web_session.web_driver

    NavigationTree(driver).navigate_to_middleware_deployment_view()
    NavigationTree(driver).navigate_to_middleware_providers_view()
    NavigationTree(driver).navigate_to_middleware_servers_view()
    NavigationTree(driver).navigate_to_middleware_datasources_view()
    NavigationTree(driver).navigate_to_topology_view()