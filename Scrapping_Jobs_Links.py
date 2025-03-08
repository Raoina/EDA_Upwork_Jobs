# Importing necessary libraries
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# Setting up Selenium with undetected_chromedriver options
options = uc.ChromeOptions()
options.add_argument("start-maximized")  # Start browser maximized
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection

# Initializing the WebDriver
upwork_jobs = uc.Chrome(options=options)

# Define the search query and base URL
search_query = "artificial intelligence" # if we changed this, then we are scrapping other jobs like data analyst, javascript, and Android Developer
base_url = "https://www.upwork.com"
num_pages = 20  # Number of pages to scrape

# Lists to store job data
all_job_titles = []
all_job_links = []

# Scrape job titles and links from multiple pages
for p in range(1, num_pages + 1):
    print(f"Scraping page {p}...")

    # Load the job search results page
    upwork_jobs.get(f"https://www.upwork.com/nx/search/jobs/?from_recent_search=true&q={search_query}&page={p}&per_page=50")
    time.sleep(20)  # Wait for the page to load (adjust if necessary)

    # Extract job titles
    job_elements = upwork_jobs.find_elements(By.XPATH, '//h2[@class="h5 mb-0 mr-2 job-tile-title"]/a')
    job_titles = [job.text for job in job_elements]
    all_job_titles.extend(job_titles)

    # Extract job links
    job_links = [job.get_attribute("href") for job in job_elements]
    job_links = [base_url + link if link.startswith("/") else link for link in job_links]
    all_job_links.extend(job_links)

    print(f"Finished page {p}: Found {len(job_titles)} job titles and {len(job_links)} job links.")

print(f"Total job titles: {len(all_job_titles)}")
print(f"Total job links: {len(all_job_links)}")

# Close the browser session
upwork_jobs.quit()

# Creating a DataFrame from the collected data
df = pd.DataFrame({
    'Title': all_job_titles,
    'Link': all_job_links
})

# Display the first few rows of the DataFrame
print(df.head())

# Save the data to a CSV file
filename = f"{search_query.replace(' ', '_')}_Jobs_Links.csv"
df.to_csv(filename, index=False)
print(f"DataFrame saved to {filename}")