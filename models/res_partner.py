from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    is_book_author = fields.Boolean(string='Book Author', default=False)
    is_book_publisher = fields.Boolean(string='Book Publisher', default=False)
