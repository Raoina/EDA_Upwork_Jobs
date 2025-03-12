# DEP-Project
Goal: Scraping job listings from Upwork, preprocessing the collected data, and extracting useful insights.

*Project Steps*
1. Scraping Job Links
    - File: Scrapping_Job_Links.py (or .ipynb)
    - Description: This script scrapes Upwork for job listings related to multiple tracks:
          Artificial Intelligence
          JavaScript
          Data Analyst
          Android Developer
    - Output: A CSV file containing job links for each category, which will be used in the next step to extract job details.

2. Extracting Job Details
    - File: Scrapping_All_Jobs_per_Track.py (or .ipynb)
    - Description: This script loops through the job URLs in each track's CSV file, accesses each job listing, and extracts relevant features such as:
Price, Job Type, Required skills, duration, etc.
    - Output: A CSV file for each track containing the scraped job details.
