"""
    Comments Controller File
"""
from system.core.controller import *

class Comments(Controller):
    def __init__(self, action):
        super(Comments, self).__init__(action)
        self.load_model('Comment')


    def create_comment(self, messageid, userid):
        comment_info = {
            "message_id": messageid,
            "user_id": session['userid'],
            "comment": request.form['comment']
        }
        
        comment_added_status = self.models['Comment'].post_comment(comment_info)

        # If validations fail (comment empty), redirect back to form
        if comment_added_status['status'] == False:
            flash(comment_added_status['error'])
        return redirect ('/users/'+str(userid))

    def destroy_comment(self, user_id, comment_id):
        self.models['Comment'].delete_comment(comment_id)
        return redirect ('/users/'+str(user_id))
