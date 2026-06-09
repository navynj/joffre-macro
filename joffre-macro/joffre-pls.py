
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
import time


if __name__ == "__main__":
    try:
        date = input("Enter the date: ")
        people = input("Enter the number of people: ")
        options = uc.ChromeOptions() 
        options.headless = False
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = uc.Chrome(options=options)
        
        wait = WebDriverWait(driver, 10)

        driver.get("https://reserve.bcparks.ca/dayuse/registration")
        bookPassBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Book a pass for Joffre Lakes Provincial Park']")))
        driver.execute_script("arguments[0].click();", bookPassBtn)

        while(True):
            wait.until(EC.visibility_of_element_located((By.ID, 'visitDate')))
            print('===================', datetime.datetime.now())
            
            dateInput = driver.find_element(By.ID, 'visitDate')
            passType = driver.find_element(By.ID, "passType")
            passTypeSelect = Select(passType)

            dateInput.clear()
            dateInput.send_keys(date)
            passTypeSelect.select_by_index(1)

            print('date', dateInput.get_attribute("value"))
            print('passType', passType.get_attribute("value"))

            visitTimeDay = driver.find_element(By.ID, "visitTimeDAY")
            visitDisabled = visitTimeDay.get_attribute('disabled')
            print('visitDisabled', visitDisabled)

            if not visitDisabled:
                driver.execute_script("arguments[0].click();", visitTimeDay)
                
                passCount = driver.find_element(By.ID, "passCount")
                passCountSelect = Select(passCount)

                if people:
                    passCountSelect.select_by_value(people);
                else:
                    options = passCountSelect.options
                    last_index = len(options) - 1
                    passCountSelect.select_by_index(last_index);
                
                while True:
                    try:
                        nextBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-bs-target='#turnstileModal'")))
                        driver.execute_script("arguments[0].click();", nextBtn)
                        
                        time.sleep(0.2)

                        while True:
                            modalOpened = driver.find_element(By.ID, "turnstileModal")
                            modalOpenedClass = modalOpened.get_attribute('class')
                            if 'show' in modalOpenedClass:
                                continue
                            else:
                                break
                                
                    
                        stillNextBtn = driver.find_element(By.CSS_SELECTOR, "[data-bs-target='#turnstileModal'")
                        if stillNextBtn:
                            driver.refresh()
                            continue
                        else:
                            break
                    except:
                        continue
            # break
            else:
                driver.refresh()

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(999)
    finally:
        print("* Success!!!!!!!")
        time.sleep(999) 
