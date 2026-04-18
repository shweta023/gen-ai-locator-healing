from selenium import webdriver

# Initialize the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

# Open a webpage
driver.get("https://the-internet.herokuapp.com/login")

# Get the page source
source = driver.page_source
print(source)

# Quit the driver
driver.quit()