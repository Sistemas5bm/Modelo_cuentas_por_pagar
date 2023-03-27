# -*- coding:utf-8 -*-
from odoo import fields, models, api

class Impuestos(models.Model):
    _name = "impuestos"
    name = fields.Char(string='Impuesto')
    factor = fields.Float(string='% - $')
    tipo_afectacion = fields.Selection(selection=[('positive','Positivo'),
                                                  ('negative','Negativo')])