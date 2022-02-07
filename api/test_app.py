from requests.auth import _basic_auth_str
from api import app
import os
from flask import Flask, abort, request, jsonify, g, url_for, json
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

class TestClass:
    def testCreateNewUser(self):        
        response = app.test_client().post(
                        '/api/users',
                        data=json.dumps({'username': "enis1",
                                         'firstname': "enis",
                                         'lastname': "arik",
                                         'password': "go"}),
                        content_type='application/json')

        assert response.status_code == 201
    
    def testCreateSameUser(self):
        response = app.test_client().post(
                        '/api/users',
                        data=json.dumps({'username': "enis1",
                                         'firstname': "enis",
                                         'lastname': "arik",
                                         'password': "go"}),
                        content_type='application/json')

        assert response.status_code == 400

    def testGetResource(self):
        headers = {'Authorization': _basic_auth_str("enis1", "go")}
        response = app.test_client().get(
                '/api/resource',
                headers=headers)

        assert response.status_code == 201

    def testUpdateUser(self):        
        headers = {'Authorization': _basic_auth_str("enis1", "go")}
        response = app.test_client().post(
                        '/api/users/update',
                        headers=headers,
                        data=json.dumps({'username': "john2"}),
                        content_type='application/json')
        
        assert response.status_code == 201
  
    def testDeleteUser(self):
        headers = {'Authorization': _basic_auth_str("john2", "go")}
        response = app.test_client().get(
                '/api/users/delete',
                headers=headers)

        assert response.status_code == 201
