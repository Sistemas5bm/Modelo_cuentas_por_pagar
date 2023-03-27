# -*- coding:utf-8 -*-

from odoo import fields, models, api

class CatalogoDescuentos(models.Model):
    _name = "cat_descuentos"
    _sql_constraints = [('name_unique', 'UNIQUE(name)',('El registro ya existe'))]
    name = fields.Char(string='Retenciones extras')
