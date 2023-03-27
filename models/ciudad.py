# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Ciudad(models.Model):
    _name = "ciudad"

    name = fields.Char(string='Ciudad')

    active = fields.Boolean(string='Activo',default=True)

    estado = fields.Many2one(

        comodel_name = 'estado',
        string='Estado'

    )