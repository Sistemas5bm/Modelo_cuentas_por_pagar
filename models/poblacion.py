# -*- coding:utf-8 -*-
from odoo import fields, models, api


class Poblacion(models.Model):
    _name = "poblacion"

    name = fields.Char(string='Pobalcion')

    active = fields.Boolean(string='Activo',default=True)
