# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Cif(models.Model):
    _name = "cfdi_reps"

    name = fields.Char(string='Uuid')

    guid_document = fields.Char(string='Guid Document')

    regimen_emisor = fields.Char(string='Regimen Emisor')

    regimen_emisor_desc = fields.Char(string='Regimen Emisor Desc')

    partner_id = fields.Many2one(string='Proveedor')

    rfc_emisor = fields.Char(string='RFC Receptor')

    nombre_receptor = fields.Char(string='Nombre Receptor')

    tipo_documento = fields.Char(string='Tipo Documento')

    version = fields.Char(string='Versión')

    fecha = fields.Datetime(string='Fecha')

    total = fields.Float(string='Total')

    uso_cfdi = fields.Char(string='Uso cfdi')

    xml_binary = fields.Char(string='Archivo XML')



    