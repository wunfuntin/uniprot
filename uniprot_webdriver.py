from selenium.webdriver import Safari
from selenium.webdriver.safari.options import Options as SafariOptions
import time
safari_options = SafariOptions()
driver = Safari(options=safari_options)



URL = 'https://www.uniprot.org/'

driver.get(URL)

