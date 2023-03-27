# -*- coding:utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class ExtensionCuentasbancarias(models.Model):

    _inherit = 'res.partner.bank'

    es_caratura_estado_cuenta = fields.Boolean(string='¿CEC?')

    caratula_estado_cuenta = fields.Binary(string='Archivo Caratula de estado de cuenta')

    caratula_estado_cuenta_filename = fields.Char(string='Nombre del archivo')

    check = fields.Boolean(string='¿Es cuenta default?')

    resultado = fields.Char(string='Retorna valor',compute='search_default_accounts')

    alerta_check_def = fields.Char(compute='search_default_accounts')
    #alerta_check_default = fields.Selection(selection=[('test','test')])
    rfc = fields.Char(string='RFC', compute='get_rfc')

    def get_rfc(self):
        for line in self:
            rfc_line = line.env['res.partner'].search([('id', '=', line.partner_id.id)]).vat
            line.rfc = rfc_line

    @api.onchange("check")
    def search_default_accounts(self):
        for line in self:
            line.alerta_check_def = ''
            found_checks = line.env['res.partner.bank'].search_count([('check','=',True),
                                                                      ('partner_id','=',line.partner_id.id)])
            #mapea el modelo y verifica que solo exista una cuenta default(con un booleano), solo permite una
            #cuanta default (Marcada con el check)
            line.resultado = found_checks
            if found_checks == 0:
                if line.check == False:
                   line.alerta_check_def = 'HACER CUENTA DAFAULT'
                else:
                    line.alerta_check_def = 'CUENTA DAFAULT'
            if found_checks >= 2:
                line.check = False
                line.alerta_check_def = 'ESTA CUENTA NO ES DEAFULT - SOLO PUEDE HABER UNA CUENTA DEFAULT'















