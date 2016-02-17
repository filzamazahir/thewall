""" 
    Message Model File
"""
from system.core.model import Model

class Message(Model):
    def __init__(self):
        super(Message, self).__init__()

    # Get all messages for a user
    def get_all_messages_for_user(self, user_id):
        query = "SELECT users.id AS userid, users.first_name, users.last_name, messages.id AS msgid, messages.user_id_by AS msgbyuser, messages.message, messages.created_at, messages.updated_at FROM users JOIN messages ON users.id = messages.user_id_by WHERE messages.user_id_to = %s ORDER BY messages.id DESC"
        messages = self.db.query_db(query, [user_id])
        return messages

    # Post a message
    def post_message (self, message_info):
        user_id_by = message_info['user_id_by']
        user_id_to = message_info['user_id_to']
        message = message_info['message']

        if len(message) == 0:
            return {"status" : False, "error": "Comment cannot be empty."}

        insert_message_query = "INSERT INTO messages (user_id_by, user_id_to, message, created_at, updated_at) VALUES (%s, %s, %s, NOW(),NOW())"
        data = [user_id_by, user_id_to, message]
        self.db.query_db(insert_message_query, data)

        return {"status": True}


    # Delete a message
    def delete_message(self, message_id):
        delete_message_query = "DELETE FROM messages WHERE id = %s"
        self.db.query_db(delete_message_query, [message_id])
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
