# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Ciudad(models.Model):
    _name = "organismos_verificadores"

    name = fields.Char(string='Organismos verificadores')