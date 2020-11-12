# Django with Google Dialogflow

[![Python Version](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.1-brightgreen.svg)](https://djangoproject.com)

This website is build for a customer service role-play training.

Follow by this document you will:

1. Create a Mega Dialogflow agent
2. Create a Django website contain two applications:
    - Checkin
    - Checkout
3. Create a Database for recording the role-play result include:
    - CheckinRecord
    - CheckoutRecord
    - CheckinDialogRecord
    - CheckoutDialogRecord
    - and other sub-tasks in each record


## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone ...
cd HotelChatBot
```

---

### Prepare for Dialogflow

#### Creat your Dialogflow agent

Creat three agents in [dialogflow console](https://dialogflow.cloud.google.com/) :
1. Checkin agent (*files/backup/...latest/checkin/HotelCustomerCheckin.zip*)
2. Checkout agent (*files/backup/...latest/checkout/HotelCustomerCheckout.zip*)
3. Mega agent (*files/backup/...latest/mega/HotelCustomer.zip*)

Get the service private kay:
1. Follow [dialogflow document](https://cloud.google.com/dialogflow/es/docs/agents-mega) to get the private key (json file) 
2. Put the private key into *HotelChatBot/google.service.account.key/*
3. Change the variables in config file (*HotelChatBot/config.txt*) 
    - PROJECT_ID
    - CHECKIN_PROJECT_ID
    - CHECKOUT_PROJECT_ID
    - PRIVATE_KEY_PATH
    

---

### Develop Local Django Server

#### Make Virtualenv
On Linux:

```bash
python3 -m venv venv
source ./venv/bin/activate
```

On Windows:
```bash
python -m venv venv
./venv/Scripts/activate.bat
```

Install the requirements:
```
pip install -r requirements.txt
```

#### Build Database

Move to the folder where manage.py is:
```bash
cd HotelChatBot
```

Apply the migrations
```bash
python manage.py migrate
```

Create superuser:
```bash
python manage.py createsuperuser
```

#### Finally, run the development server:
```bash
cd HotelChatBot
python manage.py runserver
```
or
```bash
python main.py
```
The project will be available at **127.0.0.1:8000**.

---

### More

#### For static url setting
Please refer the end of the setting.py

#### For production:

1. For security, you should create your own Django project from zero to get your own **SECRET_KEY** in setting.py
2. Set **DEBUGE=False** in setting.py
3. Follow the [document](https://docs.djangoproject.com/en/3.1/howto/static-files/deployment/) for serving static files