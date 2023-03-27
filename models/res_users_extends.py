# -*- coding:utf-8 -*-

from odoo import fields, models, api

#BYMFRESH
class ExtensionRes(models.Model):
    _inherit = 'res.users'

    type_user_cxp = fields.Selection(string='Tipo de usuario CXP', selection=([('solicitante','Solicitante'),
                                                                               ('autorizador','Autorizador')]))
    #teste = fields.Char(string='TESTEO')
    lotes_descarga = fields.Boolean(string='Descargas Lotes', default=True)
    fletes_descarga = fields.Boolean(string='Descarga Fletes', default=True)
    cdis_descarga = fields.Boolean(string='Descarga CFDIs', default=True)
    cortes_descarga = fields.Boolean(string='Decarga Cortes', default=True)

