# Technical Interview Project

The purpose here is two-fold:

1) Assess your skills in setting up and running a Django project, given a README.

2) Your ability to add a simple page to the application.


Approach this project as if it were handed to you to maintain.  You have full ownership of
the naming and approach.  Your first task is to complete an unfinished feature.  Namely,
retrieve an image URL from a Nasa API and render it to a web page in the app.

There are optional steps, but they're only there if you blow through the two required
steps and want to continue with the exercise.  They are *not required*.


## Setup

1) Clone the repository

2) Create a Python 3.9+ virtual environment and install this app.

3) Run migrations.

4) Run the local development server and view the homepage on the localhost.


## Implement the APOD API

1) Open src/outside/nasa/api.py and implement a method to call the NASA APOD API.

2) Test the API from a Python shell.


## Implement a new page to display the APOD

1) Define a new URL, view, and template to display the APOD.

2) View the URL in a browser.


## Optional Steps

* Implement a Form to capture a date (YYYY-mm-dd), selecting a specific APOD.
* Implement a model, keyed on Date, to cache / retain the data from the API.
* Implement a unit test to test the Form behavior or View behavior.


## Docker

A Dockerfile has been included if that proves to be helpful in your local environment.