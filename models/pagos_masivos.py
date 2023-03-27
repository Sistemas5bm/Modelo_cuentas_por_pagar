# -*- coding:utf-8 -*-

from odoo import fields, models, api


class CorridaLotes(models.Model):
    _name = "pagos_masivos"

    name = fields.Many2one('account.move', string='Factura' , required=True, domain="[('move_type','=','in_invoice'),('state','=','posted'),"
                                                                                    "('payment_state','!=','paid')]",help='Este campo es para seleccionar'
                                                                                                                          ' la factura a pagar.')
    importe_adeudado = fields.Float(string='Importe Adeudado Docto', store=True , required=True, help='Este es el importe adeudado cuando se realizo el pago'
                                                                                                ' en el documento.')
    importe_a_pagar = fields.Float(string='Importe a pagar', store=True , required=True,help='Importe a pagar de la factura en el modulo de pago masivo.')



    fecha_pago = fields.Date(string='Fecha Vencimiento', store=True, required=True,help='Este campo es la fecha de pago segun el vencimiento de la factura.')

    pagos_layout_rel = fields.Many2one('pagos_layout')

    pagos_masivos_presupuesto = fields.Many2one('presupuesto_lotes')

    restante_real = fields.Float(string='Adeudo General',store=False,compute='retreive_extra_data', help='Este campo regresa el adeudo general tomando en'
                                                                                                         ' cuenta los pagos que se han realizado totalmente'
                                                                                                         ' de esta factura.')
    #Compute's fields
    uuid = fields.Char(string='UUID',related='name.uuid')
    partner_id = fields.Many2one(string='Emisor de factura', related='name.partner_id')
    payment_state = fields.Selection(string='Estado de pago', related='name.payment_state')
    date_invoice = fields.Date(string='Fecha Factura', related='name.invoice_date')
    serie = fields.Char(string='Serie', related='name.serie')
    folio = fields.Char(string='Folio', related='name.folio')


    @api.onchange("name")
    def retreive_data_from_invoice(self):
        for line in self:
            residual = line.env['account.move'].search([('id', '=', line.name.id)]).amount_residual
            invoice_date_due = line.env['account.move'].search([('id', '=', line.name.id)]).invoice_date_due
            print('inoive_date_vencimiento', invoice_date_due)
            line.importe_adeudado = residual
            line.importe_a_pagar = residual


    def retreive_extra_data(self):
        for line in self:
            residual = line.env['account.move'].search([('id', '=', line.name.id)]).amount_residual
            line.restante_real = residual
            residual = line.env['account.move'].search([('id', '=', line.name.id)]).amount_residual
            invoice_date_due = line.env['account.move'].search([('id', '=', line.name.id)]).invoice_date_due
            print('inoive_date_vencimiento', invoice_date_due)
            if (line.importe_adeudado - line.importe_a_pagar) != 0:
                line.restante_real = line.importe_adeudado - line.importe_a_pagar
            line.fecha_pago = invoice_date_due
            print(line.restante_real)



