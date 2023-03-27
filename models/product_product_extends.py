# -*- coding:utf-8 -*-widgets manymanytags

from odoo import fields, models, api

class ProductExtends(models.Model):

    _inherit = 'product.template'

    product_sat_catalogue = fields.One2many('stock_sat_catalogue','products_products_rel',string='Clave Sat')

    clave_prod_sat = fields.Char(string='Clave Producto Sat')

    clave_prod_sat_desc = fields.Char(string='Clave Producto Sat Desc')

    clave_unidad_sat = fields.Char(string='Clave Unidad Sat')

    clave_unidad_desc = fields.Char(string='Clave Unidad Sat Desc')

    unidad = fields.Char(string='Unidad')

    check_metodo_descarga_masiva = fields.Char(string='Check DM')


