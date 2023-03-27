# -*- coding:utf-8 -*-

from odoo import fields, models, api
from datetime import date

class IneSat(models.Model):
    _name = 'ine_sat'

    name = fields.Char(string='Nombre INE',default='INE')

    ine = fields.Binary(string='Archivo de INE')

    ine_filename = fields.Char(string='Nombre de archivo')

    ine_partner_rel = fields.Many2one(string='',comodel_name='res.partner')

    fecha_vencimiento = fields.Date(string='Fecha Vencimiento')

    estatus = fields.Char(string='Vigencia',compute='vigencia',store=False)


    def vigencia(self):
        for l in self:
            var_control_date = l.fecha_vencimiento
            var_control_date_char = 0
            if var_control_date == False:
                var_control_date_char = 0000
            if (var_control_date != False):
                var_control_date_char = int(str(l.fecha_vencimiento)[0:4])

            if var_control_date_char >= int(str(date.today())[0:4]):
                l.estatus = 'VIGENTE'
            else:
                l.estatus = 'VENCIDO'
