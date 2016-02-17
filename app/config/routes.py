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
routes['/users/edit/<int:user_id>'] = 'Users#show_edit'
routes['POST']['/users/update_description/<int:user_id>'] = 'Users#update_description'
routes['POST']['/users/update_info/<int:user_id>'] = 'Users#update_info'
routes['POST']['/users/update_password/<int:user_id>'] = 'Users#update_password'
routes['/users/delete/<int:user_id>'] = 'Users#delete_user'



routes['POST']['/message/<int:user_id>'] = 'Messages#create_message'
routes['/delete_message/<int:user_id>/<int:message_id>'] = 'Messages#destroy_message'

routes['POST']['/comment/<int:messageid>/<int:userid>'] = 'Comments#create_comment'
routes['/delete_comment/<int:user_id>/<int:comment_id>'] = 'Comments#destroy_comment'

