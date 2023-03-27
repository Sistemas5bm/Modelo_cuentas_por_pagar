# -*- coding:utf-8 -*-how save many2many custom more data

from odoo import fields, models, api, _
import logging

from odoo.exceptions import UserError


class AccountRegisterPaymentExtends(models.TransientModel):

    _inherit = 'account.payment.register'


    def _prepare_payment_vals(self, invoices):
        x = super(AccountRegisterPaymentExtends,self)._prepare_payment_vals(invoices)
        for line in invoices:
            id_partner_ref = line.partner_id.id
            no_cta_ind = self.env['res.partner.bank'].search([('partner_id','=',id_partner_ref),('check','=',True)]).id
            x['partner_bank_id'] = no_cta_ind
            print('Prueba Alex')
            print(no_cta_ind)
        return x

    def _create_payment_vals_from_batch(self, batch_result):
        batch_values = self._get_wizard_values_from_batch(batch_result)
        return {
            'date': self.payment_date,
            'amount': batch_values['source_amount_currency'],
            'payment_type': batch_values['payment_type'],
            'partner_type': batch_values['partner_type'],
            'ref': self._get_batch_communication(batch_result),
            'journal_id': self.journal_id.id,
            'currency_id': batch_values['source_currency_id'],
            'partner_id': batch_values['partner_id'],
            'partner_bank_id': self.env['res.partner.bank'].search([('partner_id','=',batch_values['partner_id']),('check','=',True)]).id,
            'payment_method_id': self.payment_method_id.id,
            'destination_account_id': batch_result['lines'][0].account_id.id
        }