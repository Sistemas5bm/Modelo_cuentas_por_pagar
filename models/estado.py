# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Estado(models.Model):
    _name = "estado"

    name = fields.Char(string='Estado')

    active = fields.Boolean(string='Activo',default=True)

    pais = fields.Many2one(

        comodel_name='pais',
        string='Pais'

    )