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

3. Preprocessing Scraped Data
    - Files:
         * preprocessed_AD , preprocessed_AI , preprocessed_DA , preprocessed_JS (those are the csv files of each track data)
         * Data_Preprocessing.ipynb , Data_Preprocessing.py (script for data preprocessing .py or .ipynb)
    - Description: Cleaning and processing the scraped job data, handling missing values, normalizing formats, and preparing data for analysis.
    - Output: A cleaned dataset ready for combination and analysis.

5. Combining Tracks Data
    - Files: Upwork_Scrapped_Dataset_Before_Preprocessing.csv and Upwork_Scrapped_Dataset_After_Preprocessing.csv
    - Description: Mergeing job data across different tracks into a single structured dataset for further insights.
  
6. Visualization and Insights
    - Description: Generates visualizations and extracts meaningful insights from the cleaned and combined job dataset.
    - Output: Plots inside the visualization notebook
