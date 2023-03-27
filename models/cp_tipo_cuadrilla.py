# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Cuadrillas(models.Model):

    _name = "tipo_cuadrillas"

    _description = 'Catalogo de tipo de cuadrillas'

    _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Imposible crear, ya existe un registro identico')]

    name = fields.Char(string='Tipo de cuadrilla')