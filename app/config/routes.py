"""
    Routes Configuration File

"""
from system.core.router import routes

routes['default_controller'] = 'Users'
routes['/register'] = 'Users#show_registrationform'
routes['POST']['/users/login'] = 'Users#login'
routes['POST']['/users/register'] = 'Users#register'
routes ['/users/<int:id>'] = 'Users#show'
routes['/users/logoff'] = 'Users#logoff'

routes['POST']['/message/<int:user_id>'] = 'Messages#create_message'
routes['/delete_message/<int:user_id>/<int:message_id>'] = 'Messages#destroy_message'

routes['POST']['/comment/<int:messageid>/<int:userid>'] = 'Comments#create_comment'
routes['/delete_comment/<int:user_id>/<int:comment_id>'] = 'Comments#destroy_comment'


# routes['/books'] = 'Books#index'
# routes['/books/new'] = 'Books#new'
# routes['/books/<int:bookid>'] = 'Books#show'
# routes['POST']['/books/create'] = 'Books#create_book_review'
# routes['POST']['/books/create_review/<int:bookid>'] = 'Books#create_review'
# routes['/books/delete/<int:bookid>/<int:reviewid>'] = 'Books#destroy_review'

