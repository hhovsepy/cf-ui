import pytest
from common.session import session
from common.download_report import download_report
from navigation.navigation import NavigationTree
#import os.path


@pytest.fixture (scope='session')
def web_session(request):
    web_session = session(add_provider=True)

    def closeSession():
        web_session.logger.info("Close browser session")
        web_session.close_web_driver()

    request.addfinalizer(closeSession)

    return web_session

def test_cfui_providers_download_txt(web_session):
    web_session.logger.info("Begin download report as text test")
    assert download_report(web_session,"ems_middleware").text_format()
    #assert os.path.exists("/home/pyadav/Downloads/Middleware Providers_2016_08_04.txt")

    web_session.logger.info("Begin download report as cvv test")
    assert download_report(web_session,"ems_middleware").csv_format()
    #assert os.path.exists("/home/pyadav/Downloads/Middleware Providers_2016_08_04.csv")