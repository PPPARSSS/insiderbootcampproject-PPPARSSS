import time

from nltk.corpus.reader import xpath
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)


# Quality Assurance Kariyer Sayfasına git
driver.get("https://useinsider.com/careers/quality-assurance/")
print("Kariyer sayfası açıldı.")

# "See all QA jobs" butonuna tıkla
see_all_qa_jobs_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//a[contains(@class,'btn btn-outline-secondary rounded text-medium mt-2 py-3 px-lg-5 w-100 w-md-50')]")))
see_all_qa_jobs_button.click()
print("Kariyer alternatiflerine tıklanıldı.")

time.sleep(3)  # Hata almasın diye

# "Filter by Location" listesini aç
location_filter_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#select2-filter-by-location-container")))
#location_filter_button.click()
print("Konum filtresi açıldı.")

time.sleep(3)

# "Istanbul, Turkey" seçeneğini bul ve seç
istanbul_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Istanbul, Turkey')]")))
istanbul_option.click()
print("Istanbul seçildi.")
time.sleep(1)

# "Filter by Department" listesini aç
department_filter_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#select2-filter-by-department-container")))
#department_filter_button.click()
print("Departman filtresi açıldı.")

time.sleep(1)

# "Quality Assurance" seçeneğini bul ve seç
qa_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Quality Assurance')]")))
qa_option.click()
print("Quality Assurance seçildi.")

time.sleep(1)

# İş pozisyonlarının XPath ifadeleri
positions_xpaths = [
    "//p[@class='position-title font-weight-bold'][contains(.,'Senior Software Quality Assurance Engineer')]",
    "//p[@class='position-title font-weight-bold'][contains(.,'Software QA Tester- Insider Testinium Tech Hub (Remote)')]",
    "//p[@class='position-title font-weight-bold'][contains(.,'Software Quality Assurance Engineer')]",
    "//p[@class='position-title font-weight-bold'][contains(.,'Software Quality Assurance Manager (Remote)')]"
]

# Her iş pozisyonu için gerekli kontroller
for i, position_xpath in enumerate(positions_xpaths, start=1):
    # Pozisyon başlığını kontrol et
    position_title_element = wait.until(EC.visibility_of_element_located((By.XPATH, position_xpath)))
    print(f"Position {i}: {position_title_element.text} kontrol ediliyor...")

    # Departman bilgisini kontrol et
    department_info_element = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                           f"(//span[@class='position-department text-large font-weight-600 text-primary'][contains(.,'Quality Assurance')])[{i}]")))
    print(f"Position {i}: {department_info_element.text} departman kontrolü...")

    # Konum bilgisini kontrol et
    location_info_element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, f"(//div[@class='position-location text-large'][contains(.,'Istanbul, Turkey')])[{i}]")))
    print(f"Position {i}: {location_info_element.text} lokasyon kontrolü...")

print(
    "Her iş pozisyonu için 'Quality Assurance' pozisyon ve departman alanlarında, 'Istanbul, Turkey' ise konum alanında doğrulanmıştır.")


print("Job listings are present for Istanbul, Turkey location and Quality Assurance department.")

# Locating 'View Role' buttons
view_role_buttons = driver.find_elements(By.XPATH, "//a[contains(.,'View Role')]")

for button in view_role_buttons:
    # Scroll to the element
    actions.move_to_element(button).perform()

    # Wait for the element to be clickable
    wait.until(EC.element_to_be_clickable(button))

    # Click 'View Role' button using JavaScript
    driver.execute_script("arguments[0].click();", button)

    # Switch to new window
    driver.switch_to.window(driver.window_handles[1])

    # Verify Lever Application form is present
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@data-qa,'show-page-apply')]")))
    print("Lever Application form page is verified.")

    # Close the new window and switch back
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

print("Tüm 'View Role' linkleri için işlemler başarıyla tamamlandı.")

# Test tamamlandı, tarayıcıyı kapat
driver.quit()
