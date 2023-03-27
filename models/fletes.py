# -*- coding:utf-8 -*-
import requests
from odoo import fields, models, api
import sqlalchemy as sa
import pandas as pd
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String, Float, SmallInteger, Numeric, DateTime, Date
from datetime import date, timedelta
from sqlalchemy import distinct
import logging

_logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

Base = declarative_base()


# Clase de movimientos de recepcion
class CortesDataOrden(Base):
    __tablename__ = 'REP_OrdenesCorte2'
    id_orden_corte = Column('IdOrdenCorte', Integer(), primary_key=True)
    fecha = Column('Fecha', DateTime)
    sader = Column('NoRegistro', String(500))
    huerta = Column('Huerta', String(500))
    ubicacion = Column('Ubicacion', String(500))
    poblacion = Column('Poblacion', String(500))
    estado = Column('Estado', String(500))
    municipio = Column('Municipio', String(500))
    status = Column('Status', String(500))
    nombre_productor = Column('Productor', String(500))
    nombre_transportista = Column('Transportista', String(500))
    nombre_jefe_cuadrilla = Column('JefeCuadrilla', String(500))
    observaciones = Column('Observaciones', String(500))


class CortesCajasTTS(Base):
    __tablename__ = 'View_datos_camion2'
    id_orden_corte_cajas = Column('IdOrdenCorte', Integer(), primary_key=True)
    id_cajas_cortadas = Column('CajasCortadas', Integer())
    fecha = Column('Fecha', DateTime)
    cajas_entregadas = Column('CajasMixto', Integer())
    ticket = Column('Ticket', String(200))
    pesototal = Column('PesoNeto', Integer())


class Session():
    def session(engine):
        Session = sessionmaker(bind=engine)
        # session = Session()
        session = scoped_session(Session)

        return session

    def engine():
        server_addres = '192.168.88.214' + ":" + "49703"
        #server_addres = 'e3210dfde5c7.sn.mynetname.net' + ":" + "49703"
        database = 'TTS'
        username = 'sa'
        password = 'HideMyPassBm123*'

        arguments = dict(server=server_addres, user=username,
                         password=password, database=database, charset="utf8")

        engine = sa.create_engine('mssql+pymssql:///', connect_args=arguments)
        return engine

    # Modelo de odoo


class FletesCrear(models.Model):
    _name = "fletes_modelo_tts"

    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Id orden corte', tracking=True, track_visibility='always')

    fecha = fields.Date(string='Fecha', tracking=True, track_visibility='always')

    # Un Many2one siempre recibe un entero
    huerta = fields.Many2one(comodel_name='huertas', string='Huerta', tracking=True, track_visibility='always')

    ubicacion_municipio = fields.Many2one(comodel_name='localidad', string='Localidad', tracking=True,
                                          track_visibility='always')

    poblacion = fields.Many2one(comodel_name='poblacion', string='Poblacion', tracking=True, track_visibility='always')

    estado = fields.Many2one(comodel_name='estado', string='Estado', tracking=True, track_visibility='always')

    municipio = fields.Many2one(comodel_name='ciudad', string='Municipio', tracking=True, track_visibility='always')
    municipio_pdf = fields.Char(realeated='municipio.name', store=True)

    status = fields.Char(string='Status fruta', tracking=True, track_visibility='always')

    nombre_produtor_modelo_tts = fields.Many2one(comodel_name='res.partner', string='Nombre productor', tracking=True,
                                                 track_visibility='always')

    nombre_transportista = fields.Many2one(comodel_name='res.partner', string='Nombre transportista', tracking=True,
                                           track_visibility='always')

    nombre_jefe_cuadrilla = fields.Many2one(comodel_name='res.partner', string='Jefe de cuadrilla', tracking=True,
                                            track_visibility='always')

    observaciones = fields.Text(string='Observaciones', tracking=True, track_visibility='always')

    impuestos = fields.One2many('retenciones', 'fletes_rel', string='EXTRAS', tracking=True,
                                track_visibility='always', store=True)

    importe_total_fletes_municipio = fields.Float(string='Importe municipio', compute='_compute_tarifa_final_fleteo',
                                                  tracking=True, track_visibility='always',
                                                  store=True)  # valor extraido de tarifas municipios ya con impuestos
    total_tarifa_inicial = fields.Float(string='Total tarifa', related='importe_total_fletes_municipio')
    importe_tarifa_inicial = fields.Float(string='Tarifa inicial de municipios',
                                          store=True, )  # valor extraido de tarifas municipios sin impuestos
    total_tarifa_inicial2 = fields.Float(string='Total tarifa')
    importe_mas_retencion = fields.Float(string='Importe a pagar')

    base_tarifa = fields.Float(string='Sub total')

    desgloce_iva = fields.Float(string='IVA (+)', compute='_compute_tarifa_final_fleteo')
    desgloce_retencion = fields.Float(string='Retencion IVA (-)', compute='_compute_tarifa_final_fleteo')
    desgloce_resico = fields.Float(string='ISR-Resico')

    importe_mas_retencion2 = fields.Float(
        string='Tarifa final sin modificar')  # campo creado para calculo en presupuesto flete

    beneficiario = fields.Many2one(related='nombre_transportista.beneficiario_flete', string='Beneficiario',
                                   tracking=True, track_visibility='always', store=True)
    beneficiario_pdf = fields.Char(related='nombre_transportista.beneficiario_flete.name')

    cajas_lote_fletes = fields.Integer(string='Cajas lote')

    cajas_mixtos_fletes = fields.Integer(string='Cajas en camion')

    state_fletes = fields.Selection(selection=[('borrador', 'Borrador'), ('aprobado_cfdi', 'Contabilizado CFDI'),
                                               ('bloqueo', 'bloqueo'), ]
                                    , default='borrador', string='Contabilizado CFDI', copy=False)

    peso_promedio_caja = fields.Float(string='Peso promedio cajas', )

    state = fields.Selection(selection=[('alerta_exeso', 'Exceso'), ('alerta_faltante', 'Faltante'),
                                        ('margen', 'margen'), ('bloqueo', 'Bloqueo')]
                             , default='margen', string='Estados', copy=False, )
    peso_producto = fields.Float(string='Peso productor')

    alerta_peso_cajas = fields.Char(string='Alerta de Peso')

    data_rel = fields.Many2one(default=None, comodel_name='account.move', string='Data Rel', index=True, auto_join=True,
                               ondelete="cascade", _rec_name='uuid')
    ine_venc = fields.Char(string='INE VENC', compute='get_ine')

    es_ine = fields.Char(string='INE', compute='relacion_facturador_flete')

    es_cif = fields.Char(string='CSF', compute='relacion_facturador_flete')

    es_opinion = fields.Char(string='OPINION', compute='relacion_facturador_flete')

    carta_porte = fields.Boolean(string='Carta porte')

    rel_fletes_pagos = fields.Many2one('pagos_layout')

    extras_one2many = fields.Float(string='Extras one2many')

    relacion_fletes_factutas = fields.Many2one('account.move', ondelete="cascade")

    fletes_presupuestos_rel = fields.One2many('presupuesto_flete', 'fletes_provisionados', ondelete="cascade")

    contrato_fletes_bym = fields.Char(string='Contrato', compute='relacion_facturador')
    data_rel_acount = fields.Many2one('lotes_account_move_line')

    resico = fields.Boolean()

    uuid = fields.Char(string='UUID', store=True)
    fecha_factura = fields.Char(string='Fecha factura', store=True)
    fecha_pago = fields.Date()
    estado_pago = fields.Char(string='Estado pago')
    provedor_factura = fields.Char(string='Emisor de factura', store=True)
    provedor_factura_id = fields.Integer(string='Id facturador', store=True)

    chack_cuenta_decault_fletes = fields.Boolean(string='Cuenta Banco', compuete='relacion_facturador_flete')

    relacion_layout = fields.Many2one('pagos_layout_fletes')

    regimen_resico = fields.Boolean(string='Resico')

    importe_factura = fields.Float(string='Importe factura', compute='import_fact')

    # estado_pago = fields.Char(string='Pago concepto',)# compute='concepto_factura')
    estado_pago_selection = fields.Selection(related='relacion_fletes_factutas.payment_state', string='Pago estado',
                                             store=True)
    # web_ribbon = fields.Selection(selection=([('paid','PAGADO'),('not_paid','NO PAGADO')]),string='ribbon', related='relacion_fletes_factutas.payment_state')
    account_payment_rel = fields.Many2one('account_payment')

    bloqueo_seleccion_presupuesto = fields.Boolean(
        default=False)  # evita que se ocupe un registro mas de una ves en presupuesto

    impuesto_iva = fields.Float(string='Impuesto IVA', compute='import_fact')

    impuesto_isrr_retenido = fields.Float(string='ISRR Retenido', compute='import_fact')

    impuesto_ieps_traslado = fields.Float(string='IEPS Traslado', compute='import_fact')

    impuesto_iva_retenido = fields.Float(string='IVA Retenido', compute='import_fact')

    impuesto_traslado = fields.Float(string='Impuesto traslado', compute='import_fact')

    impuesto_retenciones = fields.Float(string='Retenciones', compute='import_fact')

    isr_trasladado = fields.Float(string='ISR Traslados', compute='import_fact')

    ieps_retenido = fields.Float(string='IEPS Retenido', compute='import_fact')

    conceptos = fields.Char(string='Conceptos', compute='import_fact')

    diferencia_total = fields.Float(string='Impuesto', compute='import_fact')

    rel_presupuesto_flete = fields.Many2one('presupuesto_flete', string='Relacion con presupuesto flete')

    def concepto_factura(self):
        for concepto in self:
            concepto.r

    # extrae datos de facturas y los muestra en fletes mediante la relacion relacion_fletes_factutas
    def import_fact(self):
        for rec_fact in self:

            rec_fact.importe_factura = 0.0
            suma = 0.0
            lista = []
            cadena = ''
            rec_fact.impuesto_iva = 0.0
            rec_fact.impuesto_isrr_retenido = 0.0
            rec_fact.impuesto_ieps_traslado = 0.0
            rec_fact.impuesto_iva_retenido = 0.0
            rec_fact.impuesto_traslado = 0.0
            rec_fact.impuesto_retenciones = 0.0
            rec_fact.isr_trasladado = 0.0
            rec_fact.ieps_retenido = 0.0
            rec_fact.conceptos = ' '
            rec_fact.diferencia_total = 0.0
            for rec in rec_fact.relacion_fletes_factutas:
                # desglosa el importe de factura
                rec_fact.impuesto_iva = rec.impuesto_iva
                rec_fact.impuesto_isrr_retenido = rec.impuesto_isrr_retenido
                rec_fact.impuesto_ieps_traslado = rec.impuesto_ieps_traslado
                rec_fact.impuesto_iva_retenido = rec.impuesto_iva_retenido
                rec_fact.impuesto_traslado = rec.impuesto_traslado
                rec_fact.impuesto_retenciones = rec.impuesto_retenciones
                rec_fact.isr_trasladado = rec.isr_trasladado
                rec_fact.ieps_retenido = rec.ieps_retenido
                rec_fact.conceptos = rec.conceptos
                rec_fact.diferencia_total = rec.diferencia_total
                cadena = rec.id_pagos_db
                if cadena is not False:

                    lista = cadena.split(',')
                    if cadena != '':
                        lista = cadena.split(',')
                        vals = []
                        for line1 in lista:
                            tes1 = line1.replace('[', '')
                            tes2 = tes1.replace(',', '')
                            tes3 = tes2.replace(']', '')
                            tes4 = tes3.replace(' ', '')
                            vals.append(tes4)

                        lista_precio = []

                        for rec_v in vals:
                            if rec_v != '':
                                # costo = rec.env['account_payment'].search([('id', '=', rec_v.id)]).amount
                                # print(costo,'testeo')
                                rec_fact._cr.execute(f''' SELECT id, amount
	                                                                                  from account_payment
	                                                                                  where id = '{rec_v}'
	                                                                                  ''')
                                query_res = rec_fact._cr.dictfetchall()
                                lista_precio.append(query_res)

                                for rec4 in query_res:
                                    suma = suma + rec4['amount']
                rec_fact.importe_factura = suma + rec.amount_residual

    # Funciona en base a quien factura el flete
    def relacion_facturador_flete(self):

        for line in self:

            line.uuid = ' '
            line.fecha_factura = ' '
            line.provedor_factura = ' '
            line.regimen_resico = False

            estado_pago = 0.0
            estado_adeudado = 0.0

            for factura in line.relacion_fletes_factutas:
                line.uuid = factura.uuid
                line.fecha_factura = factura.invoice_date
                if factura.invoice_date == '01/01/2000':
                    line.fecha_factura = ' '
                estado_adeudado = factura.amount_residual
                estado_pago = factura
                # if estado_adeudado == 0.0:
                #   line.estado_pago = 'Importe adeudado '

                for nombre in factura.partner_id:
                    line.provedor_factura = nombre.name
                    line.provedor_factura_id = nombre.id
                    line.regimen_resico = nombre.regimen_resico

            dias = 0
            for state in line.relacion_fletes_factutas:
                print(state.payment_state)
                # line.estado_pago = 'not_paid'
            '''line.estado_pago = ' '


                if state.payment_state == 'paid':
                    line.estado_pago = 'PAGADO'
                if state.payment_state == 'not_paid':
                    line.estado_pago = 'NO PAGADO'
                if line.estado_pago != 'PAGADO' and line.estado_pago != 'NO PAGADO':
                    line.estado_pago = 'Pagado parcialmente'''

            es_cif2 = line.env['ine_sat'].search(
                [('ine_partner_rel', '=', line.relacion_fletes_factutas.partner_id.id)]).mapped('fecha_vencimiento')

            # query que determina el estatus del contrato en base al facturador
            line.contrato_fletes_bym = ' '
            for record_contrato in line.relacion_fletes_factutas:
                for record2 in record_contrato.partner_id:
                    print('contrato', record2.contratos_bym_rel)
                    line.contrato_fletes_bym = 'NO DOCTO'

                    for record3 in record2.contratos_bym_rel:
                        print(record3, 'tasdasa')
                        vencimiento = record3.fecha_vencimiento
                        vencimiento_acum = vencimiento
                        if vencimiento is False:
                            line.es_cif = 'VENCIMIENTO NO INGRESADO'
                        if vencimiento is not False:
                            fecha_actual = fields.Date.today()
                            if vencimiento is not False:
                                if vencimiento <= fecha_actual:
                                    line.contrato_fletes_bym = 'VENCIDO'
                                else:
                                    line.contrato_fletes_bym = 'VIGENTE'
                                    vencimiento_acum = vencimiento
                            if vencimiento_acum >= fecha_actual:
                                line.contrato_fletes_bym = 'VIGENTE'

            # query que determina el status del cif en base al facturador
            # por criterio a evaluar a 90 dias
            line.es_cif = ' '
            for record_cif in line.relacion_fletes_factutas:
                for record2 in record_cif.partner_id:
                    line.es_cif = 'NO DOCTO'
                    for record3 in record2.cif_partner_rel:
                        vencimiento = record3.fecha_emision
                        if vencimiento is False:
                            line.es_cif = 'VENCIMIENTO NO INGRESADO'
                        else:
                            fecha_actual = fields.Date.today()
                            dias = (fecha_actual - vencimiento).days
                            if dias >= 90:
                                line.es_cif = 'VENCIDO'
                            else:
                                line.es_cif = 'VIGENTE'

            # query que determina el status de opinion en base al facturador
            line.es_opinion = ' '
            for record_opinion in line.relacion_fletes_factutas:
                for record2 in record_opinion.partner_id:
                    line.es_opinion = 'NO DOCTO'
                    for record3 in record2.opinion_cumplimiento:
                        vencimiento = record3.fecha_emision

                        if vencimiento is False:
                            line.es_opinion = 'VENCIMIENTO NO INGRESADO'
                        else:

                            fecha_actual = fields.Datetime.today()
                            vencimiento = str(vencimiento.strftime("20%y-%m-%d"))
                            fecha_actual = str(fecha_actual.strftime("20%y-%m-%d"))
                            diff = int((pd.to_datetime(fecha_actual) - pd.to_datetime(vencimiento)).days)

                            # vencimiento = vencimiento.strftime("20%y-%m-%d")
                            # fecha_actual = fecha_actual.strftime("20%y-%m-%d")

                            if diff >= 90:
                                line.es_opinion = 'VENCIDO'
                            else:
                                line.es_opinion = 'VIGENTE'

            # query que determina el status de INE en base al facturador
            line.es_ine = ' '
            for record_opinion2 in line.relacion_fletes_factutas:
                for record2 in record_opinion2.partner_id:
                    line.es_ine = 'NO DOCTO'
                    for record3 in record2.ine:
                        vencimiento = record3.fecha_vencimiento

                        if vencimiento is False:
                            line.es_ine = 'VENCIMIENTO NO INGRESADO'
                        else:
                            fecha_actual = fields.Date.today()
                            if vencimiento <= fecha_actual:
                                line.es_ine = 'VENCIDO'
                            else:
                                line.es_ine = 'VIGENTE'

            for recordl in line.relacion_fletes_factutas:

                for recordl2 in recordl.partner_id:
                    for recordl3 in recordl2.bank_ids:
                        account_exists = line.env['res.partner.bank'].search_count(
                            [('partner_id', '=', line.provedor_factura)])
                        if account_exists > 0:
                            found_checks = recordl3.env['res.partner.bank'].search_count([('check', '=', True),
                                                                                          ('partner_id', '=',
                                                                                           recordl3.partner_id.id)])
                            if found_checks == 0:
                                line.chack_cuenta_decault_fletes = False
                            if found_checks >= 1:
                                line.chack_cuenta_decault_fletes = True

                        if account_exists <= 0:
                            line.chack_cuenta_decault_fletes = False
            suma = 0.0
            if line.provedor_factura == ' ':
                for resico in line.beneficiario:
                    line.regimen_resico = resico.regimen_resico

            for l in line.impuestos:
                suma = l.importe + suma
            line.total_tarifa_inicial2 = line.importe_total_fletes_municipio + suma
            acum1 = 0.0
            acum1 = line.total_tarifa_inicial2 / 1.12
            line.base_tarifa = acum1
            print(acum1, 'acumsaw')
            line.desgloce_iva = acum1 * .16
            line.desgloce_retencion = acum1 * .04
            if line.regimen_resico is False:
                line.desgloce_resico = 0.0
                line.importe_mas_retencion = line.total_tarifa_inicial2
            if line.regimen_resico is True:
                line.desgloce_resico = acum1 * 0.0125
                line.importe_mas_retencion = line.total_tarifa_inicial2 - line.desgloce_resico

    # En caso de de agregar un aumento o descuanto en retenciones extras
    # hace el ajusto a la tarifa mostrastrada
    @api.onchange('impuestos')
    def _calculo_mas_extras_fletes(self):

        for rec in self:
            suma = 0.0
            for line in rec.impuestos:
                suma = suma + line.importe
            acum1 = 0.0
            acum1 = rec.total_tarifa_inicial2 / 1.12
            rec.base_tarifa = acum1
            print(acum1, 'acumsaw')
            rec.desgloce_iva = acum1 * .16
            rec.desgloce_retencion = acum1 * .04
            if rec.regimen_resico is False:
                rec.desgloce_resico = 0.0
                rec.importe_mas_retencion = rec.total_tarifa_inicial2
            if rec.regimen_resico is True:
                rec.desgloce_resico = acum1 * 0.0125
                rec.importe_mas_retencion = rec.total_tarifa_inicial2 - rec.desgloce_resico

    def aprobar_cfdi_fletes(self):
        for rec_aprobado in self:
            rec_aprobado.state_fletes = 'aprobado_cfdi'

    def ir_borrador_fletes(self):
        for rec_borrador in self:
            rec_borrador.state_fletes = 'borrador'

    def recarcular_actualizacion(self):
        for record_fletes in self:

            importe_municipio_flete = 0.0
            res_tarifa_amount = record_fletes.env['tarifas_fletes'].search(
                [('name', '=', record_fletes.municipio.id)]).tarifa_importe_final_flete_municipio
            record_fletes.importe_total_fletes_municipio = res_tarifa_amount
            record_fletes.base_tarifa = record_fletes.total_tarifa_inicial2 /1.12

            tarifa_inicial = record_fletes.env['tarifas_fletes'].search(
                [('name', '=', record_fletes.municipio.id)]).importe
            record_fletes.importe_tarifa_inicial = tarifa_inicial
            print('record_fletes', record_fletes.importe_tarifa_inicial)

            record_fletes.uuid = ' '
            record_fletes.fecha_factura = ' '
            record_fletes.provedor_factura = ' '
            # record_fletes.estado_pago = ' '
            for factura in record_fletes.relacion_fletes_factutas:
                record_fletes.estado_pago_selection = factura.payment_state
                record_fletes.uuid = factura.uuid
                record_fletes.fecha_factura = factura.invoice_date
                if factura.invoice_date == '01/01/2000':
                    record_fletes.fecha_factura = ' '

                for nombre in factura.partner_id:
                    record_fletes.provedor_factura = nombre.name

            suma = 0.0
            for line in record_fletes.impuestos:
                suma = suma + line.importe
            # query, si hay regimen activado en res.partner hacer calculo del -.25%


    @api.model
    def create(self, variables):
        if variables['peso_promedio_caja'] > 28:
            variables['state'] = 'alerta_exeso'
            variables['alerta_peso_cajas'] = '***CAJAS CON MAS DE 28kg***'
        if variables['peso_promedio_caja'] < 22:
            variables['state'] = 'alerta_faltante'
            variables['alerta_peso_cajas'] = '***CAJAS CON MENOS DE 22kg***'

        res_tarifa_amount = self.env['tarifas_fletes'].search(
            [('name', '=', variables['municipio'])]).tarifa_importe_final_flete_municipio
        variables['importe_total_fletes_municipio'] = f'{res_tarifa_amount}'

        if variables['resico'] == True:
            variables['importe_mas_retencion'] = (variables['extras_one2many'] + res_tarifa_amount)
            # \
            # - ((variables['extras_one2many'] + res_tarifa_amount) * 0.0125)
            print(variables['importe_mas_retencion'], ' TarifaFinal')
        else:
            variables['importe_mas_retencion'] = variables['extras_one2many'] + res_tarifa_amount

        return super(FletesCrear, self).create(variables)

    # guarda en la base de datos las tarifas del modelo tafifas_fletes
    def _compute_tarifa_final_fleteo(self):
        for record_fletes in self:
            importe_municipio_flete = 0.0
            res_tarifa_amount = record_fletes.env['tarifas_fletes'].search(
                [('name', '=', record_fletes.municipio.id)]).tarifa_importe_final_flete_municipio
            record_fletes.importe_total_fletes_municipio = res_tarifa_amount

            tarifa_inicial = record_fletes.env['tarifas_fletes'].search(
                [('name', '=', record_fletes.municipio.id)]).importe
            record_fletes.importe_tarifa_inicial = tarifa_inicial
            acum1 = 0.0
            acum2 = 0.0
            if record_fletes.cajas_lote_fletes > 300:
                acum1 = ((record_fletes.cajas_lote_fletes - 300) * 15) * .16
                acum2 = ((record_fletes.cajas_lote_fletes - 300) * 15) * .04
            print(acum2)
            print('acum1', acum1)
            record_fletes.desgloce_iva = (tarifa_inicial * 0.16) + acum1
            record_fletes.desgloce_retencion = -(tarifa_inicial * 0.04) - acum2

    def download_data(self):
        engine = Session.engine()
        session = Session.session(engine)

        # valores globales para llamar el objeto fuera del modelo
        global fletes_object
        # mapeo de modelos
        rango_fletes_obj = self.env['fletes_wizard']
        contactos_obj = self.env['res.partner']
        huertas_obj = self.env['huertas']
        for j in rango_fletes_obj.search([], order='id desc', limit=1):
            j.fecha_inicial
            j.fecha_final

        # realizo el query en la clase "CortesDataOrden" para obtener un resultado
        # filtrado por fechas

        fletes_object = session.query(CortesDataOrden, CortesCajasTTS).filter(
            CortesDataOrden.fecha.cast(Date).between(j.fecha_inicial, j.fecha_final)). \
            filter(CortesCajasTTS.id_orden_corte_cajas == CortesDataOrden.id_orden_corte).all()
        # .filter(CortesMixtosCajasTTS.tiket_mixto_tts == CortesCajasTTS.ticket)

        # Objeto que crea el catalogo de huertas

        # este arreglo recorre el objeto resultante del query
        for record in fletes_object:

            if self.env['fletes_modelo_tts'].search_count([('name', '=', record[0].id_orden_corte)]) >= 1:
                print('Registro existente')
            if self.env['fletes_modelo_tts'].search_count([('name', '=', record[0].id_orden_corte)]) == 0:
                global rec_obj_fletes_dic
                global id_huerta
                global id_ubicacion_municipio
                global id_name_trasportista
                global id_municipio
                global id_productor
                global id_transportista
                global id_jefe_cuadrilla
                global id_estado
                global id_poblacion
                global testeo
                istrue = False

                # create method for record and search register
                if self.env['res.partner'].search_count([('name', '=', record[0].nombre_transportista)]) >= 1:
                    id_transportista = self.env['res.partner'].search([('name', '=', record[0].nombre_transportista)],
                                                                      limit=1).id
                    istrue = self.env['res.partner'].search(
                        [('name', '=', record[0].nombre_transportista)]).regimen_resico

                if self.env['res.partner'].search_count([('name', '=', record[0].nombre_transportista)]) == 0:
                    rec_obj_transportista_dic = {'name': record[0].nombre_transportista, }
                    id_transportista = self.env['res.partner'].create(rec_obj_transportista_dic)
                    id_transportista = id_transportista.id

                    self.env.cr.commit()

                if self.env['localidad'].search_count([('name', '=', record[0].ubicacion)]) >= 1:
                    id_ubicacion_municipio = self.env['localidad'].search([('name', '=', record[0].ubicacion)],
                                                                          limit=1).id
                if self.env['localidad'].search_count([('name', '=', record[0].ubicacion)]) == 0:
                    rec_obj_localidad_dic = {'name': record[0].ubicacion}
                    id_ubicacion_municipio = self.env['localidad'].create(rec_obj_localidad_dic)
                    id_ubicacion_municipio = id_ubicacion_municipio.id
                    self.env.cr.commit()

                if self.env['poblacion'].search_count([('name', '=', record[0].poblacion)]) >= 1:
                    id_poblacion = self.env['poblacion'].search([('name', '=', record[0].poblacion)], limit=1).id
                if self.env['poblacion'].search_count([('name', '=', record[0].poblacion)]) == 0:
                    rec_obj_poblacion_dic = {'name': record[0].poblacion, }
                    id_poblacion = self.env['poblacion'].create(rec_obj_poblacion_dic)
                    id_poblacion = id_poblacion.id
                    self.env.cr.commit()

                if self.env['ciudad'].search_count([('name', '=', record[0].municipio)]) >= 1:
                    id_municipio = self.env['ciudad'].search([('name', '=', record[0].municipio)], limit=1).id
                if self.env['ciudad'].search_count([('name', '=', record[0].municipio)]) == 0:
                    rec_obj_municipio_dic_dic = {'name': record[0].municipio, }
                    id_municipio = self.env['ciudad'].create(rec_obj_municipio_dic_dic)
                    id_municipio = id_municipio.id
                    self.env.cr.commit()

                if self.env['estado'].search_count([('name', '=', record[0].estado)]) >= 1:
                    id_estado = self.env['estado'].search([('name', '=', record[0].estado)], limit=1).id
                if self.env['estado'].search_count([('name', '=', record[0].estado)]) == 0:
                    rec_obj_estado_dic = {'name': record[0].estado, }
                    id_estado = self.env['estado'].create(rec_obj_estado_dic)
                    id_estado = id_estado.id
                    self.env.cr.commit()

                if self.env['res.partner'].search_count([('name', '=', record[0].nombre_productor)]) >= 1:
                    id_productor = self.env['res.partner'].search([('name', '=', record[0].nombre_productor)],
                                                                  limit=1).id
                if self.env['res.partner'].search_count([('name', '=', record[0].nombre_productor)]) == 0:
                    rec_obj_productor_dic = {'name': record[0].nombre_productor, }
                    id_productor = self.env['res.partner'].create(rec_obj_productor_dic)
                    id_productor = id_productor.id
                    self.env.cr.commit()

                if self.env['huertas'].search_count([('sader', '=', record[0].sader)]) >= 1:
                    id_huerta = self.env['huertas'].search([('sader', '=', record[0].sader)], limit=1).id
                if self.env['huertas'].search_count([('sader', '=', record[0].sader)]) == 0:
                    rec_obj_huertas_dic = {'name': record[0].huerta,
                                           'sader': record[0].sader,
                                           'productor': self.env['res.partner'].search(
                                               [('name', '=', record[0].nombre_productor)]).id
                                           }
                    id_huerta = self.env['huertas'].create(rec_obj_huertas_dic)
                    id_huerta = id_huerta.id
                    self.env.cr.commit()

                if self.env['res.partner'].search_count([('name', '=', record[0].nombre_jefe_cuadrilla)]) >= 1:
                    id_jefe_cuadrilla = self.env['res.partner'].search(
                        [('name', '=', record[0].nombre_jefe_cuadrilla)], limit=1).id
                if self.env['res.partner'].search_count([('name', '=', record[0].nombre_jefe_cuadrilla)]) == 0:
                    rec_obj_jefe_cuadrilla_dic = {'name': record[0].nombre_jefe_cuadrilla, }
                    id_jefe_cuadrilla = self.env['res.partner'].create(rec_obj_jefe_cuadrilla_dic)
                    id_jefe_cuadrilla = id_jefe_cuadrilla.id
                    self.env.cr.commit()

                tarifa_cajas_extra2 = 0.0
                if record[1].id_cajas_cortadas > 300:
                    tarifa_cajas_extra2 = (((record[1].id_cajas_cortadas - 300) * 15) * 1.16) \
                                          - (((record[1].id_cajas_cortadas - 300) * 15) * .04)

                cajas_camion = record[1].cajas_entregadas
                if cajas_camion == 0:
                    cajas_camion = record[1].id_cajas_cortadas
                if record[1].pesototal != 0.0:
                    promediocajas = record[1].pesototal / record[1].id_cajas_cortadas

                rec_obj_fletes_dic = {
                    'name': record[0].id_orden_corte,
                    'fecha': record[0].fecha,
                    'huerta': id_huerta,
                    'poblacion': id_poblacion,
                    'nombre_produtor_modelo_tts': id_productor,
                    'status': record[0].status,
                    'estado': id_estado,
                    'nombre_transportista': id_transportista,
                    'nombre_jefe_cuadrilla': id_jefe_cuadrilla,
                    'municipio': id_municipio,
                    'observaciones': record[0].observaciones,
                    'ubicacion_municipio': id_ubicacion_municipio,
                    'cajas_lote_fletes': record[1].id_cajas_cortadas,
                    'cajas_mixtos_fletes': cajas_camion,
                    'peso_producto': record[1].pesototal,
                    'peso_promedio_caja': promediocajas,
                    'extras_one2many': tarifa_cajas_extra2,
                    'resico': istrue,

                }
                insert_cajas_de_tts = self.env['fletes_modelo_tts'].create(rec_obj_fletes_dic)

                if record[1].id_cajas_cortadas > 300:
                    tarifa_cajas_extra = (((record[1].id_cajas_cortadas - 300) * 15) * 1.16) \
                                         - (((record[1].id_cajas_cortadas - 300) * 15) * .04)
                    id_cajas_extra = self.env['cat_descuentos'].search([('name', '=', 'CAJAS EXTRA')], limit=1)
                    recordcajasfletes = {'name': id_cajas_extra.id,
                                         'fletes_rel': insert_cajas_de_tts.id,
                                         'importe': tarifa_cajas_extra, }
                    insert_cajas_flete = self.env['retenciones'].create(recordcajasfletes)
                    self.env.cr.commit()

                print(rec_obj_fletes_dic)
                # response_dic_create = self.env['fletes_modelo_tts'].create(rec_obj_fletes_dic)
                self.env.cr.commit()
        session.close()
        engine.dispose()

