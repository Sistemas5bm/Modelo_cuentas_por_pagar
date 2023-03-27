# -*- coding:utf-8 -*-how save many2many custom more data

from odoo import fields, models, api
import logging

from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class AccountPaymentExtends(models.Model):

    _inherit = 'account.payment'

    complemento_de_pago_file = fields.Binary(string='Complemento de pago')

    complemento_de_pago_filename = fields.Char(string='Nombre de archivo')

    comprobante_pago_file = fields.Binary(string='Comprobante de pago')

    comprobante_pago_filename = fields.Char(string='Nombre de archivo')

    estatus_layout = fields.Char(string='Estatus Layout',default='notready')

    relacion_layout = fields.Many2one('pagos_layout',string='Relación Layout')

    relacion_layout_fletes = fields.Many2one('pagos_layout_fletes', string='Relación Layout')

    bank_id_name = fields.Many2one(related='partner_bank_id.bank_id')

    bank_id_name_code = fields.Char(related='partner_bank_id.bank_id.bic',string='Codigo Banco')

    recn = fields.Char(compute='get_invoice_reconciled_data', string="Pagos")







    def get_invoice_reconciled_data(self):
        for l in self:
            l.recn = l.reconciled_bill_ids.uuid



    def unlink(self):
        logger.info('Se disparo la funcion unlink')
        for record in self:
            if record.estatus_layout == 'notready' or record.estatus_layout == None:
                super(AccountPaymentExtends, record).unlink()
            else:
                raise UserError('No se puede eliminar el registro por que no se encuentra en el estado sin preparar')
