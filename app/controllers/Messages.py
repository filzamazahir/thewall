"""
    Messages Controller File
"""
from system.core.controller import *

class Messages(Controller):
    def __init__(self, action):
        super(Messages, self).__init__(action)
        self.load_model('Message')


    def create_message(self, user_id):
        message_info = {
            "user_id_by": session['userid'],
            "user_id_to": user_id,
            "message": request.form['message']
        }
        
        message_posted_status = self.models['Message'].post_message(message_info)

        # If validations fail (message empty), redirect back to form
        if message_posted_status['status'] == False:
            flash(message_posted_status['error'])
        return redirect ('/users/'+str(user_id))

    def destroy_message(self, user_id, message_id):
        self.models['Message'].delete_message(message_id)
        return redirect ('/users/'+str(user_id))


