# -*- coding:utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class ReporteSaldos(models.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'
    test = fields.Char(string='Testeo')
