# -*- coding:utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError

class AutorizacionesConfirm(models.TransientModel):


    _name = "autorizaciones_wizard"

    name = fields.Char(string='namex',default='x')
    #_inherit = 'account.move'

    password = fields.Char(string='Password')
