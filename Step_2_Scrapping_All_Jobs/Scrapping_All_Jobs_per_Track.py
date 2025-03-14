import time
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# Set up Chrome options for undetected ChromeDriver
options = uc.ChromeOptions()
options.add_argument("start-maximized")  # Start browser in maximized mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection

# Initialize undetected ChromeDriver
upwork_ai = uc.Chrome(options=options)

# Load job links from CSV file
df_jobs = pd.read_csv("artificial_intelligence_Jobs_Links.csv")
rows, cols = df_jobs.shape
print(f"Number of rows: {rows}")
print(f"Number of columns: {cols}")

# Convert job links column to a list
link_list = df_jobs["Link"].tolist()

# Set page load timeout
upwork_ai.set_page_load_timeout(120)

# Initialize data storage lists
scraped_data = []
error_scrapped = 0
count = 0
scrapped_links = 0

# Loop through each job link
for url in link_list:
    upwork_ai.get(url)  # Open the job page
    time.sleep(20)  # Allow page to load completely
    
    try:
        # Extract job title
        title = [t.text for t in upwork_ai.find_elements(By.XPATH, '//h4[@class="m-0"]')]
        
        # Extract job location
        location = [l.text for l in upwork_ai.find_elements(By.XPATH, '//span[@class="text-light-on-muted" and @data-v-371e7192=""]')]
        
        # Extract job description
        description = [d.text for d in upwork_ai.find_elements(By.XPATH, '//p[@class="text-body-sm" and @data-v-7304a83e=""]')]
        
        # Extract fixed price (if applicable)
        fixed_price = [p.text for p in upwork_ai.find_elements(By.XPATH, '//strong[@data-v-175eba53]')]
        
        # Extract budget details (min and max budget)
        budget_elements = upwork_ai.find_elements(By.XPATH, '//div[@data-test="BudgetAmount"]/p/strong')
        budget_values = [b.text.strip() for b in budget_elements if b.text.strip()]
        min_budget = budget_values[0] if len(budget_values) > 0 else None
        max_budget = budget_values[1] if len(budget_values) > 1 else None
        
        # Extract job application details (proposals, interviews, invites sent, unanswered invites)
        proposals = [p.text for p in upwork_ai.find_elements(By.XPATH, '//li[@class="ca-item"]//span[contains(text(), "Proposals:")]/following-sibling::span[@class="value"]')]
        interviewing = [i.text for i in upwork_ai.find_elements(By.XPATH, '//li[@class="ca-item"]//span[contains(text(), "Interviewing:")]/following-sibling::div')]
        invites_sent = [i.text for i in upwork_ai.find_elements(By.XPATH, '//li[@class="ca-item"]//span[contains(text(), "Invites sent:")]/following-sibling::div')]
        unanswered_invites = [u.text for u in upwork_ai.find_elements(By.XPATH, '//li[@class="ca-item"]//span[contains(text(), "Unanswered invites:")]/following-sibling::div')]
        
        # Extract client details (total spend, location, hires, active jobs)
        client_total_spent = [c.text for c in upwork_ai.find_elements(By.XPATH, '//strong[@data-qa="client-spend"]/span')]
        client_location = [l.text.strip() for l in upwork_ai.find_elements(By.XPATH, '//li[@data-qa="client-location"]/strong')]
        
        # Extract hires and active job details
        hires_elements = upwork_ai.find_elements(By.XPATH, '//div[@data-qa="client-hires"]')
        hires_text = hires_elements[0].text.strip() if hires_elements else None
        hires, active = None, None
        if hires_text:
            numbers = re.findall(r'\d+', hires_text)
            hires = numbers[0] if len(numbers) > 0 else None
            active = numbers[1] if len(numbers) > 1 else None  
        
        # Extract experience level (Entry, Intermediate, Expert)
        experience_levels = ["Expert", "Intermediate", "Entry"]
        experience_level = None
        for level in experience_levels:
            exp_element = upwork_ai.find_elements(By.XPATH, f'//strong[contains(text(), "{level}")]')
            if exp_element:
                experience_level = level
                break
        
        # Extract skills required
        skill_elements = upwork_ai.find_elements(By.XPATH, '//span[contains(@class, "air3-badge-highlight")]')
        skills = list(set([skill.text.strip() for skill in skill_elements if skill.text.strip()]))
        
        # Extract job type (Hourly or Fixed-price)
        job_type_element = upwork_ai.find_elements(By.XPATH, '//div[@class="description"][text()="Hourly" or text()="Fixed-price"]')
        job_type = job_type_element[0].text if job_type_element else None
        
        # Extract duration and work hours (for hourly jobs)
        duration = None
        work_hours = None
        if job_type == "Hourly":
            duration_element = upwork_ai.find_elements(By.XPATH, '//strong[contains(text(), "month")]')
            work_hours_element = upwork_ai.find_elements(By.XPATH, '//strong[contains(text(), "hrs/week")]')
            duration = duration_element[0].text if duration_element else None
            work_hours = work_hours_element[0].text if work_hours_element else None
        
        # Store extracted data
        scraped_data.append({
            "title": title[0] if title else None,
            "url": url,
            "job_type": job_type,
            "location": location[0] if location else None,
            "description": description[0] if description else None,
            "min_budget": min_budget,
            "max_budget": max_budget,
            "fixed_price": fixed_price if fixed_price else None,
            "experience_level": experience_level,
            "skills": skills,
            "duration": duration,
            "work_hours": work_hours,
            "proposals": proposals[0] if proposals else None,
            "interviewing": interviewing[0] if interviewing else None,
            "invites_sent": invites_sent[0] if invites_sent else None,
            "unanswered_invites": unanswered_invites[0] if unanswered_invites else None,
            "client_total_spent": client_total_spent[0] if client_total_spent else None,
            "client_location": client_location[0] if client_location else None,
            "active": active,
            "hires": hires
        })
        
        scrapped_links += 1
        print(f"Scraped Links: {scrapped_links}")
    
    except Exception as e:
        error_scrapped += 1
        print(f"Error scraping {url}: {e}")
        print(f"Not Scrapped: {error_scrapped}")
    
    count += 1
    print(f"URL Finished: {count}")

# Convert scraped data into a DataFrame and save as CSV
df_scrapped_jobs = pd.DataFrame(scraped_data)
df_scrapped_jobs.to_csv("scrapped_AI_jobs_version1.csv", index=False)

# Close the browser session
upwork_ai.quit()

# Display DataFrame info
df_scrapped_jobs.info()
