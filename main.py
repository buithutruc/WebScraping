# import libraries
from bs4 import BeautifulSoup
import requests

def find_jobs():
    # connect to the website and pull in data
    html_text = requests.get('https://www.workopolis.com/jobsearch/find-jobs?ak=Full%20Time').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('article', class_ = 'SerpJob isp')

    count = 1
    for job in jobs:
        
        # filter the jobs that have posted date
        posted_date = job.find('span', 'ctx-i18n-translated')
        if (posted_date == None):
            continue
        else:
            date_text = posted_date.text  
            job_title = job.find('h2', class_ = "SerpJob-title").text
            job_location = job.find('span', class_="SerpJob-property SerpJob-location").text.split('—')[-1].strip()
            job_salary = job.find('span', class_="Salary")
            if (job_salary == None):
                salary_text = "N/A"
            else:
                # reformat the salary text
                salary_info= (job_salary).text.split('-')
                if(len(salary_info) == 1):
                    salary_text= "".join(salary_info)
                else:
                    salary_text = salary_info[0] + "- " + salary_info[1].strip()
            # write each job post in one text file        
            with open(f'jobs/{count}.txt', 'w') as f:     
                f.write(f'''Job Title: {job_title}
Job Location: {job_location}
Salary: {salary_text}
Posted Date: {date_text}''') 
            count += 1   
              
    print(f"Total posts saved: {count-1}")
find_jobs()