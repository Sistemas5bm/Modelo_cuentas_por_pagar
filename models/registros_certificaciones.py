# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Ciudad(models.Model):
    _name = "certificaciones_registros"

    name = fields.Many2one(string="Certificacion",comodel_name='certificaciones')

    num_certificacion = fields.Char(string="Numero de certificacion")

    fecha_vencimiento = fields.Date(string="Fecha de vencimiento")

    organismo_verificador = fields.Many2one(string="Organismo verificador",comodel_name='organismos_verificadores')

    ggn = fields.Char(string="GGN")

    registro_certificaciones_huertas_rel = fields.Many2one(comodel_name='huertas',string='Huertas Relacion')

