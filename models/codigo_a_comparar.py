# -*- coding:utf-8 -*-
import base64
from odoo import fields, models, api, _
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

    fecha_mod_layout = fields.Datetime(string='Fecha Cr/Mod Layout TXT', tracking=True, track_visibility='always', store=True, readonly=True)

    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('validado', 'Validado'),
        ('cancelado','Cancelado')

    ], default='borrador', string='Estados', copy=False, tracking=True, track_visibility='always', store=True)

    presupuestos_rel = fields.Many2one(string='Presupuesto', comodel_name='presupuesto_lotes', store=True)

    total_layout = fields.Float(string='Total Layout', compute='total_calculate')

    relacion_facturas = fields.One2many('account.move','pagos_layout_rel',string='Relacion Facturas')

    pagos_masivos = fields.One2many('pagos_masivos', 'pagos_layout_rel', string='Pagos Masivos')

    def masive_payment(self):
        print('')

    @api.onchange('presupuestos_rel')
    def add_invoices_to_list(self):
        #Factura adicional
        for rec in self:
            lines = []
            list_inv = []
            dic_values_2 = ()
            for line in rec.presupuestos_rel.facturas_adicionales:
                if(line.payment_state == 'not_paid' or line.payment_state == 'partial'):
                   lines.append(line.id)
                   dic_values_2 = (0, 0, {'name': line.id,
                                  })
                   list_inv.append(dic_values_2)
                else:
                    print('')

            tup_invoice_ids = tuple(lines)
            #print(tup_invoice_ids)
            #rec.relacion_facturas = tup_invoice_ids
            rec.pagos_masivos = [(5, 0, 0)]
            rec.pagos_masivos = list_inv

        #Facturas de lotes
        for recx in self:
            linesx = []
            list_inv = []
            dic_values = ()
            for linez in recx.presupuestos_rel.lotes_provisionados:
                if (linez.data_rel.payment_state == 'not_paid' or linez.data_rel.payment_state == 'partial'):
                    linesx.append((4, int(linez.data_rel.id)))
                    dic_values = (0, 0, {'name': line.id,
                                   })
                    list_inv.append(dic_values)
                else:
                    print('')

            # remueve los items del one2many
            # rec.relacion_pagos = ([2,int(line.id_pago)])
            # Obtiene los pagos relacionados con el presupuesto
        recx.pagos_masivos = list_inv

    def total_calculate(self):
        total_lotes = 0.0
        for rec in self.relacion_pagos:
            print(rec.amount)
            total_lotes = total_lotes + rec.amount
        self.total_layout = total_lotes

    """
(0, 0,  { values })    link to a new record that needs to be created with the  given values dictionary
(1, ID, { values })    update the linked record with id = ID (write *values* on it)
(2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
(3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
(4, ID)                link to existing record with id = ID (adds a relationship)
(5)                    unlink all (like using (3,ID) for all linked records)
(6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
    """
    def action_register_payment(self):
        ''' Open the account.payment.register wizard to pay the selected journal entries.
        :return: An action opening the account.payment.register wizard.
        '''
        return {
            'name': _('Register Payment'),
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.pagos_masivos.name.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
        ''' Open the account.payment.register wizard to pay the selected journal entries.
        :return: An action opening the account.payment.register wizard.
        '''

    #Buscar coincidencia con partner_bank_id

    def pruebas(self):
        global r
        r = ''
        for r in self:
            pagos_ids = []
            r._cr.execute('''
                            SELECT id from account_payment 
                             ''')
            query_res = r._cr.dictfetchall()

            # idss = (1, 2, 3, 4, 5, 6, 7)


            for pys in query_res:
                pagos_ids.append(pys['id'])
            ids_payments_all = tuple(pagos_ids)
            #hasta aqui tod0 bien

        for rec in self:
            lines = []
            for line in rec.relacion_facturas:
                print('xxxxxxx')
                lines.append(line.id)
                print('testing data')
                print(line.id)

            tup_invoice_ids = tuple(lines)


            #condicionar si las facturas adicionales son false
            if str(tup_invoice_ids) == '()':
                print('Not have aditional invoices')
            if str(tup_invoice_ids) != '()':
                r._cr.execute('''SELECT
                payment.id as pay,
                payment.amount,
                ARRAY_AGG(DISTINCT invoice.id) AS invoice_ids,
			    invoice.id,
			    invoice.invoice_date,
                invoice.move_type
                FROM account_payment payment
                JOIN account_move move ON move.id = payment.move_id
                JOIN account_move_line line ON line.move_id = move.id
                JOIN account_partial_reconcile part ON
                part.debit_move_id = line.id
                OR
                part.credit_move_id = line.id
                JOIN account_move_line counterpart_line ON
                part.debit_move_id = counterpart_line.id
                OR
                part.credit_move_id = counterpart_line.id
                JOIN account_move invoice ON invoice.id = counterpart_line.move_id
                JOIN account_account account ON account.id = line.account_id
                WHERE account.internal_type IN ('receivable', 'payable')
                AND payment.id in %(pays)s
                AND line.id != counterpart_line.id
                AND invoice.move_type in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                AND invoice.id in %(account_move_ids)s
			    GROUP BY payment.id, invoice.move_type, invoice.id, invoice.invoice_date''', {
                'pays': ids_payments_all,
                'account_move_ids': tup_invoice_ids,
                })
            query_res = r._cr.dictfetchall()
            pagos_ids_all = []
            pagos_ids_new = []
            payments_ids = ''
            lines = []

            for res in query_res:
                payments_ids = res['pay']
                pagos_ids_new.append(payments_ids)
                lines.append((4, int(payments_ids)))
        rec.relacion_pagos = lines
        """
        for recx in self:
            linesx = []
            for linez in recx.presupuestos_rel.lotes_provisionados:
                print(linez.id_pago)
                linesx.append((4, int(linez.id_pago)))


            #remueve los items del one2many
            #rec.relacion_pagos = ([2,int(line.id_pago)])
            #Obtiene los pagos relacionados con el presupuesto
        print('formato esperado')
        print(linesx)
        recx.relacion_pagos = linesx
        """

    @api.onchange("pagos_masivos")
    def not_duplicate_payment_document(self):
        print('No duplicate')
        for line_invoice in self:
            exist_invoice_list = []
            for line_invoice_list in line_invoice.pagos_masivos:
                if line_invoice_list.name.id in exist_invoice_list:
                    raise ValidationError(_('Solo puedes colocar una misma factura por layout'))
                exist_invoice_list.append(line_invoice_list.name.id)





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

    def export_txt_layout_santander(self):
        print('santander txt')
        for record in self:
                file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_mismo_banco.txt",
                                       "w+")
                # field value len
                ini_val_len = 0
                val_name_len = 16
                val_acc_number = 16
                val_amount_len = 13
                val_ref_len = 40
                val_date_len = 8
                for line in record.relacion_pagos:
                    # print(line.bank_id_name.name)
                    if line.bank_id_name.name == 'SANTANDER':
                        # resize string with format substring
                        list_invoice = []
                        for lnx in line.reconciled_bill_ids:
                            list_invoice.append(lnx.uuid[0:8])
                        x_res = tuple(list_invoice)
                        acc_number_format = str(line.partner_bank_id.acc_number)[ini_val_len:val_acc_number]
                        name_format = str(line.partner_id.name)[ini_val_len:val_name_len]
                        amount_format = str("{:.2f}".format(line.amount))[ini_val_len:val_amount_len]
                        ref_format = str(x_res)[ini_val_len:val_ref_len]
                        date_format = line.date.strftime('%d%m%Y')
                        # count characters
                        acc_number_format_len = len(acc_number_format)
                        name_format_len = len(name_format)
                        amount_format_len = len(amount_format)
                        ref_format_len = len(ref_format)
                        # get difference between len's refer field and real field
                        spaces_to_in_acc_number = val_acc_number - acc_number_format_len
                        spaces_to_in_name = val_name_len - name_format_len
                        zeros_to_in_amount = val_amount_len - amount_format_len
                        spaces_to_in_ref = val_ref_len - ref_format_len
                        # differences + len(total)
                        spaces_to_in_acc_number_total = spaces_to_in_acc_number + acc_number_format_len
                        spaces_to_in_name_total = spaces_to_in_name + name_format_len
                        zeros_to_in_amount_total = zeros_to_in_amount + amount_format_len
                        spaces_to_in_ref_total = spaces_to_in_ref + ref_format_len
                        # format without spaces into
                        acc_number_format = acc_number_format.ljust(spaces_to_in_acc_number_total)
                        name_format = name_format.ljust(spaces_to_in_name_total)
                        amount_format = amount_format.zfill(zeros_to_in_amount_total)
                        ref_format = ref_format.ljust(spaces_to_in_ref_total)

                        # format dic for layout *.txt
                        dic = name_format + acc_number_format + amount_format + ref_format + date_format + f"\n"

                        print(dic)

                        file_layout_txt.write(dic)

                file_layout_txt.close()

                file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_mismo_banco.txt",
                                       "rb+")
                out = file_layout_txt.read()

                file_layout_txt.close()

                record.txt_layout_file = base64.b64encode(out)

                record.layout_name = 'layout_santander_mismo_banco.txt'

                record.write(
                    {'txt_layout_file': base64.b64encode(out), 'layout_name': 'layout_santander_mismo_banco.txt'})

                record.fecha_mod_layout = datetime.now()

    def export_txt_layout_other_banks(self):
        print('other banks')
        for record in self:
                file_layout_txt = open(
                    "odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_multiples_bancos.txt", "w+")
                # len's fields layout *.txt
                val_acc_number_origin_len = 16
                val_acc_number_destine_len = 20
                val_code_bank_destine_len = 5
                val_name_destine_len = 40
                val_amount_destine_len = 24
                val_amount_destine_integer_len = 17
                val_amount_destine_decimal_len = 7
                val_ref_destine_len = 130
                val_aplic_form_destine_len = 8
                ini_val_len = 0

                for line in record.relacion_pagos:

                    if line.bank_id_name.name != 'SANTANDER':
                        # formate len's
                        acc_number_origin_format = str('65507540168')[ini_val_len:val_acc_number_origin_len]
                        acc_number_destine_format = str(line.partner_bank_id.l10n_mx_edi_clabe)[
                                                    ini_val_len:val_acc_number_destine_len]
                        code_bank_destine = str(line.bank_id_name_code)[ini_val_len:val_code_bank_destine_len]
                        name_destine_format = str(line.partner_id.name)[ini_val_len:val_name_destine_len]
                        amount_destine_format = str("{:.2f}".format(line.amount))[ini_val_len:val_amount_destine_len]
                        # Revisar
                        list_x = []
                        for l_ref in line.reconciled_bill_ids:
                            list_x.append(l_ref.uuid[0:8])

                        print(tuple(list_x))
                        ref_destine_format = str(list_x)[ini_val_len:val_ref_destine_len]
                        aplic_form_destine_format = str('1')
                        # count len's
                        acc_number_origin_format_len = len(acc_number_origin_format)
                        acc_number_destine_format_len = len(acc_number_destine_format)
                        code_bank_destine_len = len(code_bank_destine)
                        name_destine_format_len = len(name_destine_format)
                        amount_destine_format_len = len(amount_destine_format)
                        amount_decimal_search_character = amount_destine_format.find('.')
                        amount_integer = amount_destine_format[ini_val_len:amount_decimal_search_character]
                        amount_decimal = amount_destine_format[
                                         amount_decimal_search_character:amount_destine_format_len].replace('.', '')
                        amount_integer_fill = amount_integer.zfill(val_amount_destine_integer_len)
                        amount_decimal_fill = amount_decimal.ljust(val_amount_destine_decimal_len, '0')
                        # Concat Integers and decimals
                        concat_amount = amount_integer_fill + amount_decimal_fill
                        print(concat_amount)

                        # Revisar
                        ref_destine_format_len = len(ref_destine_format)
                        aplic_form_destine_format_len = len(aplic_form_destine_format)

                        # get difference between len's refer field and real field
                        spaces_to_in_acc_number_origin = val_acc_number_origin_len - acc_number_origin_format_len
                        spaces_to_in_acc_number_destine = val_acc_number_destine_len - acc_number_destine_format_len
                        spaces_to_in_code_bank_destine = val_code_bank_destine_len - code_bank_destine_len
                        spaces_to_in_name_destine = val_name_destine_len - name_destine_format_len
                        spaces_to_in_ref_destine = val_ref_destine_len - ref_destine_format_len
                        spaces_to_in_aplic_form_destine = val_aplic_form_destine_len - aplic_form_destine_format_len
                        # Complete len's addition
                        spaces_to_in_acc_number_origin_total = spaces_to_in_acc_number_origin + acc_number_origin_format_len
                        spaces_to_in_acc_number_destine_total = spaces_to_in_acc_number_destine + acc_number_destine_format_len
                        spaces_to_in_code_bank_destine_total = spaces_to_in_code_bank_destine + code_bank_destine_len
                        spaces_to_in_name_destine_total = spaces_to_in_name_destine + name_destine_format_len

                        spaces_to_in_ref_destine_total = spaces_to_in_ref_destine + ref_destine_format_len
                        spaces_to_in_aplic_form_destine_total = spaces_to_in_aplic_form_destine + aplic_form_destine_format_len
                        # formate with spaces or zeros
                        acc_number_origin_format = acc_number_origin_format.ljust(spaces_to_in_acc_number_origin_total)
                        acc_number_destine_format = acc_number_destine_format.ljust(
                            spaces_to_in_acc_number_destine_total)
                        code_bank_destine = code_bank_destine.ljust(spaces_to_in_code_bank_destine_total)
                        name_destine_format = name_destine_format.ljust(spaces_to_in_name_destine_total)
                        # Falta amount
                        print()

                        # Revisar
                        ref_destine_format = ref_destine_format.ljust(spaces_to_in_ref_destine_total)
                        aplic_form_destine_format = aplic_form_destine_format.rjust(
                            spaces_to_in_aplic_form_destine_total)

                        dic = acc_number_origin_format + acc_number_destine_format + code_bank_destine \
                              + name_destine_format + concat_amount + str(
                            ref_destine_format) + aplic_form_destine_format + f"\n"

                        file_layout_txt.write(dic)
                        print('dic')
                        print(dic)

                file_layout_txt.close()

                file_layout_txt = open(
                    "odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_multiples_bancos.txt", "rb+")
                out = file_layout_txt.read()

                file_layout_txt.close()

                record.txt_layout_file = base64.b64encode(out)

                record.layout_name = 'layout_santander_multiples_bancos.txt'

                record.write(
                    {'txt_layout_file': base64.b64encode(out), 'layout_name': 'layout_santander_multiples_bancos.txt'})

                record.fecha_mod_layout = datetime.now()



    def export_txt_layout(self):
      for record in self:
        if record.layout_type_bank == 'santander_a_mismo_banco':
           file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_mismo_banco.txt", "w+")
           #field value len
           ini_val_len = 0
           val_name_len = 16
           val_acc_number = 16
           val_amount_len = 13
           val_ref_len = 40
           val_date_len = 8
           for line in record.relacion_pagos:
               #print(line.bank_id_name.name)
              if line.bank_id_name.name == 'SANTANDER':
               #resize string with format substring
               list_invoice = []
               for lnx in line.reconciled_bill_ids:
                   list_invoice.append(lnx.uuid[0:8])
               x_res = tuple(list_invoice)
               acc_number_format = str(line.partner_bank_id.acc_number)[ini_val_len:val_acc_number]
               name_format = str(line.partner_id.name)[ini_val_len:val_name_len]
               amount_format = str("{:.2f}".format(line.amount))[ini_val_len:val_amount_len]
               ref_format = str(x_res)[ini_val_len:val_ref_len]
               date_format = line.date.strftime('%d%m%Y')
               #count characters
               acc_number_format_len = len(acc_number_format)
               name_format_len = len(name_format)
               amount_format_len = len(amount_format)
               ref_format_len = len(ref_format)
               #get difference between len's refer field and real field
               spaces_to_in_acc_number = val_acc_number - acc_number_format_len
               spaces_to_in_name = val_name_len - name_format_len
               zeros_to_in_amount = val_amount_len - amount_format_len
               spaces_to_in_ref = val_ref_len - ref_format_len
               #differences + len(total)
               spaces_to_in_acc_number_total = spaces_to_in_acc_number + acc_number_format_len
               spaces_to_in_name_total = spaces_to_in_name + name_format_len
               zeros_to_in_amount_total = zeros_to_in_amount + amount_format_len
               spaces_to_in_ref_total = spaces_to_in_ref + ref_format_len
               #format without spaces into
               acc_number_format = acc_number_format.ljust(spaces_to_in_acc_number_total)
               name_format = name_format.ljust(spaces_to_in_name_total)
               amount_format = amount_format.zfill(zeros_to_in_amount_total)
               ref_format = ref_format.ljust(spaces_to_in_ref_total)

               #format dic for layout *.txt
               dic = name_format + acc_number_format + amount_format + ref_format + date_format + f"\n"

               print(dic)

               file_layout_txt.write(dic)

           file_layout_txt.close()

           file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_mismo_banco.txt", "rb+")
           out = file_layout_txt.read()

           file_layout_txt.close()

           record.txt_layout_file = base64.b64encode(out)

           record.layout_name = 'layout_santander_mismo_banco.txt'

           record.write({'txt_layout_file': base64.b64encode(out), 'layout_name': 'layout_santander_mismo_banco.txt'})

           record.fecha_mod_layout = datetime.now()

        #Layout Santander a multiples bancos.

        if record.layout_type_bank == 'santander_multiples_bancos':
           file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_multiples_bancos.txt", "w+")
           #len's fields layout *.txt
           val_acc_number_origin_len = 16
           val_acc_number_destine_len = 20
           val_code_bank_destine_len = 5
           val_name_destine_len = 40
           val_amount_destine_len = 24
           val_amount_destine_integer_len = 17
           val_amount_destine_decimal_len = 7
           val_ref_destine_len = 130
           val_aplic_form_destine_len = 8
           ini_val_len = 0


           for line in record.relacion_pagos:

              if line.bank_id_name.name != 'SANTANDER':
               #formate len's
               acc_number_origin_format = str('65507540168')[ini_val_len:val_acc_number_origin_len]
               acc_number_destine_format = str(line.partner_bank_id.l10n_mx_edi_clabe)[ini_val_len:val_acc_number_destine_len]
               code_bank_destine = str(line.bank_id_name_code)[ini_val_len:val_code_bank_destine_len]
               name_destine_format = str(line.partner_id.name)[ini_val_len:val_name_destine_len]
               amount_destine_format = str("{:.2f}".format(line.amount))[ini_val_len:val_amount_destine_len]
               #Revisar
               list_x = []
               for l_ref in line.reconciled_bill_ids:
                   list_x.append(l_ref.uuid[0:8])

               print(tuple(list_x))
               ref_destine_format = str(list_x)[ini_val_len:val_ref_destine_len]
               aplic_form_destine_format = str('1')
               #count len's
               acc_number_origin_format_len = len(acc_number_origin_format)
               acc_number_destine_format_len = len(acc_number_destine_format)
               code_bank_destine_len = len(code_bank_destine)
               name_destine_format_len = len(name_destine_format)
               amount_destine_format_len = len(amount_destine_format)
               amount_decimal_search_character = amount_destine_format.find('.')
               amount_integer = amount_destine_format[ini_val_len:amount_decimal_search_character]
               amount_decimal = amount_destine_format[amount_decimal_search_character:amount_destine_format_len].replace('.','')
               amount_integer_fill = amount_integer.zfill(val_amount_destine_integer_len)
               amount_decimal_fill = amount_decimal.ljust(val_amount_destine_decimal_len,'0')
               #Concat Integers and decimals
               concat_amount = amount_integer_fill + amount_decimal_fill
               print(concat_amount)


               # Revisar
               ref_destine_format_len = len(ref_destine_format)
               aplic_form_destine_format_len = len(aplic_form_destine_format)

               #get difference between len's refer field and real field
               spaces_to_in_acc_number_origin = val_acc_number_origin_len - acc_number_origin_format_len
               spaces_to_in_acc_number_destine = val_acc_number_destine_len - acc_number_destine_format_len
               spaces_to_in_code_bank_destine = val_code_bank_destine_len - code_bank_destine_len
               spaces_to_in_name_destine = val_name_destine_len - name_destine_format_len
               spaces_to_in_ref_destine = val_ref_destine_len - ref_destine_format_len
               spaces_to_in_aplic_form_destine = val_aplic_form_destine_len - aplic_form_destine_format_len
               #Complete len's addition
               spaces_to_in_acc_number_origin_total = spaces_to_in_acc_number_origin + acc_number_origin_format_len
               spaces_to_in_acc_number_destine_total = spaces_to_in_acc_number_destine + acc_number_destine_format_len
               spaces_to_in_code_bank_destine_total = spaces_to_in_code_bank_destine + code_bank_destine_len
               spaces_to_in_name_destine_total = spaces_to_in_name_destine + name_destine_format_len

               spaces_to_in_ref_destine_total = spaces_to_in_ref_destine + ref_destine_format_len
               spaces_to_in_aplic_form_destine_total = spaces_to_in_aplic_form_destine + aplic_form_destine_format_len
               #formate with spaces or zeros
               acc_number_origin_format = acc_number_origin_format.ljust(spaces_to_in_acc_number_origin_total)
               acc_number_destine_format = acc_number_destine_format.ljust(spaces_to_in_acc_number_destine_total)
               code_bank_destine = code_bank_destine.ljust(spaces_to_in_code_bank_destine_total)
               name_destine_format = name_destine_format.ljust(spaces_to_in_name_destine_total)
               #Falta amount
               print()

               #Revisar
               ref_destine_format = ref_destine_format.ljust(spaces_to_in_ref_destine_total)
               aplic_form_destine_format = aplic_form_destine_format.rjust(spaces_to_in_aplic_form_destine_total)


               dic = acc_number_origin_format + acc_number_destine_format + code_bank_destine\
                     + name_destine_format + concat_amount + str(ref_destine_format) + aplic_form_destine_format + f"\n"

               file_layout_txt.write(dic)
               print('dic')
               print(dic)

           file_layout_txt.close()

           file_layout_txt = open("odoo/addons_custom/cuentas_por_pagar/temp/layout_santander_multiples_bancos.txt", "rb+")
           out = file_layout_txt.read()

           file_layout_txt.close()

           record.txt_layout_file = base64.b64encode(out)

           record.layout_name = 'layout_santander_multiples_bancos.txt'

           record.write({'txt_layout_file': base64.b64encode(out), 'layout_name': 'layout_santander_multiples_bancos.txt'})

           record.fecha_mod_layout = datetime.now()



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