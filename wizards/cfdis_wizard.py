# -*- coding:utf-8 -*-

from odoo import fields, models, api


class CfdisWizard(models.TransientModel):


    _name = "cfdis_wizard"

    #_inherit = 'account.move'

    fecha_inicial = fields.Date(string='Fecha Inicial')

    fecha_final = fields.Date(string='Fecha Final')

    #current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    cdis_descarga = fields.Boolean(string='Descarga Fletes', default=True, )



    def method_a(self):
        self.env['account.move'].download_data()

    @api.model_create_multi
    def create(self,vals):

        rec = super(CfdisWizard,self).create(vals)
        return rec
