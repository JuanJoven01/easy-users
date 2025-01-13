from odoo import models, fields, exceptions
import random
import string


class EasyUserActivationCode(models.Model):
    _name = 'easy.user.activation.code'
    _description = 'User Activation Code'

    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade', unique=True)
    activation_code = fields.Char(string='Activation Code', required=True, default=lambda self: self._generate_code())

    @staticmethod
    def _generate_code(length=6):
        """
        Generate a random alphanumeric code of the given length.
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def _verify_code(self, code):
        """
        Verify the activation code and activate the user if correct.
        """
        if self.activation_code != code:
            return False

        # Activate the user
        self.user_id.active = True
        # Optionally, delete the activation record after verification
        self.unlink()
        return True
