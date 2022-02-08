# Rest_Auth

Restful Authentication API built-in Flask. It allows to create user record with username, firstname, lastname and password fields.
Plus, login/update/delete operations are also possible.

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

- POST **/api/users/update**

    Update the user credentials.<br>
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

Run `pytest` in the project directory. This will execute api/test_api.py file.

## Notes about this project.
### Time
In total about 6 hours is spent to build this project.

### Design Choices
First of all, we need to store users in a database. Username, firstname, lastname can be stored in the database but not password, for security reasons. 
Instead, we could store hashed password. For this, werkzeug library is used to generate hashed password. 
For a given password; `python`. Hashed password would look something like this; 

    pbkdf2:sha256:260000$82sUQEqVEkCFBmq4$3bcef45684e80be096d8d81bb881a18dcd0b662ac7cd14c55d411b7417200685

If we break apart this long string;
    Method $ Salt $ Hash

Method defines the hashing method. Salt with 16 character provides a unique ID for the hashed password. The rest is hashed result of the password. Salt provides an extra layer that makes release of the passwords much more difficult by attackers. 

Data Model. 

ID | username | firstname | lastname | password_hash

### Nice thing about this implementation
- Password is never stored in the database. This will secure the passwords even if the database is broken by attackers.
- Index on username will speed up the query on data readings. 

### What can be improved
- Appearently, there are better password security hash methods. Argon2 can be implemented to increase the security. 
- Authentication just with a username and password combination might be risky, if one's password is compromised. To reduce this risk, two factor authentication could be implemented to this API. The user then must provide the password, plus a second authentication factor. This could be an access code sent into user's email, phone, or to another authenticator app. 

### The things are missing to make it production-ready
- To be able to handle load on this API, we need to think about scalability. Load balancer will be necessary to spread the load on API web servers.
- Database Servers can be under heavy read/write request if millions of users are operating on it. Plus, database server should never be down. For this, several databases can be used. 
One of them can be dedicated to write action(create - update - delete actions). Other servers can be used to read (for basically checking authorization - login). 
Read servers will be replicated from Write server. If one of those servers is down, then others will be available. There will be no down time.
Mostly active users can be analyzed and they can be placed into Cache. This will speed up their login time. 
- Finally, a cloud environment could be used to provide this API server. 
