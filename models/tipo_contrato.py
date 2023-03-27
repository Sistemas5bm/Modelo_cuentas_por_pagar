# -*- coding:utf-8 -*-

from odoo import fields, models, api


class ContratosCompraVenta(models.Model):
    _name = "tipo_contrato"

    name = fields.Char(string='Tipo de contrato')

    active = fields.Boolean(string='Activo',default=True)