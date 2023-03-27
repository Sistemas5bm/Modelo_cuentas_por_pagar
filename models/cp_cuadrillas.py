# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Cuadrillas(models.Model):

    _name = "cuadrillas"

    name = fields.Many2one(comodel_name='tipo_cuadrillas',string='Tipo de cuadrilla')

    cuadrilla_rel = fields.Many2one('cortes','Relacion de cortes',ondelete='cascade')

    importe = fields.Float(string='Importe')

