[![Build Status](https://travis-ci.org/daisymacharia/Bucketlist-API.svg?branch=ft-functionality-148194901)](https://travis-ci.org/daisymacharia/Bucketlist-API)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/142345aea68a42008ae3a7ee5fd63e9f)](https://www.codacy.com/app/daisymacharia/Bucketlist-API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=daisymacharia/Bucketlist-API&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/daisymacharia/Bucketlist-API/badge.svg?branch=ft-functionality-148194901)](https://coveralls.io/github/daisymacharia/Bucketlist-API?branch=ft-functionality-148194901)
# Bucketlist-API

Online Bucket List service using Flask.(RESTful API)

The building blocks are:
  * Flask Restful
  * SQLalchemy
  * Postgres (Database)

EndPoint | Functionality
------------ | -------------
POST /auth/login | Logs a user in and generates a unique token
POST /auth/register | Register a user
POST /bucketlists/  | Create a new bucket list
GET /bucketlists/ | List all the created bucket lists that belongs to the logged in user
GET /bucketlists/{d}/ | Get single bucket list
PUT /bucketlists/{id}/ | Updates the specified bucket list
DELETE /bucketlists/{id}/ | Delete the specified bucket list
POST /bucketlists/{id}/items/ | Create a new item in bucket list
PUT /bucketlists/{id}/items/{item_id} | Update a bucket list item
DELETE /bucketlists/{id}/items/{item_id} | Delete an item in a bucket list

## INSTALLATION

These are the basic steps to install and run the application locally.

* prepare directory for project code and virtualenv:

      $ mkdir -p ~/bucketlist_api

      $ cd ~/bucketlist_api
* prepare virtual environment
  * (with virtualenv you get pip, we'll use it soon to install requirements):

      $ virtualenv --python=python3 bucketlist

      $ source bucketlist/bin/activate
  * Or an even better method would be to use virtualenv wrapper
      $ mkvirtualenv bucketlist

      $ workon bucketlist (to activate and start using your virtual environment)

* Clone the application:

      $ git clone https://github.com/daisymacharia/Bucketlist-API.git

* install requirements into virtualenv:

      $ pip install -r Bucketlist-API/requirements.txt
      $ git checkout develop

 * Start the application. This will initialize the database and create tables.
       $ python manage.py db init
       $ python manage.py db migrate
       $ python manage.py db upgrade

 * Run server

       $ flask run
 ## Screenshots
 * POST method for registering a new user
![alt text](screenshots/reg.png)

 * POST method to login an existing user, A token is issued that enables the user access to private endpoints
![alt text](screenshots/login.png)
 
 * POST method for creation of a new bucketlist
![alt text](screenshots/create_bucketlist.png)

* GET method to get bucketlist by id
![alt text](screenshots/get_bucketlist.png)

 * POST method for update of a bucketlist item
 ![alt text](screenshots/update_items.png)
 
 * GET method to get updated bucketlist item
  ![alt text](screenshots/get_updated_items.png)

 * Get the app [here](https://bucketlists-staging.herokuapp.com/apidocs/)
