# -*- coding: utf-8 -*-
## import statements
import requests_oauthlib
import webbrowser
import json
import secret_data
import psycopg2
import psycopg2.extras
import uuid
import sys
import plotly
import plotly.graph_objs
import urllib.request
import imageio
import os
from config import *
from datetime import datetime

## OAuth1 API Constants - vary by API### Private data in a hidden secret_data.py file
CLIENT_KEY = secret_data.CLIENT_KEY # what Tumblr calls Consumer Key
CLIENT_SECRET = secret_data.CLIENT_SECRET # What Tumblr calls Consumer Secret

## CACHING SETUP
#--------------------------------------------------
# Caching constants
#--------------------------------------------------
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True
CACHE_FNAME = "cache_contents.json"
CREDS_CACHE_FILE = "creds.json"

## ADDITIONAL CODE for program should go here...
## Perhaps authentication setup, functions to get and process data, a class definition... etc.
#--------------------------------------------------
# Load cache files: data and credentials
#--------------------------------------------------
try:
    with open(CACHE_FNAME, 'r') as cache_file:
        cache_json = cache_file.read()
        CACHE_DICTION = json.loads(cache_json)
except:
    CACHE_DICTION = {}

# Load creds cache
try:
    with open(CREDS_CACHE_FILE,'r') as creds_file:
        cache_creds = creds_file.read()
        CREDS_DICTION = json.loads(cache_creds)
except:
    CREDS_DICTION = {}

#--------------------------------------------------
# Model Class and Model Instances Helper Functions
#--------------------------------------------------
class Info:
    def __init__(self, data):
        blog = data["response"]["blog"]
        self.followed = bool(blog["followed"])
        self.total_posts = int(blog["total_posts"])
        self.title = blog["title"]
        self.url = blog["url"]
        self.ask_page_title = blog["ask_page_title"]
        self.name = blog["name"]
        self.id = uuid.uuid4().fields[1]

    def __repr__(self):
        return "Blog Info Data Name:" + self.name + "\n Url:" + self.url +" Title:" + self.title + "\n Ask Page Title:" + self.ask_page_title + "\n Total Posts:" + str(self.total_posts) + "\n Is Followed:" + str(self.followed)

    def __contains__(self, str):
        return str in self.name or str in self.title

class Post:
    def __init__(self, posts, info_id):
        self.date = posts["date"]
        self.summary = posts["summary"]
        self.format = posts["format"]
        self.short_url = posts["short_url"]
        self.can_like = bool(posts["can_like"])
        self.can_reply = bool(posts["can_reply"])
        self.type = posts["type"]
        self.id = uuid.uuid4().fields[1]
        self.info_id = info_id
        self.image = posts["photos"][0]["original_size"]["url"]

    def __repr__(self):
        return "Post Data Summary:" + self.summary + "\n Creaated Date:" + self.date + "\n Fomrat:" + self.format + "\n Short_URL:" + self.short_url + "\n Can Like:" + str(self.can_like) + "\n Can Reply:" + str(self.can_reply) + "\n Type:" + self.type

    def __contains__(self, str):
        return str in self.summary

def generate_model_instances(info_result, post_result):
    info = Info(info_result)
    print(repr(info))
    posts = []
    for each in post_result["response"]["posts"]:
        post = Post(each, info.id)
        print(repr(post))
        posts.append(post)
    print(len(posts))
    return info, posts


#---------------------------------------------
# Cache functions
#---------------------------------------------
def has_cache_expired(timestamp_str, expire_in_days):
    """Check if cache timestamp is over expire_in_days old"""
    # gives current datetime
    now = datetime.now()

    # datetime.strptime converts a formatted string into datetime object
    cache_timestamp = datetime.strptime(timestamp_str, DATETIME_FORMAT)

    # subtracting two datetime objects gives you a timedelta object
    delta = now - cache_timestamp
    delta_in_days = delta.days


    # now that we have days as integers, we can just use comparison
    # and decide if cache has expired or not
    if delta_in_days > expire_in_days:
        return True # It's been longer than expiry time
    else:
        return False

def get_from_cache(identifier, dictionary):
    """If unique identifier exists in specified cache dictionary and has not expired, return the data associated with it from the request, else return None"""
    identifier = identifier.upper() # Assuming none will differ with case sensitivity here
    if identifier in dictionary:
        data_assoc_dict = dictionary[identifier]
        if has_cache_expired(data_assoc_dict['timestamp'],data_assoc_dict["expire_in_days"]):
            if DEBUG:
                print("Cache has expired for {}".format(identifier))
            # also remove old copy from cache
            del dictionary[identifier]
            data = None
        else:
            data = dictionary[identifier]['values']
    else:
        data = None
    return data


def set_in_data_cache(identifier, data, expire_in_days):
    """Add identifier and its associated values (literal data) to the data cache dictionary, and save the whole dictionary to a file as json"""
    identifier = identifier.upper()
    CACHE_DICTION[identifier] = {
        'values': data,
        'timestamp': datetime.now().strftime(DATETIME_FORMAT),
        'expire_in_days': expire_in_days
    }

    with open(CACHE_FNAME, 'w') as cache_file:
        cache_json = json.dumps(CACHE_DICTION)
        cache_file.write(cache_json)

def set_in_creds_cache(identifier, data, expire_in_days):
    """Add identifier and its associated values (literal data) to the credentials cache dictionary, and save the whole dictionary to a file as json"""
    identifier = identifier.upper() # make unique
    CREDS_DICTION[identifier] = {
        'values': data,
        'timestamp': datetime.now().strftime(DATETIME_FORMAT),
        'expire_in_days': expire_in_days
    }

    with open(CREDS_CACHE_FILE, 'w') as cache_file:
        cache_json = json.dumps(CREDS_DICTION)
        cache_file.write(cache_json)

### Specific to API URLs, not private
REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
BASE_AUTH_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"

BLOG_IDENTIFIER = "blog-identifier"
DEFAULT_IDENTIFIER = "good.tumblr.com"

API_KEY = "api"
DEFAULT_METHOD = "info"

#--------------------------------------------------
# OAuth1 Functions
#--------------------------------------------------
def get_tokens(client_key=CLIENT_KEY,
               client_secret=CLIENT_SECRET,
               request_token_url=REQUEST_TOKEN_URL,
               base_authorization_url=BASE_AUTH_URL,
               access_token_url=ACCESS_TOKEN_URL,
               verifier_auto=True):
    oauth_inst = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth_inst.fetch_request_token(request_token_url)

    # Using the dictionary .get method in these lines
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    auth_url = oauth_inst.authorization_url(base_authorization_url)
    # Open the auth url in browser:
    webbrowser.open(auth_url) # For user to interact with & approve access of this app -- this script

    # Deal with required input, which will vary by API
    if verifier_auto: #if the input is default (True), like Twitter
        verifier = input("Please input the verifier:  ")
    else:
        redirect_result = input("Paste the full redirect URL here:  ")
        # returns a dictionary -- you may want to inspect that this works and edit accordingly
        oauth_resp = oauth_inst.parse_authorization_response(redirect_result)

    # Regenerate instance of oauth1session class with more data
    oauth_inst = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret,
                                                 resource_owner_key=resource_owner_key,
                                                 resource_owner_secret=resource_owner_secret, verifier=verifier)

    oauth_tokens = oauth_inst.fetch_access_token(access_token_url)  # returns a dictionary

    # Use that dictionary to get these things
    # Tuple assignment syntax
    resource_owner_key, resource_owner_secret = oauth_tokens.get('oauth_token'), oauth_tokens.get('oauth_token_secret')
    return client_key, client_secret, resource_owner_key, resource_owner_secret, verifier

def get_tokens_from_service(service_name_ident, expire_in_days=7): # Default: 7 days for creds expiration
    creds_data = get_from_cache(service_name_ident, CREDS_DICTION)
    if creds_data:
        if DEBUG:
            print("Loading creds from cache...")
            print()
    else:
        if DEBUG:
            print("Fetching fresh credentials...")
            print("Prepare to log in via browser.")
            print()
        creds_data = get_tokens()
        set_in_creds_cache(service_name_ident, creds_data, expire_in_days=expire_in_days)
    return creds_data

def create_request_identifier(url, params_diction):
    sorted_params = sorted(params_diction.items(), key=lambda x: x[0])
    params_str = "_".join([str(e) for l in sorted_params for e in l])  # Make the list of tuples into a flat list using a complex list comprehension
    total_ident = url + "?" + params_str
    return total_ident.upper()  # Creating the identifier

def get_data_from_api(request_url,
                      params_diction,
                      expire_in_days=7):
    # Check in cache, if not found, load data, save in cache and then return that data
    ident = create_request_identifier(request_url, params_diction)
    data = get_from_cache(ident, CACHE_DICTION)
    if data:
        if DEBUG:
            print("Loading from data cache: {}... data".format(ident))
    else:
        if DEBUG:
            print("Fetching new data from {}".format(request_url))
        service_ident = params_diction.get(API_KEY, DEFAULT_METHOD)
        # Get credentials
        client_key, client_secret, resource_owner_key, resource_owner_secret, verifier = get_tokens_from_service(service_ident)

        # Create a new instance of oauth to make a request with
        oauth_inst = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret,
                                                     resource_owner_key=resource_owner_key,
                                                     resource_owner_secret=resource_owner_secret,
                                                     callback_uri=verifier)

        # Call the get method on oauth instance
        # Work of encoding and "signing" the request happens behind the sences, thanks to the OAuth1Session instance in oauth_inst
        resp = oauth_inst.get(request_url + params_diction.get(BLOG_IDENTIFIER, DEFAULT_IDENTIFIER) + service_ident)
        # Get the string data and set it in the cache for next time
        data_str = resp.text
        data = json.loads(data_str)
        set_in_data_cache(ident, data, expire_in_days)
    return data

#--------------------------------------------------
# Write Data to DB
#--------------------------------------------------
# set up database connection and cursor here.
def get_connection_and_cursor():
    try:
        if db_password != "":
            db_connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
            print("Success connecting to database")
        else:
            db_connection = psycopg2.connect("dbname='{0}' user='{1}'".format(db_name, db_user))
    except:
        print("Unable to connect to the database. Check server and credentials.")
        sys.exit(1) # Stop running program if there's no db connection.

    db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    return db_connection, db_cursor

# create tables with the columns you want and all database setup here.
def setup_database():
    # Invovles DDL commands
    # DDL --> Data Definition Language
    # CREATE, DROP, ALTER, RENAME, TRUNCATE

    conn, cur = get_connection_and_cursor()

    # Check if the two tables already exist
    cur.execute("select exists(select * from information_schema.tables where table_name = 'Info')")
    infoExists = cur.fetchone()['exists']

    cur.execute("select exists(select * from information_schema.tables where table_name = 'Post')")
    postExists = cur.fetchone()['exists']

    if infoExists and postExists:
        print("Exists")
        return

    cur.execute("DROP TABLE IF EXISTS Post")
    cur.execute("""CREATE TABLE Post(
        ID SERIAL PRIMARY KEY,
        Post_Date VARCHAR(128),
        Summary TEXT,
        Format VARCHAR(128),
        Short_Url VARCHAR(255),
        Can_Like BOOLEAN,
        Can_Reply BOOLEAN,
        Type VARCHAR(128),
        Info_ID INTEGER
    )""")

    cur.execute("DROP TABLE IF EXISTS Info")
    cur.execute("""CREATE TABLE Info(
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(40),
    Total_Posts INTEGER,
    Followed BOOLEAN,
    TITLE VARCHAR(255),
    URL VARCHAR(255),
    Ask_Page_Title VARCHAR(255)
    )""")

    conn.commit()
    print('Setup database complete')
    conn.close()

# Make sure to commit your database changes with .commit() on the database connection.
def insertInfo(info_list):
    conn, cur = get_connection_and_cursor()
    for each in info_list:
        cur.execute("SELECT EXISTS(SELECT * FROM Info WHERE Info.URL Like %s)", (each.url,))
        recordExists = cur.fetchone()['exists']
        if recordExists:
            continue
        # print(each)
        cur.execute("""INSERT INTO
            Info (ID, Name, Total_Posts, Followed, TITLE, URL, Ask_Page_Title)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING""",
            (each.id, each.name, each.total_posts, each.followed, each.title, each.url, each.ask_page_title))
    conn.commit()
    conn.close()

def insertPosts(post_list, infoId):
    conn, cur = get_connection_and_cursor()
    for each in post_list:
        # print(each)
        cur.execute("SELECT EXISTS(SELECT * FROM Post WHERE Post.Short_Url Like %s)", (each.short_url,))
        recordExists = cur.fetchone()['exists']
        if recordExists:
            continue
        cur.execute("""INSERT INTO
            Post (ID, Post_Date, Summary, Format, Short_Url, Can_Like, Can_Reply, Type, Info_ID)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING""",
            (each.id, each.date, each.summary, each.format, each.short_url, each.can_like, each.can_reply, each.type, infoId))
    conn.commit()
    conn.close()

def get_and_insert_data(info_data, post_data):
    # print('--- Info Data: ---')
    # for each in info_data:
    #     print(each)
    #
    # print('--- Post data: ---')
    # for each in post_data:
    #     print(each)

    # Insert Posts/Info data
    conn, cur = get_connection_and_cursor()
    insertInfo(cur, info_data)
    insertPosts(cur, post_data)

    conn.commit()
    conn.close()

def find_can_like_in_Post():
    conn, cur = get_connection_and_cursor()
    cur.execute("SELECT COUNT(ID) FROM Post WHERE Post.can_like = 'true'")
    can_like = cur.fetchone()['count']
    cur.execute("SELECT COUNT(ID) FROM Post WHERE Post.can_like = 'false'")
    can_not_like = cur.fetchone()['count']
    conn.close()
    return can_like, can_not_like

def find_can_reply_in_Post():
    conn, cur = get_connection_and_cursor()
    cur.execute("SELECT COUNT(ID) FROM Post WHERE Post.can_reply = 'true'")
    can_reply = cur.fetchone()['count']
    cur.execute("SELECT COUNT(ID) FROM Post WHERE Post.can_reply = 'false'")
    can_not_reply = cur.fetchone()['count']
    conn.close()
    return can_reply, can_not_reply

def count_type_photo():
    conn, cur = get_connection_and_cursor()
    cur.execute("SELECT COUNT(ID) FROM Post WHERE Post.type = 'photo'")
    count_photo = cur.fetchone()['count']
    conn.close()
    return count_photo

def count_format_html():
    conn, cur = get_connection_and_cursor()
    cur.execute("SELECT COUNT(ID) FROM Post WHERE Post.format = 'html'")
    count_html = cur.fetchone()['count']
    conn.close()
    return count_html

def count_posts(id):
    conn, cur = get_connection_and_cursor()
    cur.execute("SELECT COUNT(Post.ID) FROM Post INNER JOIN Info ON Post.info_id = Info.id AND Info.id = %s", (id,))
    count = cur.fetchone()['count']
    conn.close()
    return count

def count_all_posts():
    conn, cur = get_connection_and_cursor()
    cur.execute("SELECT COUNT(ID) FROM Post")
    count = cur.fetchone()['count']
    conn.close()
    return count

#--------------------------------------------------
# Visualization Helper Functions
#--------------------------------------------------
def bar_chart(label, val):
    plotly.offline.plot({
        "data": [
            plotly.graph_objs.Bar(x=label, y=val)
        ]
    })

def get_image(data, cnt, ident):
    identifier =  os.path.abspath("image")
    file =  os.path.join(identifier, ident + str(cnt) + ".jpeg")
    urllib.request.urlretrieve(data.image, file)
    return file

def generate_gif(imagelist, file):
    images = []
    for filename in imagelist:
        images.append(imageio.imread(filename))
    imageio.mimsave(file, images, duration=0.5)
#--------------------------------------------------
# Test Helper Functions
#--------------------------------------------------
def printPostData(data):
    posts = data["response"]["posts"]
    print(type(posts))
    for post in posts:
        print([post["date"], post["summary"], post["format"], post["short_url"], post["can_like"], post["can_reply"], post["type"]])

def printInfoData(data):
    blog = data["response"]["blog"]
    print(type(blog))
    print([blog["followed"], blog["total_posts"], blog["title"], blog["url"], blog["ask_page_title"], blog["name"]])


#--------------------------------------------------
# Main Function
#--------------------------------------------------
## Make sure to run your code and write CSV files by the end of the program.
if __name__ == "__main__":
    if not CLIENT_KEY or not CLIENT_SECRET:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not REQUEST_TOKEN_URL or not BASE_AUTH_URL:
        print("You need to fill in this API's specific OAuth2 URLs in this file.")
        exit()

    # TODO: This is statically caching data, we can change to the CLI user input version
    # =============== Invoke functions ===============
    tumblr_baseurl = "https://api.tumblr.com/v2/blog/"
    tumblr_params = {'blog-identifier': "vinbeigie", 'api':"/info"}

    bei_info_result = get_data_from_api(tumblr_baseurl,
                                      tumblr_params)
    # Info
    # printInfoData(bei_info_result)

    tumblr_baseurl = "https://api.tumblr.com/v2/blog/"
    tumblr_params = {'blog-identifier': "vinbeigie", 'api':"/posts"}

    bei_post_result = get_data_from_api(tumblr_baseurl,
                                      tumblr_params)
    # Post
    # printPostData(bei_post_result)

    tumblr_baseurl = "https://api.tumblr.com/v2/blog/"
    tumblr_params = {'blog-identifier': "interior-inspire-live.tumblr.com", 'api':"/info"}

    interior_info_result = get_data_from_api(tumblr_baseurl,
                                      tumblr_params)
    # Info
    # printInfoData(interior_info_result)

    tumblr_baseurl = "https://api.tumblr.com/v2/blog/"
    tumblr_params = {'blog-identifier': "interior-inspire-live.tumblr.com", 'api':"/posts"}

    interior_post_result = get_data_from_api(tumblr_baseurl,
                                      tumblr_params)
    # Post
    # printPostData(interior_post_result)

    # =============== Transform Data to Model Instances ===============
    bei_info, bei_posts = generate_model_instances(bei_info_result, bei_post_result)
    interior_info, interior_posts = generate_model_instances(interior_info_result, interior_post_result)

    # =============== DB connection Setup/Insert/Query ===============
    setup_database()
    insertInfo([bei_info, interior_info])
    insertPosts(bei_posts, bei_info.id)
    insertPosts(interior_posts, interior_info.id)

    # =============== Visualize with Data ===============
    total_posts = count_all_posts()

    can_like, can_not_like = find_can_like_in_Post()
    can_reply, can_not_reply = find_can_reply_in_Post()

    photo = count_type_photo()
    html = count_format_html()

    posts_under_bei = count_posts(bei_info.id)
    posts_under_interior = count_posts(interior_info.id)

    # Bar Chart
    bar_chart(["total_posts_number", "posts_number_under_vinbeigie", "posts_number_under_interior","photo_type_posts", "html_format_posts", "posts_that_can_like", "posts_that_can_not_like", "posts_that_can_reply", "posts_that_can_not_reply"], [total_posts, posts_under_bei, posts_under_interior, photo, html, can_like, can_not_like, can_reply, can_not_reply])

    # Generate the Image pdfs
    bei_file_list = []
    for i in range(len(bei_posts)):
        bei_file_list.append(get_image(bei_posts[i], i, "bei"))
    generate_gif(bei_file_list, "bei_posts.gif")

    interior_file_list = []
    for i in range(len(interior_posts)):
        interior_file_list.append(get_image(interior_posts[i], i, "interior"))
    generate_gif(interior_file_list, "interior_posts.gif")
