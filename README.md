# README
# Tumblr Posts Data Visualization 
## Project Intro
#### This is a Final Project that includes most of the concepts covered in F17 SI 507. This project will run the code to grab the US National Park data from online website, process the data to store in Database and then Visualize the data with the Plotly Dashboard API. The code is fully tested with unit test.

#### This Project is aiming to provide Visualized Data for Post among the Tumblr Bloggers.

## Instructions - How to Run the Code
TODO

# Final Project - Bei Jin

### Part 1: Create a git repository on your computer to build your project, and push it to a GitHub repository of your own.

- Part 0: Setup the git repo and pushed the code, readme files to it
    - Initial README file
    - initial python files like:
		SI507F17_finalproject.py and the  SI507F17_finalproject_tests.py file
		finalproject.py will cover the data models, cache system, website data scraping system and the database connection utilization system.
		tests.py will cover all required unit tests.
	- A requirements.txt file from your virtual environment
	- Any .py or other file templates that we have to fill in. e.g. secret_data.py for the webiste API call credentials, .csv files for local caching etc.


### Part 2: Get data from least one complex source, in a way you have learned this semester, with caching.

- Part 0: Get Tumblr Post data from Tumblr websites, process the data to grab the required fields to generate the Post data class instances.
- Part 1: Store the raw data into files and setup a local file based caching system and it can support cache data expire.

### Part 3: Implementing the classes, functions, models and Connecting to Database

- Part 0: Implement the Info, Post data class to model the data
	- The class should include a __repr__ method that can descripe the National Park data
	- And a __contains__ method to check if the National Park data contains required location information
- Part 1: Use this class definition for database models in your program
	- Process the raw data to model the Post data into instances of the classes
- Part 2: Connect to the database and get Info and Post database tables data
  - Set up Info and Post database tables in a database, and store the data instances in them. 
  - Database table data with these columns in each:
  
	  **Info**
	  	    id
		    followed
		    likes
		    total_posts	title
		    url
		    ask_page_title
		    name
	
	  **Post**
	
		    id
		    date
		    summary
		    format
		    short_url
		    can_like
		    can_reply
		    type
		    info_id
	    
  - Post table has the external key to the Info table. We can make JOIN query to these tables
  - Setup the DB connection code to Connect, Insert, Update and Query the tables
  

### Part 4: Include a full test suite for your project.
- Part 0: Implement the unit test class with unittest.TestCase which should have good test coverage of the project
	-  Test as much as possible to provide good code quality

### Part 5: Include some visual representation of your data that is clear
- Part 0: Learn and use the library Plotly, which has a pretty clear Python API to create nice charts and graphs. https://plot.ly/python/
- Part 1: Onboard the Plotly Dashboard API to visualize the Tumblr Post data in result of a dashboard that reflects the numbers of Posts in Bloggers, comparison of different Posts/Blogger Info.
