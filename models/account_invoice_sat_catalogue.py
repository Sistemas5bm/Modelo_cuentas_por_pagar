# -*- coding:utf-8 -*-

from odoo import fields, models, api

class CatalogueSat(models.Model):

    _name = 'stock_sat_catalogue'

    name = fields.Char(string='Clave Sat')

    description = fields.Char(string = 'Descripción')

    products_products_rel = fields.Many2one(comodel_name='product.template',string='Relacion de productos')

    status = fields.Char(string='Estatus')




