# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Localidad(models.Model):
    _name = "localidad"

    name = fields.Char(string='Localidad')

    active = fields.Boolean(string='Activo',default=True)

    ciudad = fields.Many2one(

        comodel_name='ciudad',
        string='Ciudad'

    )