#!/usr/bin/env python                                                                                                                                

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/jhallard/praxyk
## @license MIT


import os, sys, json, requests
import subprocess, argparse, getpass
import datetime as dt

from base import PraxykBase
from user import User


# @info - Main Praxyk class for the API. This class is used to manage one's account and perform 
#           most data-grabbing operations. User's log in through this class (either in the constructor
#          or the login function), then can call the various get_* functions like get_user to get info
#          on their account. To actually create users,`
class Praxyk(PraxykBase) :

    def __init__(self, login=True, email=None, password=None, *args, **kwargs)  :
        super(Praxyk, self).__init__(*args, **kwargs)

        # if they gave the login flag and credentials, go ahead and login
        if login and (self.auth_token or (email and password)) :
            if not self.login(auth_token=self.auth_token, email=email, password=password) :
                sys.stderr.write("Could not Log-In\n")

    # @info - takes either an existing auth_token or an email and password and logs the user
    #           in via the Praxyk api /tokens/ route. Will store the returned user info in
    #           member variables that can be stored easily for later.
    def login(self, auth_token=None, email="", password="") :
        if auth_token :
            payload = {'token' : auth_token}
            results = super(Praxyk, self).get(self.TOKENS_ROUTE, payload)
            if results :
                self.user = results['user']
                self.auth_token = results['token']
                return True
            else :
                sys.stderr.write("Login With Auth-Token Failed.\n")
                return False
        elif email and password :
            payload = {'email' : email, 'password' : password}
            results = super(Praxyk, self).post(self.TOKENS_ROUTE, payload)
            if results :
                self.user = results['user']
                self.auth_token = results['token']
                return True
            return False
        return False

    # @info - returns information on a specific user, as returned through the /users/X route. If no name
    #          is given, the user that was logged in during construction is returned. If  a name is given
    #          that user is grabbed (note only admins can get info on other users)
    def get_user(self, user_id=None) :
        if user_id == None :
            user_id = self.user.get('user_id', {})
        payload = {'token' : self.auth_token}
        response = self.get(self.USERS_ROUTE+str(user_id), payload)
        if response :
            return User(auth_token=self.auth_token, user=self.user, **response['user'])
        return None
        
    def to_dict(self) :
        return {'auth_token' : self.auth_token, 'user' : self.user }
