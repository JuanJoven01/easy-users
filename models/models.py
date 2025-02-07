from odoo import models, fields, exceptions
import random
import string


class EasyUserActivationCode(models.Model):
    _name = 'easy_user.activation_code'
    _description = 'User Activation Code'

    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade', unique=True)
    activation_code = fields.Char(string='Activation Code', required=True, default=lambda self: self._generate_code())
