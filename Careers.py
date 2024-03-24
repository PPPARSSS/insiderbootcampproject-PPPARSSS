import configparser
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InsiderCareerPage:
    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get("https://useinsider.com/")

    def navigate_to_careers(self):
        company_menu = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'nav-link') and contains(., 'Company')]"))
        )
        company_menu.click()

        careers_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Careers"))
        )
        careers_option.click()

    def verify_sections(self):
        life_at_insider = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(.,'Life at Insider')]"))
        )
        our_locations = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[contains(.,'Our Locations')]"))
        )
        find_your_calling = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[contains(.,'Find your calling')]"))
        )
        return life_at_insider and our_locations and find_your_calling


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    width = int(config['WebDriverSettings']['window_width'])
    height = int(config['WebDriverSettings']['window_height'])

    if request.param == "chrome":
        web_driver = webdriver.Chrome()
    elif request.param == "firefox":
        web_driver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {request.param}")

    web_driver.set_window_size(width, height)
    web_driver.maximize_window()
    request.cls.driver = web_driver
    yield
    web_driver.quit()

@pytest.mark.usefixtures("driver")
class TestInsiderCareerPage:
    def test_career_page_sections(self):
        self.career_page = InsiderCareerPage(self.driver)
        self.driver.implicitly_wait(10)

        self.career_page.load()
        self.career_page.navigate_to_careers()
        assert self.career_page.verify_sections(), "Careers sayfasındaki belirli bölümler eksik."


# Test senaryosunu çalıştır
if __name__ == "__main__":
    pytest.main()
