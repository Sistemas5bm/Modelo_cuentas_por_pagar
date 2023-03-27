# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Lotes(models.Model):
    _name = "lotesx"

    name = fields.Char(string='Numero de lote')

    id_credito_mov = fields.Integer(string='IdCreditoMovimiento')

    nombre_proveedor = fields.Char(string='Nombre')

    fecha = fields.Datetime(string='Fecha')

    tipo_movimiento = fields.Char(string='Tipo de movimiento')

    importe = fields.Float(string='Importe')

    kilogramos = fields.Float(string='Kilogramos')

    observaciones = fields.Char(string='Observaciones')
