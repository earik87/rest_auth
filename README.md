# Rest_Auth

Restful Authentication API built-in Flask. It allows to create user record with username, firstname, lastname and password fields.
Plus, login/update/delete operations are also possible for users.

## Installation

After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv venv
    $ venv\Scripts\activate
    (venv) $ pip install -r requirements.txt

## Running

To run the server use the following command:

    (venv) $ python api.py

Then, from a different terminal window you can send requests.

## API Documentation

- POST **/api/users**

    Register a new user.<br>
    The body must contain a JSON object that defines `username`, `firstname`, `lastname` and `password` fields.<br>
    On success, a status code 201 is returned. The body of the response contains a JSON object with the newly added user.
    Notes:
    - The password is hashed before it is stored in the database. Once hashed, the original password is discarded.

- GET **/api/resource**

    Return a protected resource. This checks if user is logged in.<br>This request must be authenticated using a HTTP Basic Authentication header. Username and password need to be provided.<br>
    On success, status code 201 and a JSON object with data for the authenticated user is returned.<br>

- GET **/api/users/update**

    Return the updated user credentials.<br>
    This request must be authenticated using a HTTP Basic Authentication header. Username and password need to be provided.<br>
    On success, status code 201 and a JSON object with data for the updated user is returned.<br>

- GET **/api/users/delete**
  
    Delete the user.
    This request must be authenticated using a HTTP Basic Authentication header. Username and password need to be provided.<br>
    On success, a status code 201 is returned.<br>

## Examples

The following `curl` command registers a new user with username `enis87` and password `python`:

```
$ curl -i -X POST -H "Content-Type: application/json" -d '{\"username\":\"enis87\",\"firstname\":\"enis\",\"lastname\":\"arik\",\"password\":\"python\"}' http://127.0.0.1:5000/api/users

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 74
Server: Werkzeug/1.0.1 Python/3.10.0
Date: Sun, 06 Feb 2022 17:55:56 GMT

{
  "firstname": "enis",
  "lastname": "arik",
  "username": "enis87"
}
```

These credentials can now be used to access protected resources:

```
$ curl -u enis87:python -i -X GET http://127.0.0.1:5000/api/resource
HTTP/1.0 201 OK
Content-Type: application/json
Content-Length: 31
Server: Werkzeug/1.0.1 Python/3.10.0
Date: Sun, 06 Feb 2022 17:56:34 GMT

{
  "data": "Hello, enis87!"
}
```

Using the wrong credentials leads the request to be refused:

```
$ curl -u enis87:java -i -X GET http://127.0.0.1:5000/api/resource
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/html; charset=utf-8
Content-Length: 19
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/1.0.1 Python/3.10.0
Date: Sun, 06 Feb 2022 17:58:31 GMT

Unauthorized Access
```

Now, let's update the user password from "python" to "go":

```
$ curl -u enis87:python -i -X POST -H "Content-Type: application/json" -d '{\"password\":\"go\"}' http://127.0.0.1:5000/api/users/update
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 106
Server: Werkzeug/1.0.1 Python/3.10.0
Date: Sun, 06 Feb 2022 17:59:42 GMT

{
  "data operation:": "update",
  "firstname": "enis",
  "lastname": "arik",
  "username": "enis87"
}
```

The following command deletes the user "enis87":

```
$ curl -u enis87:go -i -X GET http://127.0.0.1:5000/api/users/delete 
HTTP/1.0 201 CREATED
Content-Type: text/html; charset=utf-8
Content-Length: 20
Server: Werkzeug/1.0.1 Python/3.10.0
Date: Sun, 06 Feb 2022 18:00:10 GMT

The user is deleted!
```

## Testing

Run `pytest` in the project directory. This will execute api/test_app.py file.
