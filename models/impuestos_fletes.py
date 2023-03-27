# -*- coding:utf-8 -*-
from odoo import fields, models, api

class ImpuestosTarifas(models.Model):
    _name = 'impuestos_tarifas'
    name = fields.Float(string='Importe')
    iva = fields.Float(string='IVA')
    importe_mas_iva = fields.Float(string='Importa más IVA')
    retencion_iva = fields.Float(string='Retenciones de IVA')
    importe_total = fields.Float(string='Importe total')
    retencion_adicional = fields.Float(string='Retencion adicional')

    def calcular_impuetos_tarifas(self):
        self.iva = self.name * .16
        self.importe_mas_iva = self.name * 1.16
        self.retencion_iva = self.name * .04
        self.importe_total = self.importe_mas_iva - self.retencion_iva

