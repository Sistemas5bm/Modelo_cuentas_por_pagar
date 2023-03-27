# -- coding:utf-8 --

from odoo import fields, models, api

class OrdenesExtends(models.Model):

    _inherit = 'purchase.order'

    #account_move_rel = fields.Many2many('account.move','purchase_order_account_move_rel_4','account_id','purchase_id',string='Relacion Facturas')

    sale_order_count = fields.Integer(compute='_compute_sale_order_count',string='# of Sales Order', store=True)

    coneccion_factura = fields.One2many('account.move','rel_purchase', string='Relacion', store=True, copy=True)




    @api.onchange('coneccion_factura')
    def clonacion_productos(self):
        for rec in self:
            lista = []
            for line in rec.coneccion_factura:
               fecha = line.date
               if fecha is False:
                   fecha = fields.Date.today()
               for t in line.invoice_line_ids:
                   descripcion = t.name
                   if descripcion == False:
                       descripcion = 'Sin descripcion'
                   id_producto = line.env['product.template'].search([('id', '=', t.product_id.id)]).id
                   print('showme')
                   print(t.product_id)
                   print('id producto', id_producto)


                   vals = (0, 0, {'product_id':id_producto,
                                   'name':descripcion,
                                   'product_qty':t.quantity,
                                   'price_unit':t.price_unit,
                                   'date_planned':fecha,
                                   'product_uom': t.product_uom_id,
                                   'price_subtotal':500
                                   #'acount_tax':t.acount_tax,

                               })
                   print(vals, ' Lista')

                   print(vals)
                   lista.append(vals)
            rec.order_line = [(5, 0, 0)]
            rec.order_line = lista
            rec.amount_total = 5000


    def create(self, variables):
        print('create')
        print(variables)
        return super(OrdenesExtends, self).create(variables)


    def update_all_products(self):
        x_prod = self.env['product.template'].search([])


