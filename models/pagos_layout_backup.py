# -*- coding:utf-8 -*-
import base64
from odoo import fields, models, api
import logging
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
logger = logging.getLogger(__name__)

class PagosLayout(models.Model):

    _name = "pagos_layout"

    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Referencia',copy=False,tracking=True,track_visibility='always',store=True,required=True)

    fecha_reg = fields.Datetime(string='Fecha Layout',default=datetime.now(),tracking=True,track_visibility='always',store=True,readonly=False,required=True)

    banco = fields.Many2one(comodel_name='res.bank',string='Banco Origen',tracking=True,track_visibility='always',store=True)

    layout_type_bank = fields.Selection(string='Tipo de layout',
                                   selection=[
                                       ('santander_multiples_bancos','Santander Multiples Bancos'),
                                       ('santander_a_mismo_banco','Santander A Mismo Banco'),
                                       ('bbva_a_multiples_bancos','Bbva Multiples Bancos'),
                                       ('bbva_a_mismo_banco','Bbva Mismo Banco')
                                   ],default='santander_a_mismo_banco',copy=False,tracking=True,track_visibility='always',store=True)

    relacion_pagos = fields.One2many('account.payment','relacion_layout',size=64,tracking=True,track_visibility='always',store=True)

    layout_name = fields.Char(string='Contenedor de layout',size=64,default='layout.txt',tracking=True,track_visibility='always',store=True)

    txt_layout_file = fields.Binary(string='Archivo de layout',tracking=True,track_visibility='always',store=True,readonly=True)

    fecha_mod_layout = fields.Datetime(string='Fecha Cr/Mod Layout TXT',tracking=True,track_visibility='always',store=True,readonly=True)

    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('validado', 'Validado'),
        ('cancelado','Cancelado')

    ], default='borrador', string='Estados', copy=False,tracking=True,track_visibility='always',store=True)

    def delete_edit_validate(self):
        invoices_from_payment = self.relacion_pagos
        #print('primer dato',invoices_from_payment)
        for line_payment in invoices_from_payment:
            #print(line_payment.id)
            result = self.env['account.move'].search([('payment_id', '=', line_payment.id)]).ref
            #self._cr.execute('select ref FROM account_move where payment_id=%s'%(line_payment.id))
            #result = self._cr.fetchall()
            row_separator = ' '
            if result.count(row_separator) == 0:
                print('Fac Individuales: ')
                print(result)
                result = result
            if result.count(row_separator) > 0:
               print('Fac separadas: ')
               print(result.replace(' ', '\n'))
               result = result.replace(' ', '\n')


    def setStatusReady(self):
        for line in self:
            print('Prueba')

    def cancelar_layout(self):
        #self.state = 'borrador'
        self._cr.execute('update pagos_layout set state=%s where id=%s', ('borrador', self.id))
        for xline in self.relacion_pagos:
            print(xline.id)
            pago_id = self.env['account.payment'].browse([xline.id])
            print(self.env['account.payment'].browse([xline.id]))
            pago_id.write({'estatus_layout': 'notready'})
            self.env.cr.commit()

    def default_bank(self):
        self.banco = self.env['res.bank'].search([('name', '=', 'SANTANDER')], limit=1).id

    @api.model
    def create(self, variables):
            modelo_layout_pago = super(PagosLayout, self).create(variables)
            logger.info('variables : {0}'.format(variables))
            return modelo_layout_pago

    def write(self, vals):
        if any(state == 'validado' for state in set(self.mapped('state'))):
            raise ValidationError("No se puede editar en estado 'validado'")
        else:
            return super().write(vals)


    def export_txt_layout(self):
        if self.layout_type_bank == 'santander_a_mismo_banco':
           print('Layout TXT')
           file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_mismo_banco.txt", "w+")
           for line in self.relacion_pagos:
               dic = str(line.partner_id.name) + " " + str(line.partner_bank_id.acc_number) + " " + str(line.amount) + " " + str(line.recn) +\
                             " " + line.date.strftime('%d%m%Y') + f"\n"
               print(dic)
               file_layout_txt.write(dic)

           file_layout_txt.close()

           file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_mismo_banco.txt", "rb+")
           out = file_layout_txt.read()

           file_layout_txt.close()

           self.txt_layout_file = base64.b64encode(out)

           self.layout_name = 'layout_santander_mismo_banco.txt'

           self.write({'txt_layout_file': base64.b64encode(out), 'layout_name': 'layout_santander_mismo_banco.txt'})

           self.fecha_mod_layout = datetime.now()

        if self.layout_type_bank == 'santander_multiples_bancos':
           print('Layout TXT')
           file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_multiples_bancos.txt", "w+")
           for line in self.relacion_pagos:
               dic = "65507540168" + "     " + str(line.partner_bank_id.acc_number) + "  " + str(line.bank_id_name_code) + "     " + str(line.partner_id.name) +\
                     "     " + str(line.amount) + "     " + str(line.recn) +\
                             "     "  + "N" + "     "+ "1" + "\n"
               print(dic)
               file_layout_txt.write(dic)

           file_layout_txt.close()

           file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_multiples_bancos.txt", "rb+")
           out = file_layout_txt.read()

           file_layout_txt.close()

           self.txt_layout_file = base64.b64encode(out)

           self.layout_name = 'layout_santander_multiples_bancos.txt'

           self.write({'txt_layout_file': base64.b64encode(out), 'layout_name': 'layout_santander_multiples_bancos.txt'})

           self.fecha_mod_layout = datetime.now()



    def printPdf(self):
        print('PRINT PDF')

    def confirmLayout(self):
        print('Confirm Layout')
        for xline in self.relacion_pagos:
            print(xline.id)
            pago_id = self.env['account.payment'].browse([xline.id])
            print(self.env['account.payment'].browse([xline.id]))
            pago_id.write({'estatus_layout': 'locked'})
            self.env.cr.commit()
        self.state = 'validado'
