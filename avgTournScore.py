import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException 
import time 

browser = webdriver.Chrome()
browser.get("http://localhost:8000/")
print(browser.title)
try:
    wait = WebDriverWait(browser, 10)
    elem = wait.until (EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Tourn")))
    print(elem.text)
    elem.click()

    elem = wait.until (EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Oak")))
    print(elem.text)
    elem.click()

    elem = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    print(elem.text)

except TimeoutException:
    print("Locating Links in WGT Website Failed")

time.sleep(10)

golf_soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
soup_elems = golf_soup.select('td a')
scores = []
for i in soup_elems:
    score = int(i.getText())
    scores.append(score)
print("AVG : ", sum(scores) / len(scores))

    


browser.close()

   
   
