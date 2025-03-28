from selenium import webdriver
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.headless = False  # Show browser for debugging
driver = webdriver.Chrome(options=options)

# Try the correct URL
URL = "https://www.hackerrank.com/domains/algorithms"

driver.get(URL)
time.sleep(5)  # Allow time for page to load

print("Final URL:", driver.current_url)

if "404" in driver.title:
    print("❌ ERROR: Page not found!")
else:
    print("✅ Page loaded successfully!")

driver.quit()