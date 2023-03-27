# -*- coding:utf-8 -*-

from odoo import fields, models, api
import logging
import pandas as pd
logger = logging.getLogger(__name__)
class HuertasContratosterceros(models.Model):

    _name = "huertas_contratos_terceros"

    name = fields.Many2one(string='Tipo de contrato',comodel_name='tipo_contrato')

    contrato_terceros_huerta = fields.Binary(string='Archivo contrato de terceros')

    contrato_terceros_huerta_filename = fields.Char(string='Nombre de archivo')

    fecha_apertura = fields.Date(string='Fecha apertura')

    fecha_vencimiento = fields.Date(string='Fecha Vencimiento')

    beneficiarios = fields.Many2many(string='Beneficiarios',comodel_name='res.partner')

    es_kg = fields.Boolean(string='Kilogramos limite')

    kg = fields.Float(string='Kilogramos totales')

    huertas_contratos_terceros_huertas_rel = fields.Many2one(string='Huertas Contratos Relacion',comodel_name='huertas')

    alias_nombre = fields.Char(string='Alias del contrato')


    @api.model
    def create(self, variables):
        modelo_huerta = super(HuertasContratosterceros, self).create(variables)
        nombre_productor = modelo_huerta.huertas_contratos_terceros_huertas_rel.productor.name
        huerta = modelo_huerta.huertas_contratos_terceros_huertas_rel.name
        sader = modelo_huerta.huertas_contratos_terceros_huertas_rel.sader
        fecha_emision = modelo_huerta.fecha_apertura
        fecha_vencimiento = modelo_huerta.fecha_vencimiento
        string_x = ''
        for line in modelo_huerta.beneficiarios:
            line.name
            global list
            list = [line.name]
        my_list= []
        my_list.append(list)

        #print(nombre_productor)
        logger.info('variables : {0}'.format(variables))
        alias_compuesto = variables['name']
        variables['alias_nombre'] = alias_compuesto
        print(my_list)



        return modelo_huerta

