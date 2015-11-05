## Readme

web2py-liscio is a content management system (CMS) built on the web2py framework

web2py is a free open source full-stack framework for rapid development of fast, scalable, secure and portable database-driven web-based applications.

It is written and programmable in Python. LGPLv3 License

Learn more at http://web2py.com

## Install

1. Simply install web2py from here http://www.web2py.com/init/default/download

2. Run your installation and access the admin panel (default location with rocket server: http://127.0.0.1:8000/admin/default/site)

3. In the right-hand pane, under Upload and install packed application
a. Enter the name of the application you wish to use (use "init" to automatically setup routing)
b. Enter web2py liscio github clone url in the "Or get from URL" field: https://github.com/peregrinius/web2py-liscio.git

## Setup

### Initialise Super Admin (yourself)

..liscio../models/\_db.py

At the end of the db.py file add your desired login details

user1 = db.auth_user.insert(
        password = db.auth_user.password.validate('frosty')[0],
        email = 'jack.frost@gmail.com',
        first_name = 'Jack',
        last_name = 'Frost',
    )
