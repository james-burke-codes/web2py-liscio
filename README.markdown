## Readme

web2py-liscio is a content management system (CMS) built on the web2py framework

web2py is a free open source full-stack framework for rapid development of fast, scalable, secure and portable database-driven web-based applications.

It is written and programmable in Python. LGPLv3 License

Learn more at http://web2py.com

## Setup

### Initialise Super Admin (yourself)

/applications/init/models/\_db.py

At the end of the db.py file add your desired login details

user1 = db.auth_user.insert(
        password = db.auth_user.password.validate('frosty')[0],
        email = 'jack.frost@gmail.com',
        first_name = 'Jack',
        last_name = 'Frost',
    )
