"""
    Users Controller File
"""
from system.core.controller import *
    
class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Message')
        self.load_model('Comment')

    def index(self):
        # Display log in page if not logged in
        if not session.get('userid') or not session['userid']: #second one means if session['userid'] = False
            return self.load_view('users/index.html')

        # If logged in already, redirect to dashboard (according to admin level)
        users = self.models['User'].get_all_users()
        current_user = self.models['User'].get_a_user(session['userid'])
        return self.load_view('/users/dashboard.html', current_user = current_user, users = users)

    # routes  ['POST']  ['/users/login']
    def login(self):

        login_info = {
            "email": request.form['email'], 
            "password": request.form['password']
        }
        login_status = self.models['User'].login_user(login_info)

        #Flash errors if login fails
        if login_status['status'] == False:
            error_dict = login_status['error_dict']
            for key,val in error_dict.items():
                flash(val, key)

        #Log in the user if user is authenticated
        if login_status['status'] == True:
            session['userid'] = login_status['id']

        return redirect ('/')


    # routes ['/register']
    def show_registrationform(self):
        return self.load_view('users/register.html')

    # routes ['POST'] ['/users/register']
    def register(self):
        register_info = {
            "fname": request.form['fname'],
            "lname": request.form['lname'],
            "email": request.form['email'], 
            "password": request.form['password'],
            "conf_password": request.form['conf_password']
        }

        register_status = self.models['User'].register(register_info)

        #Flash errors if registration fails
        if register_status['status'] == False:
            error_dict = register_status['error_dict']
            for key,val in error_dict.items():
                flash(val, key)
            return redirect ('/register')

        #Log in the user if user is registered successfully
        else:
            session['userid'] = register_status['id']
            return redirect ('/')

    # route ['/users/logoff']
    def logoff(self):
        session['userid'] = False
        return redirect ('/')


    #route ['/users/id']
    def show(self, id):
        current_user = self.models['User'].get_a_user(session['userid'])
        userprofile = self.models['User'].get_a_user(id)
        messages = self.models['Message'].get_all_messages_for_user(id)
        comments_messages_users = self.models['Comment'].get_all_comments_for_users_messages(id)
        return self.load_view('messages/wall.html', current_user = current_user, userprofile = userprofile, messages = messages, comments_messages_users = comments_messages_users) 
    
    # routes ['/users/edit/<int:user_id>'] 
    def show_edit (self, user_id):
        user_to_edit = self.models['User'].get_a_user(user_id)
        return self.load_view('users/edit_profile.html', user_to_edit = user_to_edit)

    # route ['POST'] ['/users/update_description/<int:user_id>']
    def update_description (self, user_id):
        description = request.form['description']

        return

    # route ['POST'] ['/users/update_info/<int:user_id>']
    def update_info (self, user_id):
        info = {
            "firstname": request.form['firstname'],
            "lastname": request.form['lastname'],
            "email": request.form['email']
        }
        update_status = self.models['User'].update_info(info)

        if update_status['status'] == False:
            error_dict = update_status['error_dict']
            for key,val in error_dict.items():
                flash(val, key)
            return redirect ('/users/edit/'+str(user_id))

        return redirect ('/')

    # route ['POST'] ['/users/update_password/<int:user_id>']
    def update_password (self, user_id):
        password_to_update = {
            "password": request.form['password'],
            "conf_password": request.form['conf_password']
        }

        return


    # routes ['/users/delete/<int:user_id>']
    def delete_user (self, user_id):
        self.models['User'].delete_user(user_id)
        return redirect ('/')

