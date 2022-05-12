from odoo import api, fields, models


class Book(models.Model):
    _name = 'library.book'
    _description = 'Book Model'

    name = fields.Char(string='Title', required=True)
    genre = fields.Char(string='Genre', required=True)
    release_year = fields.Datetime('Release Year', required=True)
    pages_count = fields.Integer(string='Pages', required=True)
    price = fields.Integer(string='Price', required=True)
    stock = fields.Integer(string='Stock', required=True)
    publisher = fields.Many2one(
        comodel_name='res.partner',
        string='Publisher',
        domain=[('is_book_publisher', '=', True)], store=True)
    author = fields.Many2one(
        comodel_name='res.partner',
        string='Author',
        domain=[('is_book_author', '=', True)], store=True)
