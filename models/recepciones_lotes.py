# -*- coding:utf-8 -*-

from odoo import fields, models, api


class RecepcionesLotes(models.Model):

    _name = 'recepciones_lotes'

    _description = 'Este modelo es una interfaz origen TTS de los datos de repciones de fruta'

    name = fields.Integer(string='Id Recepción')

    id_lote = fields.Integer(string='Id Lote')

    id_orden_corte = fields.Integer(string='Id Orden Corte')

    fecha = fields.Date(string='Fecha')

    ticket = fields.Char(string='Ticket')

    peso_bruto = fields.Float(string='Peso Bruto')

    peso_tara = fields.Float(string='Peso Tara')

    peso_muestra = fields.Float(string='Peso Muestra')

    peso_neto = fields.Float(string='Peso Neto')

    peso_bascula_productor = fields.Float(string='Peso Bruto')