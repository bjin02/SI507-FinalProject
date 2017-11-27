# README
## Project Intro
#### This is a Final Project that includes most of the concepts covered in F17 SI 507. This project will run the code to grab the data from online website, process the data to store in Database and then Visualize the data. The code is fully tested with unit test.

## Instructions - How to Run the Code
TODO

# Final Project - Bei Jin

### Part 1: Create a git repository on your computer to build your project, and push it to a GitHub repository of your own.

- Part 0: Setup the git repo and pushed the code, readme files to it
    - Initial README file
    - initial python files like:
		SI507F17_finalproject.py and the  SI507F17_finalproject_tests.py file
	- A requirements.txt file from your virtual environment
	- Any .py or other file templates that we have to fill in. e.g. secret_data.py


### Part 2: Get data from least one complex source, in a way you have learned this semester, with caching.

- Part 0: Scraping with BeautifulSoup from website
- Part 1: Setup a caching system and it must be at least as complex as e.g. the one in the textbook
	- It’s OK to borrow heavily (but should cite in your README code you borrow) from the textbook, code from class, etc, just make sure it all works for your code in your project

### Part 3: Implementing the classes, functions, models and Connecting to Database

- Part 0: Implement at least 1 class definition
	- The class should include a __repr__ method and a __contains__ method
- Part 1: Use this class definition for anything useful in your program
	- using it to process the data you gather and storing them in database tables, or using it to process data that results from querying your database
- Part 2: Connect to the database and get in at least 2 different database tables
  - Set up at least 2 database tables in a database, and write code to store data in them. 
  - Each database table have a least 2 columns and end up containing at least 4 rows of data.
  - The tables you create have at least 1 relationship existing between them, e.g. so you could make a reasonable JOIN query on the two tables.
  - Have more than two tables if you want, and you may make the database structure more complex.
  

### Part 4: Include a full test suite for your project.
- Part 0: You must have at least 15 test methods and at least 2 subclasses of unittest.TestCase which should have good test coverage of the project
	-  Use at least one setUp method (e.g. if you need to create instances to test, open files to test…), and a tearDown method if it is useful

### Part 4: Include some visual representation of your data that is clear
- Part 0: Learn and use the library Plotly, which has a pretty clear Python API I highly recommend! It creates nice charts and graphs. https://plot.ly/python/
