# -*- coding:utf-8 -*-

from odoo import fields, models, api

class ContratoBym(models.Model):
    _name = "contrato_bym"
    name = fields.Char(string='Tipo de contrato', default='Contrato B&M')
    contrato_bym_archivo = fields.Binary(string='Archivo contrato B&M')
    fecha_apertura = fields.Date(string='Fecha apertura')
    fecha_vencimiento = fields.Date(string='Fecha Vencimiento')

    res_partner_contract_rel = fields.Many2one(comodel_name='res.partner')

    beneficiario = fields.Many2many('res.partner', string='Beneficiarios', store=True)
