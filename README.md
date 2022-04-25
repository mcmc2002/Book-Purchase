# Take home project
This is a simple e-commerce application that a customer can use to purchase a book, but it's missing the payments functionality — your goal is to integrate Stripe to get this application running!

## Candidate instructions
You'll receive these in email.

## Application overview
This is a simple e-commerce application that a customer can use to purchase a book using Stripe payment functionality. This take home assignment is written in Python with Flask framework.

To simplify this project, no database was used here. Instead `app.py` includes a simple case statement to read the GET params for `item`. 

To get started, clone the repository and run pip3 to install dependencies:

```
git clone https://github.com/mcmc2002/Book-Purchase && cd sa-takehome-project-python
pip3 install -r requirements.txt
```

Modify the `.env` using your Stripe account's test API keys.

Then run the application locally:

```
flask run
```

Navigate to [http://localhost:5000](http://localhost:5000) to view the index page.
