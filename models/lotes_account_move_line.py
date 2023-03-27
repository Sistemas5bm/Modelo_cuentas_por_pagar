# -*- coding:utf-8 -*-how save many2many custom more data
from datetime import datetime
from time import strftime
import logging
from odoo import fields, models, api, _
import pandas as pd
from datetime import date,timedelta

from odoo.exceptions import UserError
logger = logging.getLogger(__name__)

class LotesCfdi(models.Model):
    _name = "lotes_account_move_line"
    _description = "Linea de factura con lotes"
    name = fields.Many2one(comodel_name='lotes',string='Lote', required=True)
    lotes_fecha_recepcion = fields.Date(string='Fecha Recepcion',related='name.fecha',store=True)
    lotes_nombre_productor = fields.Many2one(related='name.id_partner')
    lotes_huerta = fields.Many2one(related='name.sader')
    abono_kilogramos = fields.Float(string='Abono Kg')
#este es compute
    abono_importe = fields.Float(string='Abono Importe',compute='_compute_abono_importe')
    lotes_saldo_pendiente = fields.Float(string='Importe pendiente',related='name.saldo_pendiente',compute='_compute_kg_pendientes')
#este es compute
    lotes_kilogramos_pendiente = fields.Float(string='Kg Pendientes',related='name.kilogramos_pendientes',store=True,compute='_compute_kg_pendientes')
    metodo_pago = fields.Char(related='data_rel.metodo_pago')
    forma_de_pago = fields.Char(related='data_rel.forma_de_pago')
    lotes_kilogramos = fields.Float(string='Kilogramos Lote',related='name.cantidad',compute='_compute_kg_pendientes')
    lotes_importe = fields.Float(string='Importe Lote',related='name.importe')
    lotes_sader = fields.Many2one(string='Sader',related='name.sader')
    lotes_sader_code = fields.Char(string='Sader Codigo', related='name.sader.sader')
    lotes_jefe_acopio = fields.Many2one(string='Jefe Acopio', related='name.jefe_acopio')
    #verificar_contrato
    lotes_sader_contrato = fields.One2many(string='Contratos', related='name.sader.contrato_terceros_lista')
    lotes_precio_unitario = fields.Float(string='Precio Unitario Lote',related='name.precio_u')
    lotes_observaciones = fields.Char(string='Observaciones',related='name.observaciones')
    cfdi_id_rel = fields.Many2one(string='Cfdi',comodel_name='account.move')
    lotes_id_rel = fields.Many2one(string='Lotes id Rel', comodel_name='lotes')
    status_pago_rel = fields.Char(string='Estatus Pago',related='name.status_pago')
    data_rel = fields.Many2one(comodel_name='account.move',string='Data Rel',index=True,required=True,readonly=True, auto_join=True, ondelete="cascade",_rec_name='uuid')
    serie = fields.Char(related='data_rel.serie')
    folio = fields.Char(related='data_rel.folio')
    uuid = fields.Char(related='data_rel.uuid',store=True)
    id_factura = fields.Integer(related='data_rel.id')
    id_partner = fields.Many2one(related='data_rel.partner_id',string='Emisor de factura',store=True)
    fecha_factura = fields.Date(related='data_rel.invoice_date',string='Fecha Factura')
    fecha_pago = fields.Date(related='data_rel.invoice_date_due',string='Fecha De Vencimiento')
    estado_pago = fields.Selection(related='data_rel.state',string='Estado Factura')
    estado_factura = fields.Selection(related='data_rel.payment_state',string='Estado Pago')
    estado_contabilizacion = fields.Selection(string='Estado Contabilizacion',related='name.state')
    provision_lote = fields.Char(string='Provision Lote',related='name.status_provision',store=True,readonly=True)
    impuesto = fields.Char(string='Retencion',compute='calcularCampos_Impuestos')
    abono_importe_con_impuesto = fields.Float(string='Abono Importe - Ret', compute='calcularCampos_Impuestos')
    abono_importe_con_impuesto_db = fields.Float(string='Abono Importe data base')
    estatus_contratos = fields.Char(string='Etatus Contrato',compute='get_contracts_data')
    es_tarjeta_apeam = fields.Boolean(string='Tarjeta Apeam',compute='get_documental_data')
    #revisar
    es_opinion = fields.Char(string='OPINION',compute='get_aditional_data')
    es_ine = fields.Boolean(string='INE',compute='get_aditional_data')
    es_cif = fields.Char(string='CSF',compute='get_aditional_data')
    #aqui revisar
    estatus_layout = fields.Char(string='Estatus Layout')
    #rep_imp_pagado = fields.Float(string='Imp Pagado REPS',compute='get_sum_imp_pagado')
    rep_imp_por_pagar = fields.Float(string='Imp Por Pagar REPS',compute='get_sum_imp_pagado')
    res = fields.Char(compute='search_date',string='Total')
    fecha_pago_tuple = fields.Char(compute='get_payments_ids',string='Fecha Pago')
    id_pago = fields.Char(string='Id Pago',compute='get_payments_ids')
    state_special = fields.Selection(string='Estado Marca',selection=[
        ('check_freeze', 'Congelado'),
        ('check_freeze_invert', 'Default'),

    ],copy=False, tracking=True, track_visibility='always', readonly=True,store=True)

    lotes_presupuestos_rel = fields.Many2one(comodel_name='presupuesto_lotes')

    lotes_status_lock = fields.Selection(string='Estado De Bloqueo', selection=[
        ('lock', 'Bloqueado'),
        ('unlock', 'Desbloqueado'),

    ], copy=False, tracking=True, track_visibility='always', readonly=True, store=True)

    reporte_saldos_lotes_line_rel = fields.Many2one('reporte_saldos',string='Reporte Saldos Lotes Line Rel')

    ine_data = fields.Char(string='Ine Data')
    #Vencimiento del ine
    ine_venc = fields.Char(string='INE VENC',compute='get_ine')

    #account_partner_bank = fields.Boolean(string='Cta Banco', compute='get_account_partner_bank_status')

    contrato_bym_resparnet = fields.Char(string='Contrato B&M', compute='_contrato_bym_rel')
    contrato_bym_rel = fields.One2many('res.partner', 'relacion_contrato_bym')
    #rel_tes = fields.Many2one('res.partner')
    chack_cuenta_decault_lotes = fields.Boolean(string='Cta Banco', compute='get_account_partner_bank_status', default=False)

    #rel_purchase_order = fields.Many2many('purchase.order')

    def _contrato_bym_rel(self):
        for line in self:
            line.contrato_bym_resparnet = 'NO DOCTO'
            for rec in line.id_partner:
                for rec2 in rec.contratos_bym_rel:
                    fecha_inicial = rec2.fecha_apertura
                    vencimiento = rec2.fecha_vencimiento
                    fecha_actual = fields.Date.today()
                    vencimiento_acum = fecha_actual
                    if vencimiento is not False:
                        if vencimiento >= line.lotes_fecha_recepcion and fecha_inicial <= line.lotes_fecha_recepcion:
                            line.contrato_bym_resparnet = 'VIGENTE'
                        else:
                            line.contrato_bym_resparnet = 'VENCIDO'
                            vencimiento_acum = vencimiento
                    if vencimiento_acum >= fecha_actual and fecha_inicial <= line.lotes_fecha_recepcion:
                        line.contrato_bym_resparnet = 'VIGENTE'
            if line.lotes_nombre_productor.name == line.id_partner.name:
                line.contrato_bym_resparnet = 'NO APLICA'

    def get_account_partner_bank_status(self):
        for l in self:


            for recordl in l.data_rel:
                l.chack_cuenta_decault_lotes =False
                for recordl2 in recordl.partner_id:
                    for recordl3 in recordl2.bank_ids:
                        account_exists = l.env['res.partner.bank'].search_count([('partner_id', '=', l.id_partner.id)])
                        if account_exists > 0:
                            found_checks = recordl3.env['res.partner.bank'].search_count([('check', '=', True),
                                                                                          ('partner_id', '=',
                                                                                           recordl3.partner_id.id)])
                            if found_checks == 0:
                                l.chack_cuenta_decault_lotes = False
                            if found_checks >= 1:
                                l.chack_cuenta_decault_lotes = True

                        if account_exists <= 0:
                            l.chack_cuenta_decault_lotes = False


    def get_ine(self):
        for l in self:
            l.ine_venc = ' '
            #contador en 0's
            contador = 1
            #mapeo el modelo en un objeto
            ines_vigentes = l.env['ine_sat']
            # variable de control para fecha
            var_control_date = ''
            if l.estado_factura == 'paid':
               var_control_date = l.fecha_pago_tuple
               var_control_date = var_control_date.replace('(', '')
               var_control_date = var_control_date.replace(')', '')
               var_control_date = var_control_date[0:10]
               if var_control_date.count('-') >= 3:
                  var_control_date = str(var_control_date[0:4])

            print(var_control_date)
            if l.estado_factura != 'paid':
                var_control_date = str(date.today())
            #Revisar resultados finales
            l.ine_venc = 'NO DOCTO'
            for i in ines_vigentes.search([('ine_partner_rel','=',l.data_rel.partner_id.id)], order='id desc'):
                format_date = str(i.fecha_vencimiento)

                if format_date[0:4] >= var_control_date[0:4] and i.fecha_vencimiento is not False:
                    contador = contador + 2
                else:
                    contador = contador + 1
            contador = contador
            if contador >= 3:
                l.ine_venc = 'VIGENTE'

            if contador==2:
                l.ine_venc = 'VENCIDO'



    def put_check_freeze(self):
        for l in self:
            print('x')
            l.state_special = 'check_freeze'
    def put_check_freeze_invert(self):
        for l in self:
            l.state_special = 'check_freeze_invert'

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
                'active_ids': self.data_rel.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    def write(self, variables):
        logger.info('write variables : {0}'.format(variables))
        # Lee si la fecha contrato ya ha sido creada y no permite modificarla despues de haberla creado
        if 'estado_factura' == 'paid':
            # se manda un error
            raise UserError('El lote no se puede editar por que ya se encuentra en estado de pagado')

        if 'lotes_status_lock' == 'lock':
            # se manda un error
            raise UserError('El lote no se puede editar por que ya se encuentra en estado de presupuestado')
        # se graba el diccionario en la bd
        return super(LotesCfdi, self).write(variables)
    """
    def unlink(self):
        logger.info('Se disparo la funcion unlink')
        for record in self:
         if record.estado_factura == 'not_paid' and record.lotes_status_lock == 'unlock':
            super(LotesCfdi, record).unlink()
         else:
            raise UserError('No se puede eliminar el registro por que el lote esta pagado / presupuestado')
    """

    def get_payments_ids(self):
        for l in self:
            m = l.env['account.move'].search([('id','=',l.id_factura)]).recn
            id_pagox = l.env['account.move'].search([('id', '=', l.id_factura)]).id_pagos
            l.fecha_pago_tuple = m
            l.id_pago = id_pagox


    def search_date(self):
        for line in self:
            line.res = 'x'
            print('this')
            print(line.data_rel)

    def get_sum_imp_pagado(self):
        for line in self:
            sum_importe_pagado_rep = sum(line.env['pagos_doctos_rel'].search([('id_documento',"ilike",line.uuid)]).mapped('imp_pagado'))
            line.rep_imp_pagado = sum_importe_pagado_rep


    #trae los datos documentales del proveedor a traves de la relacion factura "data_rel"
    def get_aditional_data(self):
        for line in self:
            #calcula las opiniones que estan el rango de fecha de la factura relacionada "data_rel"
            x = line.env['opinion_cumplimiento_sat'].search([('opinion_cumplimiento_partner_rel','=',line.data_rel.partner_id.id)]).mapped("fecha_emision")
            fecha_factura = pd.to_datetime(line.data_rel.invoice_date)
            mes_factura = fecha_factura.strftime('%b')
            contador_vigencias = 0
            status = ' '
            print(x,'es equis')
            if x ==[]:
                status = 'NO DOCTO'
            for linx in x:

                mes_contrato = linx.strftime('%b')
                print('Diferencia')
                diff = int((pd.to_datetime(fecha_factura) - pd.to_datetime(linx)).days)
                print(diff)
                if mes_factura == mes_contrato or diff < 0 or diff <= (90):
                    contador_vigencias = contador_vigencias + 1
                    if contador_vigencias == 0:
                        status = 'VENCIDO'
                    if contador_vigencias > 0:
                        status = 'VIGENTE'

                else:
                    contador_vigencias = contador_vigencias + 1
                    if contador_vigencias == 1:
                        status = 'VENCIDO'
                    if contador_vigencias > 1:
                        status = 'VIGENTE'
                if status == ' ':
                    status = 'NO DOCTO'
            line.es_opinion = status

            #calcula qty de ines vigentes o vencidas
            calcular_ines = line.env['ine_sat'].search_count([('ine_partner_rel','=',line.data_rel.partner_id.id)])
            if calcular_ines >= 1:
                line.es_ine = True
            if calcular_ines < 1:
                line.es_ine = False
            #calcula las caratulas que estan el rango de fecha de la factura relacionada "data_rel"
            qty_cifs = line.env['cif'].search([('cif_rel', '=', line.data_rel.partner_id.id)]).mapped('fecha_emision')
            fecha_factura = pd.to_datetime(line.data_rel.invoice_date)
            mes_factura = fecha_factura.strftime('%b')
            contador_vigencias = 0
            status = ' '
            if qty_cifs == []:
                status = 'NO DOCTO'
            for linx in qty_cifs:
                mes_contrato = linx
                mes_contrato = mes_contrato.strftime('%b')
                print('Otro parametro que ocupo ver')
                print(mes_contrato)
                print('Diferencia')
                diff = int((pd.to_datetime(fecha_factura) - pd.to_datetime(linx)).days)
                print(diff)
                if mes_factura == mes_contrato or diff < 0 or diff <= (90):
                    contador_vigencias = contador_vigencias + 1
                    if contador_vigencias == 0:
                        status = 'VENCIDO'
                    if contador_vigencias > 0:
                        status = 'VIGENTE'

                else:
                    contador_vigencias = contador_vigencias + 0
                    if contador_vigencias == 0:
                        status = 'VENCIDO'
                    if contador_vigencias > 0:
                        status = 'VIGENTE'
            line.es_cif = status


    def get_documental_data(self):
        for line in self:
            #Busca la tarjeta APEAM
            line.es_tarjeta_apeam = line.env["huertas"].search([('id', '=', line.name.sader.id)]).es_tarjeta_apeam
            #Busca la OPINION DE CUMPLIMIENTO


    def get_contracts_data(self):
        for line in self:
            busqueda_vigencias = line.env["huertas_contratos_terceros"].search_count([('huertas_contratos_terceros_huertas_rel', '=', line.name.sader.id),('fecha_vencimiento','>=',line.lotes_fecha_recepcion),
                                                                                      ('fecha_apertura','<=',line.lotes_fecha_recepcion)])
            x = line.env["huertas_contratos_terceros"].search(
                [('huertas_contratos_terceros_huertas_rel', '=', line.name.sader.id),
                 ('fecha_vencimiento', '>=', line.lotes_fecha_recepcion),
                 ('fecha_apertura','<=',line.lotes_fecha_recepcion)])
            print('****busqueda vigencias******')
            print(busqueda_vigencias)
            print(x,' es X')
            print('**********Contador de lista beneficiarios************')
            validator_count = 0

            busqueda_vigencias2 = line.env["huertas_contratos_terceros"].search_count(
                [('huertas_contratos_terceros_huertas_rel', '=', line.name.sader.id)])
            print(busqueda_vigencias2,'prueba 1')



            for lnx in x:
                for lnx_benef in lnx.beneficiarios:
                    if lnx_benef.id == line.data_rel.partner_id.id:
                        validator_count = validator_count + 1
                    if lnx_benef.id != line.data_rel.partner_id.id:
                        validator_count = validator_count + 0
            print(validator_count)

            if busqueda_vigencias <= 0:
               line.estatus_contratos = 'VENCIDO'
            if busqueda_vigencias > 0:
                if validator_count > 0:
                   line.estatus_contratos = 'VIGENTE'
                else:
                    line.estatus_contratos = 'VENCIDO'


            if busqueda_vigencias2 <= 0:
                line.estatus_contratos = 'NO DOCTO'
            if line.data_rel.partner_id.name == line.lotes_nombre_productor.name:
                line.estatus_contratos = 'NO APLICA'





    def name_get(self):
        result = []
        for record in self:
            record_name = f'{record.uuid} \n {record.id_partner.name} \n {record.serie} \n {record.folio} \n {record.fecha_factura} \n {record.estado_pago}'
            result.append((record.id, record_name))
        return result


    def contabilizar_lote(self):
        for line in self:
         line.name.state = 'Contabilizado Lote'

    def contabilizar_cfdi(self):
        for line in self:
         line.name.state = 'Contabilizado Cfdi'


    def convertir_a_borrador(self):
        for line in self:
         line.name.state = 'borrador'

    #es para cuando recien selecciona el lote (calculo inicial)
    @api.onchange('name')
    @api.depends('name')
    def _compute_kg_pendientes(self):

       # recorro todos los datos de la funcion
       for lote in self:

        #suma de abono de kilogramos
        records_sum = sum(lote.env["lotes_account_move_line"].search([('name','=',lote.name.id)]).mapped('abono_kilogramos'))
        kilogramos_pendientes = sum(lote.env["lotes_account_move_line"].search([('name','=',lote.name.id)]).mapped('lotes_kilogramos_pendiente'))

        lote.abono_kilogramos = lote.lotes_kilogramos - records_sum

        lote.lotes_kilogramos_pendiente = lote.lotes_kilogramos - records_sum
        lote.lotes_saldo_pendiente = lote.lotes_kilogramos_pendiente * lote.lotes_precio_unitario


    #este esta bien
    @api.onchange('abono_kilogramos')
    def _compute_abono_importe(self):
       for lote in self:
        # campo abono importe compute
        records_sum = 0

        records_sum = sum(lote.env["lotes_account_move_line"].search([('name','=',lote.name.id)]).mapped('abono_kilogramos'))

        if records_sum == lote.lotes_kilogramos:
            lote.lotes_kilogramos_pendiente = 0
            lote.lotes_saldo_pendiente = 0
            lote.abono_importe = lote.abono_kilogramos * lote.lotes_precio_unitario
        if records_sum < lote.lotes_kilogramos:
            lote.lotes_kilogramos_pendiente = (lote.lotes_kilogramos - records_sum) - (lote.abono_kilogramos)
            lote.lotes_saldo_pendiente = lote.lotes_kilogramos_pendiente * lote.lotes_precio_unitario
            lote.abono_importe = lote.abono_kilogramos * lote.lotes_precio_unitario






    @api.depends('impuesto','abono_importe_con_impuesto','data_rel')
    def calcularCampos_Impuestos(self):
        for line in self:

            #Agregar resultado nulo por si el dato no existe
            amount_untaxed_calc = 0.0
            amount_total_calc = 0.0
            impuestos_retenidos = 0.0


            if line.data_rel.id:
                #print('SI EXISTE RELACION')
                amount_untaxed_calc = sum(line.env["account.move"].search([('id', '=', line.data_rel.id)]).mapped('amount_untaxed'))
                amount_total_calc = sum(line.env["account.move"].search([('id', '=', line.data_rel.id)]).mapped('amount_total'))
                impuestos_retenidos = sum(line.env["account.move"].search([('id', '=', line.data_rel.id)]).mapped('total_impuestos_retenidos'))

            if not line.data_rel.id:
                #print('NO EXISTE RELACION')
                amount_untaxed_calc = 0.0
                amount_total_calc = 0.0
            #print(amount_total_calc)
            #print(amount_untaxed_calc)
            ref_impuesto = ''
            abono_importe_calc = 0.0

            if impuestos_retenidos is None:
                ref_impuesto = ''
                abono_importe_calc = 0
            if  impuestos_retenidos is None:
                ref_impuesto = ''
                abono_importe_calc = 0
            if impuestos_retenidos > 0:
                ref_impuesto = 'ISR 1.25%'
                abono_importe_calc = (line.abono_importe) - (line.abono_importe * 0.0125)
            if impuestos_retenidos <= 0:
                ref_impuesto = 'TASA 0'
                abono_importe_calc = line.abono_importe

            line.impuesto = ref_impuesto
            line.abono_importe_con_impuesto = abono_importe_calc
            line.abono_importe_con_impuesto_db = abono_importe_calc









