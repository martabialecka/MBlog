# MBlog

Before starting MBlog, set environment variables:

```
SECRET_KEY
ADMIN_USERNAME
ADMIN_PASSWORD
```

To run the "MBlog", install python 3.x and execute

```
pip install -r requirements.txt
```

From `MBlog` directory execute

```
flask db init
flask db migrate
flask db upgrade
flask run
```
