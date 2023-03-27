# -*- coding:utf-8 -*-

from odoo import fields, models, api


class CorridaLotes(models.Model):
    _name = "lotes_corrida"

    name = fields.Char(string='Id Seleccion')
    fecha = fields.Datetime(string='Fecha')
    id_lote = fields.Char(string=' Id Lotes')
    id_lote2 = fields.Many2one(string='Id lote', comodel_name='lotes')
    peso_neto = fields.Float(string='Peso neto')
    producto = fields.Char(string='Producto')
    presentacion = fields.Char(string='Presentacion')
    cajas = fields.Float(string='Cajas')
    kilogramos = fields.Float(string='Kilogramos')
    exportacion = fields.Float(string='Exportacion')
    nacional = fields.Float(string='Nacional')
    merma = fields.Float(string='Merma')
    porc_exportacion = fields.Float(string='Porc Exportacion')
    porc_nacional = fields.Float(string='Porc Nacional')
    porc_merma = fields.Float(string='Porc Merma')
    porcentaje_produc = fields.Float(string='Porcentaje producto', digits=(12, 2))
    lote_recepcion = fields.Integer(string='Recepcion de lote')
    orden_corte_lote = fields.Integer(string='Orden de cotre')
    tipo_corte = fields.Char(string='Tipo de corte')
    #id_no_pallet = fields.Integer(string='Id No Pallet')
    #id_seleccion_pallet = fields.Integer(string='Id Seleccion Pallet')