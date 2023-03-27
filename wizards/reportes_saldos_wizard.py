# -*- coding:utf-8 -*-

from odoo import fields, models, api
from datetime import datetime

class SaldosWizard(models.TransientModel):


    _name = "reportes_saldos_wizard"

    #_inherit = 'account.move'
    name = fields.Char(string='Name',default='Busqueda')

    date_start = fields.Date(string='Fecha Inicial',default=datetime.today())

    date_type = fields.Selection(selection=[
        ('fecha_lote', 'Fecha Lote'),
        ('fecha_factura', 'Fecha Factura'),
        ('fecha_pago','Fecha de pago'),

    ], default='fecha_lote', string='Busqueda por fecha: ', copy=False, tracking=True, track_visibility='always',
        store=True)

    date_end = fields.Date(string='Fecha Final',default=datetime.today())

    productor_id = fields.Many2one('res.partner',string='Proveedor')

    pagado_flete = fields.Selection(string='Estatus', selection=[('pagado', 'Pagado'),('no_pagado','No pagado'),
                                                                ('sin_factura','Sin facturar')],track_visibility='always'
                                    ,default='pagado')

    provider_type = fields.Selection(selection=[
        ('todo', 'Todo'),
        ('productor', 'Por Productor'),
        ('emisor', 'Por Emisor'),
        ('presupuesto','Presupuesto'),

    ], default='todo', string='Busqueda por: ', copy=False, tracking=True, track_visibility='always',
        store=True)

    presupuesto = fields.Many2one('presupuesto_lotes',string='Presupuesto #')

    presupuesto_fletes = fields.Many2one('presupuesto_flete', string='Presupuesto flete #')

    def print_no_facturado(self):
        return self.env.ref('cuentas_por_pagar.report_estado_cuenta_card').report_action(self)
    def print_no_facturado_xls(self):
        return self.env.ref('cuentas_por_pagar.report_estado_cuenta_card_xls').report_action(self)
    def print_facturado_no_pagado(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_facturado_no_pagado').report_action(self)
    def print_facturado_no_pagado_xls(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_facturado_no_pagado_xls').report_action(self)
    #saldo de proveedor
    def print3(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_fac_no_pag_no_fac_no_pag').report_action(self)
    #saldo de proveedor
    def print3_xls(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_fac_no_pag_no_fac_no_pag_xls').report_action(self)
    def print_fact_no_pagado_datelle(self):
        self.date_start = super(SaldosWizard, self).browse(self.id).date_start
        print(self.date_start)
        self.date_end = super(SaldosWizard, self).browse(self.id).date_end
        print(self.date_end)
        return self.env.ref('cuentas_por_pagar.report_lotes_fac_no_pag_detail').report_action(self)
    def print_fact_no_pagado_datelle_xls(self):
        self.date_start = super(SaldosWizard, self).browse(self.id).date_start
        print(self.date_start)
        self.date_end = super(SaldosWizard, self).browse(self.id).date_end
        print(self.date_end)
        return self.env.ref('cuentas_por_pagar.report_lotes_fac_no_pag_detail_xls').report_action(self)
    def print_no_fac_datelle(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_no_fac_detall').report_action(self)

    def print_no_fac_datelle_xls(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_no_fac_detall_xls').report_action(self)
    def print_pagado(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_pagado').report_action(self)
    def print_pagado_xls(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_pagado_xls').report_action(self)
    def print_pagado_prod(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_pagado_prod').report_action(self)
    def print_pagado_prod_xls(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_pagado_prod_xls').report_action(self)
    def print_pagado_prod_det(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_pagado_prod_det').report_action(self)
    def print_pagado_prod_det_xls(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_pagado_prod_det_xls').report_action(self)
    def print_pagado_emi_det(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_pagado_emi_det').report_action(self)
    def print_pagado_emi_det_xls(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_pagado_emi_det_xls').report_action(self)
    #Reporte de presupuesto por fctura
    def print_pres_xls(self):
        return self.env.ref('cuentas_por_pagar.report_pres_fac_xls').report_action(self)
    def print_pres_pdf(self):
        return self.env.ref('cuentas_por_pagar.report_pres_fac').report_action(self)
    def print_fleteros_pdf(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_fleteros').report_action(self)
    def print_reporte_pagos_fleteros_pdf(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_fleteros2').report_action(self)
    def print_reporte_feltes_facturas_pdf(self):
        return self.env.ref('cuentas_por_pagar.report_lotes_fleteros3').report_action(self)
    def print_report_presupuesto_fletes_pdf(self):
        return self.env.ref('cuentas_por_pagar.report_presupuesto_fletes').report_action(self)
    def print_report_presupuesto_fletes_xls(self):
        print('butoon')
    @api.model_create_multi
    def create(self,vals):
        rec = super(SaldosWizard,self).create(vals)
        return rec