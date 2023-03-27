# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Cif(models.Model):
    _name = "cif"

    name = fields.Char(string='CSF',default='CSF')

    cif_filename = fields.Char(string='Nombre de archivo')

    cif_file = fields.Binary(string='Archivo CSF')

    fecha_emision = fields.Date(string='Fecha de emisión')

    cif_rel = fields.Many2one('res.partner',string='CSF Rel')
