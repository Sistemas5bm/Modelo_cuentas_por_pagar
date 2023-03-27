# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Cif(models.Model):
    _name = "pagos_doctos_rel"

    name = fields.Char(string='Guid Document')

    id_pago = fields.Char(string='Id Pago')

    id_documento = fields.Char(string='Id Documento')

    serie = fields.Char(string='Serie')

    folio = fields.Char(string='')

    moneda_dr = fields.Char(string='Moneda Dr')

    moneda_dr_desc = fields.Char(string='Moneda Dr Desc')

    tipo_cambio_dr = fields.Float(string='Tipo De Cambio Dr')

    metodo_pago_dr = fields.Char(string='Metodo Pago Dr')

    metodo_pago_dr_desc = fields.Char(string='Metodo Pago Dr Desc')

    num_parcialidad = fields.Integer(string='Num Parcialidades')

    imp_saldo_ant = fields.Float(string='Importe Saldo Anterior')

    imp_pagado = fields.Float(string='Importe Pagado')

    imp_saldo_insoluto = fields.Float(string='Importe Saldo Insoluto')

    fecha = fields.Datetime(string='Fecha Pago')

    account_move_pagos_rel = fields.Many2one(comodel_name='account.move',string='Relacion a facturas')
