# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Pais(models.Model):
    _name = "sat_documentos_lotes"

    name = fields.Char(string='Bico',default='BICO')

    bico_file = fields.Binary(string='BICO')

    bico_filename = fields.Char(string='Nombre de archivo')

    active = fields.Boolean(string='Activo', default=True)

    bico_lotes_rel = fields.Many2one(string='Bico Relacion',comodel_name='lotes')