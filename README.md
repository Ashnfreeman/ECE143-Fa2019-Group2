# ECE 143 Final Project: Engineering Jobs Analysis

## File Structure

The "Datasets and Pictures" folder contains all the files you will need to download and store in one folder somewhere locally.

The pdf "ECE143_FinalPresentation_Group2" is our final presentation slides.

The Jupyter notebook "ECE143_FinalSubmission_Group2.ipynb" is a Jupyter notebook that contains all of the code to create our graphics.

Their are 5 .py files in this repository:

* HardwareVersusSoftware.py
* Salary.py
* wordclouds.py
* location_visualization.py
* Data_Scraping.py

All of these .py files need to be downloaded and stored in the same location as the Jupyter notebook in order for the Jupyter notebook to run.

## Prerequisites

### Modules you need to have installed:

* numpy 
* pandas
* matplotlib
* Basemap
* wordcloud

### Getting Our Code Setup to Run on Your Machine

After installing the above modules, you will need to make sure you define the path to the folder that contains all of the files you downloaded from our "Datasets and Pictures" file in this GitHub.
In the Jupyter notebook, change the path to the folder by changing the value of the variable "path_of_datasets" to the appropriate path.

## Description of Each .py File

* **HardwareVersusSoftware.py:** When run, this code produces graphs comparing the ratings of hardware jobs vs. software jobs at certain companies, and can compare different kinds of ratings across 8 different companies for both hardware and software jobs. 
* **Salary.py:** When run, this code compares average salaries across different states.
* **wordclouds.py:** When run, this code produces word clouds of "good" and "bad" reviews at 8 different companies.
* **location_visualization.py:** When run, this code produces the map figures analyzing the job distribution across different locations.
* **Data_Scraping.py:** When run, this code scrapes a dataset from Glassdoor for a certain company. In order to run this code, you must first change the URL variable (start_url) to the link that you would like (navigate to the Glassdoor page for the company that you're interested in, click on the "Reviews" tab, and use that webpage's link). In order to save your .csv file to the preferred place on your computer, change the variable "thePath" to your preferred file path. Lastly, change the variable "company" to the name of the company, or whatever you want your .csv file to be named.
 
