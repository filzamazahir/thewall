""" 
    Comment Model File
"""
from system.core.model import Model

class Comment(Model):
    def __init__(self):
        super(Comment, self).__init__()

    # Get all comments for a user's messages
    def get_all_comments_for_users_messages (self, user_id):
        query = "SELECT users.id AS comment_userid, users.first_name, users.last_name, messages.id AS comment_msgid, comments.id AS commentid, comments.comment, comments.created_at, comments.updated_at FROM users JOIN comments ON users.id = comments.user_id JOIN messages ON messages.id = comments.message_id WHERE users.id = %s ORDER BY comments.id DESC"
        comments_for_messages = self.db.query_db(query, [user_id])
        return comments_for_messages


    # Post a comment
    def post_comment (self, comment_info):
        message_id = comment_info['message_id']
        user_id = comment_info['user_id']
        comment = comment_info['comment']

        if len(request.form['comment']) == 0:
            return {"status" : False, "error": "Comment cannot be empty."}


        insert_comment_query = "INSERT INTO comments (message_id, user_id, comment, created_at, updated_at) VALUES(%s, %s, %s, NOW(), NOW())"
        data = [message_id, user_id, comment]
        self.db.query_db(insert_comment_query, data)

        return {"status": True}


    # Delete a comment
    def delete_comment(self, comment_id):
        delete_comment_query = "DELETE FROM comments WHERE id = %s"
        self.db.query_db(delete_comment_query, [comment_id])
        return

    """
    Below is an example of a model method that queries the database for all users in a fictitious application

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """

    """
    If you have enabled the ORM you have access to typical ORM style methods.
    See the SQLAlchemy Documentation for more information on what types of commands you can run.
    """
