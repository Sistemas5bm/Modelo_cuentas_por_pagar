# -*- coding:utf-8 -*-
from odoo import fields, models, api

class FletW(models.TransientModel):
    _name = "fletes_wizard"
    fecha_inicial = fields.Date(string='Fecha inicial',store=True)
    fecha_final = fields.Date(string='Fecha final',store=True)

    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    fletes_descarga = fields.Boolean(string='Descarga Fletes', default=True, )



    def method_a(self):
        self.env['fletes_modelo_tts'].download_data()

    @api.model_create_multi
    def create(self, vals):
        rec = super(FletW, self).create(vals)
        return rec 
