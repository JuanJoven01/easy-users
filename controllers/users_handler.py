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
                'error': 'Data requerida no completa',
                'message': 'Los campos email, name y password son obligatorios'
            }

            # Create the user
            user = request.env['res.users'].sudo().create({
                'name': name,
                'login': email,
                'password': password,
                'groups_id': [(4, 12)],  # Add the user at the group ID 12 (easy_apps), the code 4 ensure do not remove any register
            })

            return {
                'success': True,
                'message': 'Usuario creado exitosamente',
                'user_id': user.id,
            }
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Hubo un problema al crear el usuario'
            }
