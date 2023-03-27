# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Cif(models.Model):
    _name = "cfdi_reps_detail"

    name = fields.Char(string='Guid Document')

    id_pago = fields.Char(string='Id Pago')

    version = fields.Char(string='Versión')

    fecha_pago = fields.Datetime(string='Fecha de pago')

    forma_pago = fields.Char(string='Forma Pago')

    forma_pago_desc = fields.Char(string='Forma de pago desc')

    moneda = fields.Many2one(string='Moneda P')

    tipo_cambio = fields.Float(string='Tipo Cambio Pago')

    monto = fields.Float(string='Monto')

    num_operacion  = fields.Char(string='Num Operacion')

    rfc_emisor = fields.Char(string='RFC Emisor')

    nom_banco_ord_ext = fields.Char(string='Banco Ord Ext')

    cta_ordenante = fields.Char(string='Cuenta Ordenante')

    rfc_emisor_cta_beneficiario = fields.Char(string='Cta beneficiario')

