# README
# Tumblr Posts Data Visualization 
## Project Intro
#### This is a Final Project that includes most of the concepts covered in F17 SI 507. This project will run the code to grab the Post data from Tumblr website, process the data to store in Database and then Visualize the data with the Plotly Dashboard API. The code is fully tested with unit test.

#### This Project is aiming to provide Visualized Data for Post among the Tumblr Bloggers.

## Instructions - How to Run the Code
 1. Pip install the required pkgs from the requirements.txt
 2. In the command line, run the python SI507F17_finalproject.py to run the main application. Note: if you see errors like the SSL certify verify failed. Please run the /Applications/Python 3.6/Install Certificates.command to update since Python 3.6 on MacOS uses an embedded version of OpenSSL, which does not use the system certificate store
 3. You are supposed to run at Python3 and please fill in the ***CLIENT_KEY, CLIENT_SECRET*** in the secret_data.py in order to run the code. These KEY, SECRETS can be found in the Canvas upload files
 4. After you run this, you are supposed to see the temp-plot.html file Representing the Chart of the data analysis for all posts https://ibb.co/dwa8C6, the bei_posts.gif Representing the Images of all posts by Vinbeigie https://ibb.co/g9AuKm  and interior_posts.gif Representing the Images of all posts by Interior https://ibb.co/cvJQQR
 5. When Code in runned, the Tumblr Blog Info/Posts API  via Oauth requests and Cache functions are called to grab the data either from online or locally. You will see the output: Loading from data cache....if the cache is hit.
 6. When the Blog Info/Posts data are fetched, the application run functions to generate the Model Instances for Info/Post and they will print out as the repr() format.
 7. When Model Instances are generated, the database setup connection is called to insert the data to the DB tables. You will see : Success connecting to database
Setup database complete in the output. Note: The DB table name is ***FinalProject*** you will see that in the config.py. You should also replace the ***db_user, db_password*** with your username, password in order to connect your DB locally.
 8.  After successfully inserting the data to DB, you will see lots of Success connecting to database in the output. And there is some DB query functions running to grab the data from DB for Data Analysis. There is also JOIN query for the two tables: *Info* and *Post*.
 9. After getting these query data, plotly function is running to generate the chart html file. You can see the output in the ***temp-plot.html*** file. 
 10. There is another Gif file generation function running to generate the Gif files(***bei_posts.gif*** and ***interior_posts.gif***) to Visualize all the images in the Posts by Vinbeigie and Interior.
 11. Links to the resources: plotly https://plot.ly/python/offline/, imageio https://imageio.github.io/
 12. Citation of the code example borrowed from class: oauth1_twitter_caching.py
in Lecture 11.

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

- Part 0: Get Tumblr Post data from Tumblr websites via OAuth authentication, process the data to grab the required fields to generate the Post/Info data class instances.
- Part 1: Store the raw data into files and setup a local file based caching system and it can support cache data expire.

### Part 3: Implementing the classes, functions, models and Connecting to Database

- Part 0: Implement the Info, Post data class to model the data
	- The class should include a __repr__ method that can descripe the Post/Info data
	- And a __contains__ method to check if the Post data contains some words in Summary 
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
