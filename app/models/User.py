""" 
    User Model File
"""
from system.core.model import Model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$') 


class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def login_user(self, login_info):
        email = login_info['email']
        password = login_info['password']
        error_dict = {}
        error = False

        #Check if both fields are inputted
        if len(email) ==0 or len(password) == 0:
            error_dict ['login'] = "All fields are required! Please try again."
            return {"status": False, "error_dict": error_dict}

        current_user = self.db.query_db("SELECT * FROM users WHERE email = %s", [email]) 
        
        #Validate email
        if not EMAIL_REGEX.match(email): 
            error_dict ['login'] = "Invalid email address"
            error = True

        #Check if user exists with the given email and password        
        elif len(current_user) == 0:
            error_dict['login'] = "Wrong email or password entered. Please try again"
            error = True

        elif not self.bcrypt.check_password_hash(current_user[0]['password'], password):
            error_dict['login'] = "Wrong email or password entered. Please try again"
            error = True

        if error == True: 
            return {"status":False, "error_dict": error_dict}

        #User has been authenticated, log the user in
        id_col = self.db.query_db("SELECT id FROM users WHERE email = %s", [email])
        loggedin_user_id = id_col[0]['id']

        return {"status": True, "id":loggedin_user_id}

    def register(self, register_info):

        fname = str(register_info['fname'])
        lname = str(register_info['lname'])
        email = register_info['email']
        password = register_info['password']
        conf_password = register_info['conf_password']
        userlevel = 0

        error_dict = {}
        error = False

        #Check if all fields are inputted, return right away if any field is missing
        if len(fname)==0 or len(lname) ==0 or len(email) ==0 or len(password)==0 or len(conf_password)==0:
            error_dict['register'] = "All fields are required! Please try again."
            error = True
            return {"status" : False, "error_dict": error_dict}

        #Check first name is atleast 2 chars
        if len(fname) < 2:
            error_dict['fname'] = "First Name must be atleast 2 characters. Please try again."
            error = True

        elif str.isalpha(fname)==False:
            error_dict['fname'] = "Names must not contain numbers. Please try again."
            error = True

        #Check last name is atleast 2 chars & all characters
        if len(lname) < 2:
            error_dict['lname'] = "Last name must be atleast 2 characters. Please try again."
            error = True

        elif str.isalpha(lname)==False:
            error_dict['lname'] = "Last name must not contain numbers. Please try again."
            error = True

        #Validate email
        if not EMAIL_REGEX.match(email):
            error_dict['email_register'] = "Invalid email address."
            error = True

        #Check if email already exists in database
        query = "SELECT * FROM users WHERE email = %s"
        data = [email]
        user = self.db.query_db(query, data)
        if len(user) > 0:
            error_dict['email_register'] = "Email address already exists. Please try registering with another email, or login using this email."
            error = True

        #Validate password
        num_in_pass = False
        upper_in_pass = False
        for char in str(password):
            if str.isupper(char):
                upper_in_pass = True
            if str.isdigit(char):
                num_in_pass = True

        if len(password) < 8:
            error_dict['password_register'] = "Password must be 8 characters."
            error = True

        elif password != conf_password:
            error_dict['password_register'] = "Passwords do not match."
            error = True

        elif num_in_pass == False or upper_in_pass == False:
            error_dict['password_register'] = "Please use atleast 1 uppercase letter and 1 numeric value in your password."
            error = True


        #Check if there were any errors in the previous validation process
        if error == True:
            return {"status" : False, "error_dict": error_dict}

        #Add user to database if no errors then return the id for login purposes
        pw_hash = self.bcrypt.generate_password_hash(password)
        users = self.get_all_users()

        # Make the user an admin if no other users exist
        if len(users) == 0 :
            userlevel = 1

        insert_query = "INSERT INTO users (first_name, last_name, email, password, user_level, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
        data = [fname, lname, email, pw_hash, userlevel]
        self.db.query_db(insert_query, data)

        last_id_col = self.db.query_db("SELECT id FROM users ORDER BY id DESC LIMIT 1")
        last_user_id = last_id_col[0]['id']

        return {"status": True, "id":last_user_id}

    def update_info (self, info):
        firstname = str(info['firstname'])
        lastname = str(info['lastname'])
        email = info['email']

        error_dict = {}
        error = False

        #Check if all fields are inputted, return right away if any field is missing
        if len(fname)==0 or len(lname) ==0 or len(email) ==0 or len(password)==0 or len(conf_password)==0:
            error_dict['register'] = "All fields are required! Please try again."
            error = True
            return {"status" : False, "error_dict": error_dict}

        #Check first name is atleast 2 chars
        if len(fname) < 2:
            error_dict['fname'] = "First Name must be atleast 2 characters. Please try again."
            error = True

        elif str.isalpha(fname)==False:
            error_dict['fname'] = "Names must not contain numbers. Please try again."
            error = True

        #Check last name is atleast 2 chars & all characters
        if len(lname) < 2:
            error_dict['lname'] = "Last name must be atleast 2 characters. Please try again."
            error = True

        elif str.isalpha(lname)==False:
            error_dict['lname'] = "Last name must not contain numbers. Please try again."
            error = True

        #Validate email
        if not EMAIL_REGEX.match(email):
            error_dict['email_register'] = "Invalid email address."
            error = True

        #Check if email already exists in database
        query = "SELECT * FROM users WHERE email = %s"
        data = [email]
        user = self.db.query_db(query, data)
        if len(user) > 0:
            error_dict['email_register'] = "Email address already exists. Please try registering with another email, or login using this email."
            error = True

        if error == True:
            return {"status" : False, "error_dict": error_dict}

        update_query = "UPDATE users (first_name, last_name, email, updated_at) VALUES (%s, %s, %s, NOW())"
        data = [firstname, lastname, email]
        self.db.query_db(update_query, data)

        return {"status": True, "success": "Your basic information was updated successfully!"}


    def update_password(self, password_to_update):
        password = password_to_update['password']
        conf_password = password_to_update['conf_password']

        #Validate password
        num_in_pass = False
        upper_in_pass = False
        for char in str(password):
            if str.isupper(char):
                upper_in_pass = True
            if str.isdigit(char):
                num_in_pass = True

        if len(password) < 8:
            error_dict['password_register'] = "Password must be 8 characters."
            error = True

        elif password != conf_password:
            error_dict['password_register'] = "Passwords do not match."
            error = True

        elif num_in_pass == False or upper_in_pass == False:
            error_dict['password_register'] = "Please use atleast 1 uppercase letter and 1 numeric value in your password."
            error = True


        #Check if there were any errors in the previous validation process
        if error == True:
            return {"status" : False, "error_dict": error_dict}

        pw_hash = self.bcrypt.generate_password_hash(password)
        update_query = "UPDATE users (password, updated_at) VALUES (%s, NOW())"
        self.db.query_db(update_query, [pw_hash])

        return {"status": True, "success": "Your password was changed successfully!"}


    def update_description(self, description):
        update_query = "UPDATE users (description, updated_at) VALUES (%s, NOW())"
        self.db.query_db(update_query, [description])
        return {"status": True, "success": "Your description was updated successfully!"}

    def update_user_level(self, user_level):
        update_query = "UPDATE users (user_level, updated_at) VALUES (%s, NOW())"
        self.db.query_db(update_query, [user_level])
        return {"status": True, "success": "User level was updated successfully!"}


    def get_a_user (self, id):
        query = "SELECT * FROM users WHERE id = %s"
        data = [id]
        user = self.db.query_db(query, data)
        return user[0]

    def get_all_users (self):
        users = self.db.query_db("SELECT * FROM USERS")
        return users

    def delete_user (self, id):
        delete_user_query = "DELETE FROM users WHERE id = %s"
        self.db.query_db(delete_user_query, [id])
        return



    