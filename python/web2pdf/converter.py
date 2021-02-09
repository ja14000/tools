
import sys
import json
import base64
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(1920, 1200))
# display.start()

if len(sys.argv) != 3:
  print ("usage: converter.py <html_page_sourse> <filename_to_save>")
  exit()

# myFindElement(String xpath)
# {
#     try{
#         driver.findElement(By.xpath(path))
#     }
#     catch (ElementNotFoundException e){
#         if !closethepopup(){print ('Element not found')}
#     }
#     catch (GeneralException ge){
#     }
# }


def send_devtools(driver, cmd, params={}):
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  if response.get('status'):
    raise Exception(response.get('value'))
  return response.get('value')


def get_pdf_from_html(path, chromedriver='./chromedriver', print_options = {}):
  webdriver_options = Options()
  webdriver_options.add_argument('--headless')
  # webdriver_options.add_argument('--disable-gpu')
  # webdriver_options.add_argument('--printing') #driver 88 and above only
  webdriver_options.add_argument('--run-all-compositor-stages-before-draw')
  webdriver_options.add_argument('--window-size=1920,1200')
  webdriver_options.add_argument('--viewport-size=1920,1200')
  webdriver_options.add_argument('--ignore-certificate-errors')
  webdriver_options.add_argument('--no-sandbox')
  webdriver_options.add_argument('--disable-dev-shm-usage')
  webdriver_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
  # webdriver_options.add_argument('load-extension=./extensions/ublock_origin.crx')
  # webdriver_options.add_argument('--load-extension=./extensions/idcookies.zip')
  # webdriver_options.add_argument('load-extension=./extensions/dark_reader.crx')
  # webdriver_options.add_extension('./extensions/headless.crx')
  # webdriver_options.add_extension('./extensions/idcookies.zip')
  # webdriver_options.add_extension('./extensions/dark_reader.crx')
  # webdriver_options.add_extension('./extensions/ublock_origin.crx')
  
  driver = webdriver.Chrome(chromedriver, options=webdriver_options)
  driver.set_window_size(1920, 1080) #Ensures highest res version of any image on the page is loaded
  driver.get(path)
  # time.sleep(5)
  # alert = driver.switch_to_alert()
  # alert.accept() 
  # content = driver.page_source

  # with open('webpage.html', 'w') as f:

  #     f.write(content)

  # driver.find_element_by_xpath('//*[@id="eu-cookie-policy"]/div/div[2]/button').click()
  # driver.find_element_by_id(("cookie_action_close_header")).click();
  try:
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="I AGREE"]'))).click()
  except:
    print('error')
    pass

  # try:
  #   a = Alert(driver)
  #   a.accept()
  # except:
  #   print('error2')


  #Force lazy images/frames to fully load by scrolling them into view. 
  # Scrolling by 100px seems to be the sweet spot, going faster means the images
  # don't have time to load, going slower means the script takes a long time to 
  # complete execution.
  

  startPos = 0
  newPos = 1
  currentPos = 0

  pageLength = driver.execute_script("return document.body.scrollHeight"); # Excecute JS code that returns the height of the page in pixels
  # pageLength = (math.ceil(pageLength/100)*100)
  
  while startPos != newPos:
      startPos = driver.execute_script("return window.scrollY;")
      currentPos += 100
      driver.execute_script("window.scrollTo(0, {});".format(currentPos))
      newPos = driver.execute_script("return window.scrollY;")
      # print(posA)
      # print(posB)
  print('Page Length (px): ' + str(pageLength))
  print('Final Position (px): ' + str(newPos))
  calculated_print_options = {
    'landscape': False,
    'marginTop': 0,
    'marginBottom': 0,
    'marginLeft': 0,
    'marginRight': 0,
    'paperWidth': 11.75,
    'paperHeight': int((pageLength/100)+1),
    'displayHeaderFooter': False,
    'printBackground': True,
	  'preferCSSPageSize': True,
    'include-background': True,
  }
  calculated_print_options.update(print_options)
  result = send_devtools(driver, "Page.printToPDF", calculated_print_options)
  driver.close()
  driver.quit()
  return base64.b64decode(result['data'])

if __name__ == "__main__":
  pass
  # TODO: add short help layout


result = get_pdf_from_html(sys.argv[1], chromedriver='./chromedriver')
with open(sys.argv[2], 'wb') as file:
  file.write(result)
print('PDF written to: ' + sys.argv[2])

# os.startfile(sys.argv[2])
subprocess.run(['open', sys.argv[2]], check=True)
