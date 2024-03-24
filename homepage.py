from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pytest

class InsiderHomePage:
    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get("https://useinsider.com/")

    def is_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return True
        except TimeoutException:
            return False

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        web_driver = webdriver.Chrome()
    elif request.param == "firefox":
        web_driver = webdriver.Firefox()
    else:
        raise ValueError("Unsupported browser type: {}".format(request.param))

    web_driver.implicitly_wait(10)
    request.cls.driver = web_driver
    request.cls.homepage = InsiderHomePage(web_driver)
    yield
    # Kapanma kodu her durumda çalışacak şekilde konumlandırıldı
    web_driver.quit()

@pytest.mark.usefixtures("driver")
class TestInsiderHomepageAccessibility:
    def test_homepage_accessibility(self):
        self.homepage.load()
        assert self.homepage.is_loaded(), "Insider Ana Sayfası yüklenemedi."

if __name__ == "__main__":
    pytest.main()
