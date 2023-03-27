# -*- coding:utf-8 -*-

from odoo import fields, models, api


class CortesWizard(models.TransientModel):

    _name = "cortes_wizard"

    #_inherit = 'cortes'

    fecha_inicial = fields.Date(string='Fecha inicial')

    fecha_final = fields.Date(string='Fecha final')

    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    cortes_descarga = fields.Boolean(string='Decarga Cortes', default=True)

    type_user_char = fields.Char(string='User')



    def method_a(self):
        self.env['cortes'].download_data()

    def buscarDatosH(self):
        self.env['cortes'].buscarDatos()

    @api.model_create_multi
    def create(self,vals):

        rec = super(CortesWizard,self).create(vals)
        return rec
