import pytest
from common.session import session
from views.servers import servers
from views.providers import providers


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session()

    # presume that MIQ has no Middleware Hawkular provider
    provider = providers(web_session)
    provider.add_provider_if_not_present()

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()
    request.addfinalizer(closeSession)

    return web_session

def test_servers_view(web_session):
    web_session.logger.info("Begin Server View")
    servs = servers(web_session)
    assert (servs.validate_servers_list())

def test_server_details(web_session):
    web_session.logger.info("Begin Server Details")
    ui_pairs = servers(web_session).validate_server_details()
    assert ui_pairs.get("Product") == web_session.PROVIDER
    assert ui_pairs.get("Middleware Provider") == web_session.HAWKULAR_PROVIDER_NAME

