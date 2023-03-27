# -*- coding:utf-8 -*-

from odoo import fields, models, api


class LotesCfdi(models.Model):

    _name = "lotes_cfdi"


    name = fields.Char(string='Nombre',default='Lotes - Cfdi - Rel')


    #es el restante
    saldo_pendiente = fields.Float(string='Saldo Pendiente')
    # es el abono
    abono = fields.Float(string='Abono')

    account_move_id = fields.Many2one(comodel_name='account.move',string='Factura')

    account_move_id_uuid = fields.Char(related='account_move_id.uuid',string='UUID')

    account_move_id_partner_id = fields.Many2one(related='account_move_id.partner_id',string='Emisor de factura')

    lotes_id = fields.Many2one(comodel_name='lotes',string='Lote')

    lotes_id_fecha = fields.Date(related='lotes_id.fecha',string='Fecha Corte')

    lotes_id_partner_id = fields.Many2one(related='lotes_id.id_partner',string='Productor')

    lotes_id_importe = fields.Float(related='lotes_id.importe',string='Importe Lote')