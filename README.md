# Chronicles
IMG Summer Project

## Set up instructions
* Clone the repository
* Set up a virutal environment and activate
* Use the following comand to install all the necessary dependencies:
  ``` 
  pip install -r requirements.txt 
  ```
* Install docker
* Use the following command to set up a redis backing store:
  ```
  docker run -p 6379:6379 -d redis:5
  ```
* Create a MySQL databse named ```Chronicles```
* Make an environment file named ```.env``` and store the following credentials in that file:
  ```
  DEBUG = 0
  SECRET_KEY = *your_secret_key*
  MYSQL_PASSWORD = *Password to access MySQL database*
  
  CLIENT_ID = *OAuth Client ID*
  CLIENT_SECRET = *OAuth Client Secret*
  
  SENDER_EMAIL = *Email-ID for the Email Wizard*
  SENDER_PASSWORD = *Password for the above Email-ID*
  ```
* Run the following command to start backend server:
  ```
  daphne -p 8000 chronicles.asgi:application
  ```
