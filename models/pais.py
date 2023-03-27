# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Pais(models.Model):
    _name = "pais"

    name = fields.Char(string='Pais')

    active = fields.Boolean(string='Activo',default=True)

