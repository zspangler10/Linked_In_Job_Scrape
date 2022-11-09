from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Creating a webdriver instance
path = r'C:\Users\user\PycharmProjects\pythonProject\chromedriver\chromedriver.exe'
driver: webdriver = webdriver.Chrome(path)
# Opening the url we have just defined in our browser
driver.get("https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Pittsburgh%2C%20Pennsylvania%2C"
           "%20United%20States&geoId=101351937&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0")

print("Opening URL")

# Maximize Window
driver.maximize_window()
driver.minimize_window()
driver.maximize_window()
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10) # to ensure window loads

print("Collecting Job Elements")
# We create a while loop to browse all jobs, gives up after X number of tries of the loop "counter < 200"
counter = 0
while counter < 1:
    # We keep scrolling down to the end of the view.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        # We try to click on the load more results buttons in case it is already displayed.
        infinite_scroll_button = driver.find_element(By.XPATH, ".//button[@aria-label='Load more results']")
        infinite_scroll_button.click()
        counter += 1
        time.sleep(0.1)

    except:
        # If there is no button, there will be an error, so we restart the loop
        time.sleep(0.1)
    pass

# Collecting all HTML elements where each job's information resides
job_lists = driver.find_element(By.CSS_SELECTOR, 'ul[class="jobs-search__results-list"]') # Contains all the job cards
jobs = job_lists.find_elements(By.XPATH, "//*[@id='main-content']/section[2]/ul/li") # Each individual job card

new_set = set(jobs)
print("Unique Jobs Found:", len(new_set))

# Create empty lists to store data in later
job_title_list = []
company_name_list = []
job_location_list = []
job_date_list = []
job_link_list = []
job_description_list = []
job_seniority_list = []
job_type_list = []
job_function_list = []
job_industry_list = []

print("Scraping Job Information")

# Setting Counter Variable to 0 for Percentage tracking
current_num = 0

# For loop to try to run through each code block for each job we just collected
for job in jobs:
    # Click on individual Job post and then collect Job Link
    try:
        job.find_element(By.CSS_SELECTOR, "a[class*='base-card__full-link']").click()
        job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        job_link_list.append(job_link)
    except:
        job_link_list.append(None)
        pass

    # Scrape Job Title
    try:
        job_title = job.find_element(By.CSS_SELECTOR, "a[class*='base-card__full-link']").text
        job_title_list.append(job_title)
    except:
        job_title_list.append(None)
        pass

    # Scrape Company Name
    try:
        company_name = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
        company_name_list.append(company_name)
    except:
        company_name_list.append(None)
        pass

    # Scrape Job Location
    try:
        job_location = job.find_element(By.CLASS_NAME, "job-search-card__location").text
        job_location_list.append(job_location)
    except:
        job_location_list.append(None)
        pass

    # Scrape Job Posted Date
    try:
        job_date = job.find_element(By.XPATH, '//*[@id="main-content"]/section[2]/ul/li/div/div/div/time').get_attribute(
            "datetime")
        job_date_list.append(job_date)
    except:
        job_date_list.append(None)
        pass

    # Scrape Job Description
    jd_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div'
    try:
        job_description = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, jd_path))).text
        job_description_list.append(job_description)
    except:
        job_description_list.append(None)
        pass

    # Scrape Job Seniority
    seniority_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span'

    try:
        job_seniority = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, seniority_path))).get_attribute("innerText")
        job_seniority_list.append(job_seniority)
    except:
        job_seniority_list.append(None)
        pass

    # Scrape Job Type
    emp_type_path = '/html/body/div/div/section/div/div/section/div/ul/li[2]/span'

    try:
        job_type = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, emp_type_path))).get_attribute("innerText")
        job_type_list.append(job_type)
    except:
        job_type_list.append(None)
        pass

    # Scrape Job Function
    function_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[3]/span'

    try:
        job_function = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, function_path))).get_attribute("innerText")
        job_function_list.append(job_function)
    except:
        job_function_list.append(None)
        pass

    # Scrape Job Industry
    industry_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span'

    try:
        job_industry = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, industry_path))).get_attribute("innerText")
        job_industry_list.append(job_industry)
    except:
        job_industry_list.append(None)
        pass

    # Percentage Progress Tracker
    print("Current at: ", current_num, "Percentage at: ", (current_num + 1) / len(jobs) * 100, "%")
    current_num += 1  # adds +1 to current_num counter

# Creating Pandas dataframe with custom header names
job_data = pd.DataFrame({
    'Date Posted': job_date_list,
    'Company Name': company_name_list,
    'Job Title': job_title_list,
    'Location': job_location_list,
    'Job Description': job_description_list,
    'Seniority': job_seniority_list,
    'Employment Type': job_type_list,
    'Function': job_function_list,
    'Industry': job_industry_list,
    'Link': job_link_list
})

# Exporting Pandas dataframe as CSV to specified file path
job_data.to_csv(r'C:\Users\user\Desktop\Linked_In_Job_Scrape\Linked_In_Job_Scrape.csv', index=False, header=True,
                encoding="utf-8")
print("Completed")
