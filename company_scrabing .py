import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
# Setup WebDriver for Chrome
browser = webdriver.Chrome()

# Open the website
browser.get('https://techbehemoths.com/companies')
print(browser.title)

# Wait until elements are loaded
wait = WebDriverWait(browser, 10)
base_url=browser.current_url


company_data = []
for i in range(1,5):
    try:
        print("Current URL:", browser.current_url)
        # Find the next page link using a more specific XPath
        next_page_link=f"{base_url}?page={i}"
        # Navigate to the next page
        browser.get(next_page_link)
        browser.implicitly_wait(15)
        # Find the company names
        company_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.co-box__name.font-medium a")))
        # Print the current page URL
        print("Current URL:", browser.current_url) 
        # Extract the company names, links, and additional information
        for company in company_elements:
            try:
                company_name = company.text
                company_link = company.get_attribute('href')
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[1])
                browser.get(company_link)

                # Extract additional information from the company page
                locations = browser.find_element(By.CLASS_NAME, "co-box__loc").text
                #__layout > div > div.page-content > div > div.company-jumbotron.header-spacer.bg-blue > div.container > div > div.col-lg-8 > div.c--descr > div > div.co-lrg-meta > div > div:nth-child(2) > span.value.txt-blue.font-medium
                team_size=browser.find_element(By.CSS_SELECTOR,'div.col-lg-8 > div.c--descr > div > div.co-lrg-meta > div > div:nth-child(2) > span.value.txt-blue.font-medium').text
 
                foundation_year=browser.find_element(By.CSS_SELECTOR,'div:nth-child(1) > span.value.txt-blue.font-medium').text
                print(foundation_year,team_size)
                service_speciality_list = browser.find_element(By.CLASS_NAME, "services-list").text

                # Extract the hourly rate
                hourly_rate_box = browser.find_element(By.CLASS_NAME, "co-box__tltip")
                hover = ActionChains(browser).move_to_element(hourly_rate_box)
                hover.perform()

                try:
                    tooltip_text = browser.find_element(By.CSS_SELECTOR, "span.co-box__tltip-txt.flex-centered.absolute").text
                    print(tooltip_text)
                except NoSuchElementException:
                    tooltip_text = "N/A"

                company_data.append({
                    'Company Name': company_name,
                    'Company Link': company_link,
                    'Locations': locations,
                    'Service Speciality List': service_speciality_list,
                    'Team Size':team_size,
                    'Founding Year':foundation_year,
                    'Hourly Rate': tooltip_text
                })
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
            except NoSuchElementException:
                print(f"Could not extract data for company: {company_name}")
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                continue       
    except TimeoutException:
        print("Timed out waiting for the elements to load.")
        browser.quit()
        exit()   
    


# Save the data to a CSV file
df = pd.DataFrame(company_data)
df.to_csv('company_data.csv', index=False)

# Close the browser
browser.quit()
    