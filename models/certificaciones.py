# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Ciudad(models.Model):
    _name = "certificaciones"

    name = fields.Char(string='Certificacion')