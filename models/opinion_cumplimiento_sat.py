# -*- coding:utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class OpinionCumplimiento(models.Model):
    _name = 'opinion_cumplimiento_sat'

    name = fields.Char(string='Opinion de cumplimiento de obligaciones fiscales',
                       default='Opinion de cumplimiento de obligaciones fiscales')

    opinion_cumplimiento = fields.Binary(string='Archivo de OCOF')

    opinion_cumplimiento_filename = fields.Char(string='Nombre de archivo')

    opinion_cumplimiento_partner_rel = fields.Many2one(string='Opinion relacion',comodel_name='res.partner')

    fecha_emision = fields.Datetime(string='Fecha de emision')