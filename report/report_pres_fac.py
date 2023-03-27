# -*- coding:utf-8 -*-

from odoo import fields, models, api
#Listo
class PresupuestoFacExcel(models.AbstractModel):
    _name = 'report.cuentas_por_pagar.pres_fac_xls'
    _description = 'Reporte Presupuesto Por Factura (Productores)'
    _inherit = ['report.report_xlsx.abstract']

    @api.model
    def generate_xlsx_report(self, workbook, data,row_count):

        #Refresh view pagado_por_factura

        q_payments_tuple = """SELECT id FROM public.account_payment order by id asc"""

        self._cr.execute(q_payments_tuple)

        res_payments_tuple = self._cr.fetchall()

        # print(res_payments_tuple)
        list_tuple = []
        for line in res_payments_tuple:
            list_tuple.append(line[0])
        list_tuple = tuple(list_tuple)

        q_invoice_tuple = """SELECT id FROM public.account_move WHERE move_type = 'in_invoice' order by id asc"""

        self._cr.execute(q_invoice_tuple)

        res_invoice_tuple = self._cr.fetchall()

        # Add view partial payments

        q_partial_payments = """ CREATE OR REPLACE VIEW partial_payments AS SELECT ap.debit_move_id,ap.credit_move_id,ap.amount,account_move_line.move_id FROM public.account_partial_reconcile as ap
                                        left join account_move_line on ap.credit_move_id  = account_move_line.id
                                        ORDER BY debit_move_id desc;
                                     """
        self._cr.execute(q_partial_payments)

        # print(res_payments_tuple)
        list_tuple_invoice = []
        for line_invoice in res_invoice_tuple:
            list_tuple_invoice.append(line_invoice[0])
        list_tuple_invoice = tuple(list_tuple_invoice)

        q_view_payments_invoices = f"""CREATE OR REPLACE VIEW pagado AS SELECT 
                        payment.id as payment_id,
                        ARRAY_AGG(DISTINCT invoice.id) AS invoice_ids,
        				invoice.id as inv_id,
        				move.date as fechax,
                        invoice.move_type as move_type,
                        sum(part.amount) as amount
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
                        AND payment.id IN {list_tuple}
                        AND line.id != counterpart_line.id
                        AND invoice.move_type in ('in_invoice')
                    	AND invoice.id IN {list_tuple_invoice}
        			GROUP BY payment.id, invoice.move_type, invoice.id, fechax;
                    CREATE OR REPLACE VIEW pagado_por_factura AS 
                    select inv_id,sum(amount) as amount FROM public.pagado
                  
                    group by inv_id;
                    SELECT * FROM pagado_por_factura;"""

        self._cr.execute(q_view_payments_invoices)

        #Finish view pagado_por_factura


        for i in self.env['reportes_saldos_wizard'].search([], order='id desc', limit=1):
            # ordenar por nombre
            # lote_inicial_object.search([],order='name')
            i.presupuesto
        print('id_presupuesto')
        print(i.presupuesto.id)
        query = f"""
        select distinct(data_rel) as id,
        account_move.uuid as uuid,
        res_partner.name as name,
        case when  sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed) < 0 then 
        (case when  sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed) = 0
        then (select amount from pagado_por_factura where inv_id = data_rel) else sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed)
        end) * -1 else (case when  sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed) = 0
        then (select amount from pagado_por_factura where inv_id = data_rel) else sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed)
        end) end as amount_residual_signed
        from lotes_account_move_line
        left join account_move on lotes_account_move_line.data_rel = account_move.id
        left join res_partner on account_move.partner_id = res_partner.id
        where lotes_presupuestos_rel = {i.presupuesto.id}
        group by data_rel,account_move.uuid,res_partner.id 
        union all
        SELECT account_move.id,
        account_move.uuid as uuid,
        res_partner.name as name,
        case when  sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed) < 0 then 
        (case when  sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed) = 0
        then (select amount from pagado_por_factura where inv_id = account_move.id) else sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed)
        end) * -1 else (case when  sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed) = 0
        then (select amount from pagado_por_factura where inv_id = account_move.id) else sum(account_move.amount_residual_signed)/count(account_move.amount_residual_signed)
        end) end as amount_residual_signed
        FROM public.account_move
        left join res_partner on account_move.partner_id = res_partner.id
        where presupuesto_lote_fac_adic_rel = {i.presupuesto.id}
        group by account_move.id,account_move.uuid,res_partner.id
        order by id asc
        """
        self._cr.execute(query)
        result = self._cr.fetchall()
        print('Ressssss')
        print(result)
        row_count = 0
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', })
        sheet = workbook.add_worksheet('Reporte 1')
        for lines in result:
            row_count = row_count + 1
            sheet.set_column(3, 3, 50)
            sheet.set_column(2, 2, 30)
            sheet.write(0, 0, 'Id', format1)
            sheet.write(row_count, 0, lines[0], format2)
            sheet.write(0, 1, 'Uuid', format1)
            sheet.write(row_count, 1, lines[1], format2)
            sheet.write(0, 2, 'Proveedor', format1)
            sheet.write(row_count, 2, lines[2], format2)
            sheet.write(0, 3, 'Importe', format1)
            sheet.write(row_count, 3, lines[3], format2)