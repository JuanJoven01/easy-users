from odoo import http
from odoo.http import request
class EasyUsers(http.Controller):
    @http.route('/api/easy_apps/users/new_user', methods=['POST'], type='jsonrpc', auth='public')
    def create_easy_user(self, **kwargs):
        """
        Endpoint to create users on the group 'easy_apps'.
        """
        try:
            # get the requested data
            email = kwargs.get('email')
            name = kwargs.get('user_name')
            password = kwargs.get('password')

            if not email or not name or not password:
                return {
                'error': 'Insufficient data',
                'message': 'Fields email, name and password are required'
                }
            #verify if email already exist
            user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            if user:
                return {
                'error': 'Repeated email',
                'message': 'The Email is already registred'
                }
            # Create the user
            new_user = request.env['res.users'].sudo().create({
                'name': name,
                'login': email,
                'password': password,
                'active': False, # default until activate the email
                'groups_id': [(4, 12)],  # Add the user at the group ID 12 (easy_apps), the code 4 ensure do not remove any register
            })

            return {
                'success': True,
                'message': 'Usuario creado exitosamente',
                'user_id': new_user.id,
            }
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Hubo un problema al crear el usuario'
            }
        oo
