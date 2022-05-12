from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'library.order'
    _description = 'New Order'

    order_book_detail = fields.One2many(
        comodel_name='library.order_book_detail',
        inverse_name='order_id',
        string='Order Book'
    )

    name = fields.Char(string='Order Code', required=True)
    order_date = fields.Datetime('Order Date', default=fields.Datetime.now())
    customer = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        domain=[('is_customernya', '=', True)], store=True)
    total = fields.Integer(compute='_compute_total',
                           string='Total', store=True)

    @api.depends('order_book_detail')
    def _compute_total(self):
        for record in self:
            record.total = sum(self.env['library.order_book_detail'].search(
                [('order_id', '=', record.id)]).mapped('price'))


class OrderBookDetail(models.Model):
    _name = 'library.order_book_detail'
    _description = 'Order Book Detail'

    order_id = fields.Many2one(
        comodel_name='library.order', string='Book Order')
    book_id = fields.Many2one(comodel_name='library.book', string='Book')
    name = fields.Char(string='Name')
    single_price = fields.Integer(
        compute='_compute_single_price', string='Single Price')
    qty = fields.Integer(string='Quantity')
    price = fields.Integer(compute='_compute_price', string='price')

    @api.depends('book_id')
    def _compute_single_price(self):
        for record in self:
            record.single_price = record.book_id.price

    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            stock = self.env['library.book'].search(
                [('stock', '<', record.qty), ('id', '=', record.id)])
            if stock:
                raise ValidationError("Not Enough Stock")

    @api.depends('single_price', 'qty')
    def _compute_price(self):
        for record in self:
            record.price = record.single_price * record.qty

    @api.model
    def create(self, vals):
        record = super(OrderBookDetail, self).create(vals)
        if record.qty:
            self.env['library.book'].search([('id', '=', record.book_id.id)]).write({
                'stock': record.book_id.stock-record.qty})
            return record
