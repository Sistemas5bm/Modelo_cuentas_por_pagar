# -*- coding:utf-8 -*-

from odoo import fields, models, api
class UserPermits(models.Model):
    _name= 'permisos_usuarios'
    name = fields.Many2one('res.users', string='Usuarios', )
    type_user = fields.Selection(string='Tipo de usuario', selection=([('solicitante', 'Solicitante'),
                                                ('autorizador', 'Autorizador')]), default='autorizador')



