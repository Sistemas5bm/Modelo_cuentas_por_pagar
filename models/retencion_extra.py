# -*- coding:utf-8 -*-
from odoo import fields, models, api

class Retenciones(models.Model):
    _name = "retenciones"
    name = fields.Many2one('cat_descuentos', string='Retenciones extras')
    importe = fields.Float(string='Importe')
    fletes_rel = fields.Many2one('fletes_modelo_tts')