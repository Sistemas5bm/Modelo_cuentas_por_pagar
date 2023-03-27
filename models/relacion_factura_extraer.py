# -- coding:utf-8 --

from odoo import fields, models, api

class RelacionFactura(models.Model):
    _name = 'relacion_fatura_copia'

    name = fields.Char(string='Producto')

    descripcion = fields.Char(string='Descripcion')

    cuenta = fields.Char(string='Cuenta')

    cuenta_analitica = fields.Char(string='Cuenta analitica')

    etiquetas_analiticas = fields.Char(string='Etiquetas analiticas')

    cantidad = fields.Float(string='Cantidad')

    udm = fields.Char(string='UdM')

    precio = fields.Float(string='Precio')

    descuento = fields.Float(string='Desc%')

    impuestos = fields.Char(string='Impuestos')

    sub_total = fields.Float(string='Sub total')

    pedido_compra = fields.Char(string='Pedido de compra')