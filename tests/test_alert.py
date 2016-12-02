import pytest
from common.session import session
from views.eap_alerts import eap_alerts

@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    return web_session


def test_add_mw_alert(web_session):
    web_session.logger.info("Begin Add alert test")
    assert eap_alerts(web_session).add_alert()

def test_copy_mw_alert(web_session):
    web_session.logger.info("Begin Copy alert test")
    assert eap_alerts(web_session).copy_alert()

def test_edit_mw_alert(web_session):
    web_session.logger.info("Begin Edit alert test")
    assert eap_alerts(web_session).edit_alert()

def test_delete_mw_alert(web_session):
    web_session.logger.info("Begin delete alert test")
    assert eap_alerts(web_session).delete_alert()

