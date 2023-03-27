# -*- coding:utf-8 -*-
import datetime

from odoo import fields, models, api
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String, Float, SmallInteger, Numeric, DateTime, Date
from sqlalchemy import cast
from sqlalchemy import distinct
from sqlalchemy import or_
import logging
import pandas as pd
import pendulum

_logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

Base = declarative_base()

#Table contpaqi contabilidad cfdis relacionados , distingue las notas de credito y facturas de anticipo.
class CfdiRelacionados(Base):
    __tablename__ = 'CfdiRelacionados'
    guid_document = Column('GuidDocument',String(500), primary_key=True)
    uuid = Column('UUID',String(500))
    tipo_relacion = Column('TipoRelacion',String(500))
    tipo_relacion_desc = Column('TipoRelacionDesc',String(500))

class PagosDocRel(Base):
    __tablename__ = 'View_Pagos'
    guid_document = Column('GuidDocument',String(500),primary_key=True)
    id_pago = Column('IdPago',String(500))
    id_documento = Column('IdDocumento',String(500))
    serie = Column('Serie',String(500))
    folio = Column('Folio',String(500))
    moneda_dr = Column('MonedaDr',String(500))
    moneda_dr_desc = Column('MonedaDRDesc',String(500))
    tipo_cambio_dr = Column('TipoCambioDr',String(500))
    metodo_pago_dr = Column('MetodoDePagoDr',String(500))
    metodo_pago_dr_desc = Column('MetodoDePagoDrDesc',String(500))
    num_parcialidad = Column('NumParcialidad',Integer)
    imp_saldo_ant = Column('ImpSaldoAnt',Float)
    imp_pagado = Column('ImpPagado',Float)
    imp_saldo_insoluto = Column('ImpSaldoInsoluto',Float)
    fecha = Column('FechaPago',DateTime)


class Conceptos(Base):
    __tablename__ = 'Conceptos'
    guid_document = Column('GuidDocument', String(500), primary_key=True)
    cantidad = Column('Cantidad', Float)
    valor_unitario = Column('ValorUnitario', Float)
    importe = Column('Importe', Float)
    descuento = Column('Descuento', Float)
    clave_prod_sat = Column('CveProdSer',String(50))
    clave_prod_sat_desc = Column('CveProdSerDesc',String(1000))
    no_identificacion = Column('NoIdentificacion',String(50))
    clave_unidad = Column('ClaveUnidad',String(50))
    clave_unidad_desc = Column('ClaveUnidadDesc',String(100))
    unidad = Column('Unidad',String(100))
    descripcion = Column('Descripcion',String(3000))

    #####################revisado hasta aqui


# Clase para descargar encabezados de contpaqi contabilidad
class CfdisContpaqiData(Base):
    # Tabla comprobante contpaqi contiene las cabeceras de todos los CFDI
    __tablename__ = 'Comprobantes_View'
    # todos los campos del cfdi 3.3
    uuid = Column('UUID', String(600), primary_key=True)
    guid_document = Column('GuidDocument', String(500))
    rfc_emisor = Column('RFCEmisor', String(500))
    nombre_emisor = Column('NombreEmisor', String(500))
    regimen_emisor = Column('RegimenEmisor', String(500))
    regimen_emisor_desc = Column('RegimenEmisorDesc', String(500))
    curp_emisor = Column('CurpEmisor', String(500))
    rfc_receptor = Column('RFCReceptor', String(500))
    nombre_receptor = Column('NombreReceptor', String(500))
    regimen_receptor = Column('RegimenReceptor', String(500))
    total_impuestos_retenidos = Column('TotImpRetenidos', Float)
    total_impuestos_traslado = Column('TotImpTraslado', Float)
    version = Column('Version', String(500))
    serie = Column('Serie', String(500))
    folio = Column('Folio', String(500))
    fecha = Column('Fecha', DateTime)
    fecha_mes = Column('FechaMes', String(500))
    fecha_anio = Column('FechaAnio', String(200))
    forma_de_pago = Column('FormaPago', String(500))
    forma_de_pago_desc = Column('FormaPagoDesc', String(500))
    condiciones_de_pago = Column('CondicionesPago', String(500))
    subtotal = Column('Subtotal', Float)
    descuento = Column('Descuento', Float)
    tipo_cambio = Column('TipoCambio', Float)
    moneda = Column('Moneda', String(500))
    moneda_desc = Column('MonedaDesc', String(500))
    total = Column('Total', Float)
    tipo_comprobante = Column('TipoComprobante', String(500))
    metodo_pago = Column('MetodoPago', String(500))
    metodo_pago_desc = Column('MetodoPagoDesc', String(500))
    lugar_exp = Column('LugarExp', String(500))
    lugar_exp_desc = Column('LugarExpDesc', String(500))
    fecha_timbrado = Column('FechaTimbrado', DateTime)
    fecha_timbrado_mes = Column('FechaTimbradoMes', String(500))
    fecha_timbrado_anio = Column('FechaTimbradoAnio', String(500))
    numero_certificado = Column('NumeroCertificado', String(500))
    confirmacion = Column('Confirmacion', String(500))
    tipo_documento = Column('TipoDocumento', String(500))
    residencia_fiscal = Column('ResidenciaFiscal', String(500))
    residencia_fiscal_desc = Column('ResidenciaFiscalDesc', String(500))
    num_registro_id_trib = Column('NumRegIdTrib', String(500))
    uso_cfdi = Column('UsoCFDI', String(500))
    uso_cfdi_desc = Column('UsoCFDI_Desc', String(500))
    tipo_comprobante_desc = Column('TipoComprobanteDesc', String(500))
    num_cuenta = Column('NumCta', String(500))
    tipo_relacion_desc = Column('TipoRelacionDesc',String(500))


#####################revisado hasta aqui


class Session():
    def session(engine):
        Session = sessionmaker(bind=engine)
        # session = Session()
        session = scoped_session(Session)

        return session

    def engine():
        server_addres = 'e3210dfde5c7.sn.mynetname.net' + ":" + "49706"
        #server_addres = '192.168.88.214' + ":" + "49706"
        database = 'document_e6bf5000-4ec4-4221-b121-079a0be33697_metadata'
        username = 'sa'
        password = 'HideMyPassBm123'

        arguments = dict(server=server_addres, user=username,
                         password=password, database=database, charset="utf8")

        engine = sa.create_engine('mssql+pymssql:///', connect_args=arguments)
        return engine
    #Conexion a la BD content de contpaqi (XML FILE)
    def engine_xml():
        #server_addres_xml = '192.168.88.214' + ":" + "49706"
        server_addres_xml = 'e3210dfde5c7.sn.mynetname.net' + ":" + "49706"
        database_xml = 'document_b293efb8-0254-4a13-8ab5-dd78af6bfc8b_content'
        username_xml = 'sa'
        password_xml = 'HideMyPassBm123'

        # Modelo de odoo
        #####################revisado hasta aqui
class FacturaCfdi(models.Model):

    _inherit = 'account.move'

    uuid = fields.Char(string='UUID')

    guid_document = fields.Char(string='Guid Document')

    rfc_emisor = fields.Char(string='RFC Emisor')

    nombre_emisor = fields.Char(string='Nombre Emisor')

    regimen_emisor = fields.Char(string='Regimen Emisor')

    regimen_emisor_desc = fields.Char(string='Regimen Emisor Desc')

    curp_emisor = fields.Char(string='CURP Emisor')

    rfc_receptor = fields.Char(string='RFC Receptor')

    nombre_receptor = fields.Char(string='Regimen Receptor')

    total_impuestos_retenidos = fields.Float(string='Total de impuestos retenidos')

    total_impuestos_traslado = fields.Float(string='Total Impuestos Traslado')

    version = fields.Char(string='Versión')

    serie = fields.Char(string='Serie')

    folio = fields.Char(string='Folio')

    fecha = fields.Datetime(string='Fecha')

    fecha_filtro = fields.Date(string='Fecha filtro')

    fecha_mes = fields.Char(string='Fecha Mes')

    fecha_anio = fields.Char(string='Fecha Año')

    forma_de_pago = fields.Char(string='Forma de pago')

    forma_de_pago_desc = fields.Char(string='Forma de pago desc')

    condiciones_de_pago = fields.Char(string='Condicones de pago')

    subtotal = fields.Float(string='Subtotal')

    descuento = fields.Float(string='Descuento')

    tipo_cambio = fields.Float(string='Tipo de cambio')

    moneda = fields.Char(string='Moneda')

    moneda_desc = fields.Char(string='Moneda Desc')

    total = fields.Float(string='Total')

    tipo_comprobante = fields.Char(string='Tipo de comprobante')

    metodo_pago = fields.Char(string='Metodo de pago')

    metodo_pago_desc = fields.Char(string='Metodo de pago desc')

    lugar_exp = fields.Char(string='Lugar Exp')

    lugar_exp_desc = fields.Char(string='Lugar Exp Desc')

    fecha_timbrado = fields.Datetime(string='Fecha timbrado')

    fecha_timbrado_mes = fields.Char(string='Fecha Timbrado Mes')

    fecha_timbrado_anio = fields.Char(string='Fecha Timbrado Año')

    numero_certificado = fields.Char(string='Número certificado')

    confirmacion = fields.Char(string='Confirmación')

    tipo_documento = fields.Char(string='Tipo Documento')

    residencia_fiscal = fields.Char(string='Residencia Fiscal')

    residencia_fiscal_desc = fields.Char(string='Residencia Fiscal Desc')

    num_registro_id_trib = fields.Char(string='Num registro identificación tributaria')

    uso_cfdi = fields.Char(string='Uso de cfdi')

    uso_cfdi_desc = fields.Char(string='Uso de cfdi desc')

    tipo_comprobante_desc = fields.Char(string='Tipo Comprobante Desc')

    num_cuenta = fields.Char(string='Num cuenta')

    xml_cfdi = fields.Text(string='Cfdi XML')

    lotes_cfdi_relacionn = fields.One2many('lotes_account_move_line','data_rel')

    x = fields.Many2one(related='lotes_cfdi_relacionn.lotes_nombre_productor')

    xx = fields.Many2one(related='lotes_cfdi_relacionn.lotes_huerta')

    factura_original_name = fields.Char(string='Nombre de archivo')

    factura_original_file = fields.Binary(string='Factura Original')

    nc_original_name = fields.Char(string='Nombre de archivo')

    nc_original_file = fields.Binary(string='Nota de credito Original')

    purchase_order_rel = fields.Many2many('purchase.order', 'purchase_order_account_move_rel_4','purchase_id','account_id', string='Ordenes Compra')

    rep_rel = fields.One2many('pagos_doctos_rel','account_move_pagos_rel',string='Relación de REPS')

    x_field = fields.Many2many(comodel_name='account.payment',compute='retreivePayment',string='Pagoz',related='')

    recn = fields.Char(compute='acount_paym_ivoice', string="Pagos")

    id_pagos = fields.Char(string='Pagos',compute='acount_paym_ivoice')

    layout_rel = fields.Many2one('pagos_layout',string='Relacion Layout')

    presupuesto_lote_fac_adic_rel = fields.Many2one('presupuesto_lotes',string='Presupuesto Lote Rel')


    lotes_provisionados = fields.One2many('lotes_account_move_line', 'lotes_presupuestos_rel',
                                          string='Lotes Presupuestados')




    def button_cancel(self):
        self.write({'auto_post': False, 'state': 'cancel'})
        account_move_line_obj = self.env['lotes_account_move_line']
        account_move_line_obj.search([('data_rel', '=', self.id)]).unlink()

    #funcion que regresa los pagos
    def acount_paym_ivoice(self):
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

        r._cr.execute('''
                SELECT
                    payment.id AS pay,
                    ARRAY_AGG(DISTINCT invoice.id) AS invoice_ids,
    				invoice.id,
    				move.date AS fechax,
                    invoice.move_type AS tipo
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
                    AND payment.id IN %(pays)s
                    AND line.id != counterpart_line.id
                    AND invoice.move_type in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                	AND invoice.id = %(account_move_ids)s
    			GROUP BY pay, tipo, invoice.id, fechax
    			ORDER BY pay DESC
                ''', {
            'pays': ids_payments_all,
            'account_move_ids': r.id,
        })
        query_res = r._cr.dictfetchall()
        pagos_ids_all = []
        pagos_ids_new = []
        payments_ids = ''

        for res in query_res:
            #self.recn = res['fechax']
            x = res['fechax']
            payments_ids = res['pay']
            x.strftime("%b %d %Y")
            pagos_ids_all.append(x)
            pagos_ids_new.append(payments_ids)

        x_date = pagos_ids_all
        x_date = str(x_date).replace('datetime.date','')
        x_date = str(x_date).replace('[', '')
        x_date = str(x_date).replace(']', '')
        x_date = str(x_date).replace(',','-')
        x_date = str(x_date).replace(' ','')

        self.recn = x_date
        self.id_pagos = payments_ids

        # Cambios en el One2many de lotes
        @api.onchange('lotes_cfdi_relacionn')
        def _onchange_cfdis_lotes(self):
            # Lista vacia contenedor de ciclos
            RowList = []
            # funciones de calculo numerico de lotes
            self.env['lotes_account_move_line']._compute_kg_pendientes()
            self.env['lotes_account_move_line']._compute_abono_importe()
            # se busca el concepto de 21 dias en odoo por medio del xml id
            id_dias_pago = self.env.ref('account.account_payment_term_21days')
            # ciclo recorre el One2many
            for line in self.lotes_cfdi_relacionn:
                # sino es falso el resultado
                if line.name.fecha is not False:
                    # lista = pandas conversion de date.time a date (fecha de cada linea de lote)
                    my_list = pd.to_datetime(line.name.fecha).date()
                    # se agregan los resultados de las iteraciones a RowList
                    RowList.append(my_list)
                # si es falso el resultado no hacer nada
                if line.name.fecha is False:
                    print('Omitir')
                if line.name.fecha == None:
                    print('Omitir')
            # imprimir la lista en una sola linea
            print('Antes de suma')
            # se obtiene la fecha mas vieja de la lista y por default la fecha de la factura para evitar false's
            oldest = pd.to_datetime(max(RowList, default=self.invoice_date)).date()
            # se le agregarn los dias a la fecha mas vieja 21 dias
            add_days = pd.to_datetime(oldest) + datetime.timedelta(days=id_dias_pago.line_ids.days)
            # se formatea la variable a solo date
            add_days = add_days.strftime("%Y-%m-%d")
            # se imprime la fecha
            # date vacio
            friday_date = ''
            print((pd.to_datetime(add_days).date()).strftime("%A"))
            # cuando sea sabado el dia calculado regresar al viernes anterior
            if (pd.to_datetime(add_days).date()).strftime("%A") == 'sábado':
                friday_date = pendulum.parse(add_days).previous(pendulum.FRIDAY).strftime('%Y-%m-%d')
            # condicional si es viernes
            if (pd.to_datetime(add_days).date()).strftime("%A") == 'viernes':
                # usar el dia de la suma de dias
                friday_date = add_days
                # sino es viernes
            if (pd.to_datetime(add_days).date()).strftime("%A") != 'viernes' and (
            pd.to_datetime(add_days).date()).strftime("%A") != 'sábado':
                # buscar el siguiente viernes
                friday_date = pendulum.parse(add_days).next(pendulum.FRIDAY).strftime('%Y-%m-%d')
                # se coloca la fecha calculada en la fecha de pago
            self.invoice_date_due = friday_date
            print(friday_date)

    #####################revisado hasta aqui

    def download_data(self):
        engine = Session.engine()
        session = Session.session(engine)

        global cfdi_contpaqi

        contactos_obj = self.env['res.partner']

        rango_cfdis_obj = self.env['cfdis_wizard']

        cfdi_obj = self.env['account.move']

        products_obj = self.env['product.template']

        moneda_obj = self.env['res.currency'].search([('name', '=', 'MXN')])

        for i in rango_cfdis_obj.search([], order='id desc', limit=1):
            # ordenar por nombre
            # lote_inicial_object.search([],order='name')
            i.fecha_inicial
            i.fecha_final

        #establezco que descargare tod0 menos lo que tenga aplicacion de anticipos que son las NOTAS DE CREDITO
        cfdis_objeto = session.query(CfdisContpaqiData).filter(
            CfdisContpaqiData.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)). \
            filter(CfdisContpaqiData.rfc_emisor!='BAM170904DM5'). \
        filter(CfdisContpaqiData.rfc_receptor == 'BAM170904DM5').filter(CfdisContpaqiData.forma_de_pago_desc!='Aplicación de anticipos').\
            filter(CfdisContpaqiData.uso_cfdi != 'G02').filter(CfdisContpaqiData.tipo_documento != 'Pago')\
            .all()
        print('FACTURAZ VIEW')
        print(cfdis_objeto)


        #este objecto filtra por adquisicion de mercacias para despues ser llamado por un metodo que registre a los proveedores
        cfdi_object_cat_emisores = session.query(distinct(CfdisContpaqiData.rfc_emisor),
                                                  CfdisContpaqiData.nombre_emisor).order_by(
            CfdisContpaqiData.nombre_emisor).filter(
            CfdisContpaqiData.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).filter(CfdisContpaqiData.rfc_emisor!='BAM170904DM5'). \
        filter(CfdisContpaqiData.rfc_receptor=='BAM170904DM5').all()

        #Este query relaciona las NOTAS DE CREDITO con el UUID de los CFDI Relacionados.
        cfdi_notas_credito_object = session.query(CfdisContpaqiData,CfdiRelacionados).filter(CfdisContpaqiData.fecha.cast(Date).between(i.fecha_inicial,i.fecha_final)). \
        filter(CfdiRelacionados.tipo_relacion_desc != 'Sustitución de los CFDI previos').\
            filter(CfdisContpaqiData.tipo_comprobante == 'E').filter(CfdisContpaqiData.guid_document == CfdiRelacionados.guid_document).all()
        print('XNOTAS DE CREDITO VIEW')
        print(cfdi_notas_credito_object)


        for record2 in cfdi_object_cat_emisores:
            global response
            response = ''
            # agregar datos de al diccionario python
            id_category_productor = self.env.ref('cuentas_por_pagar.category_productor')
            response = {'vat': record2[0],
                        'name': record2[1],
                        'category_id': id_category_productor, }
            print(record2[0])
            if self.env['res.partner'].search_count([('vat', '=', record2[0])]) >= 1:
                print('Este contacto ya existe')
                print(self.env['res.partner'].search_count([('vat', '=', record2[0])]))
            # valida y si no hay registros coincidentes almacena un nuevo registro
            if self.env['res.partner'].search_count([('vat', '=', record2[0])]) == 0:
                rec = self.env['res.partner'].create(response)
                self.env.cr.commit()
                print(response)
#recorre la data de cfdis de sql server Comprobantes
        for record in cfdis_objeto:
            global recordObject
            global recordConceptosObject
            #validacion si existe la factura o no.
            if self.env['account.move'].search_count([('uuid', '=', record.uuid)]) >= 1:
                print('Cfdi repetido')
            if self.env['account.move'].search_count([('uuid', '=', record.uuid)]) == 0:
                # este arreglo busca y obtiene el id del proveedor
             for line in contactos_obj.search([('vat', '=', record.rfc_emisor)]):

                print('no existen datos repetidos')
                # objecto donde se almacena el diccionario a dar de alta encabezado del cfdi
                recordObject = {'uuid': record.uuid,
                                'move_type': 'in_invoice',
                                'guid_document': record.guid_document,
                                'rfc_emisor': record.rfc_emisor,
                                'nombre_emisor': record.nombre_emisor,
                                'regimen_emisor': record.regimen_emisor,
                                'regimen_emisor_desc': record.regimen_emisor_desc,
                                'partner_id': line.id,
                                'invoice_date': record.fecha,
                                'curp_emisor': record.curp_emisor,
                                'rfc_receptor': record.rfc_receptor,
                                'nombre_receptor': record.nombre_receptor,
                                'total_impuestos_retenidos': record.total_impuestos_retenidos,
                                'total_impuestos_traslado': record.total_impuestos_traslado,
                                'version': record.version,
                                'serie': record.serie,
                                'folio': record.folio,
                                'fecha_mes': record.fecha_mes,
                                'fecha_anio': record.fecha_anio,
                                'forma_de_pago': record.forma_de_pago,
                                'forma_de_pago_desc': record.forma_de_pago_desc,
                                'condiciones_de_pago': record.condiciones_de_pago,
                                'descuento': record.descuento,
                                'tipo_cambio': record.tipo_cambio,
                                'moneda': record.moneda,
                                'moneda_desc': record.moneda_desc,
                                'tipo_comprobante': record.tipo_comprobante,
                                'metodo_pago': record.metodo_pago,
                                'metodo_pago_desc': record.metodo_pago_desc,
                                'lugar_exp': record.lugar_exp,
                                'lugar_exp_desc': record.lugar_exp_desc,
                                'fecha_timbrado': record.fecha_timbrado,
                                'fecha_timbrado_mes': record.fecha_timbrado_mes,
                                'fecha_timbrado_anio': record.fecha_timbrado_anio,
                                'numero_certificado': record.numero_certificado,
                                'confirmacion': record.confirmacion,
                                'uso_cfdi': record.uso_cfdi,
                                'uso_cfdi_desc': record.uso_cfdi_desc,
                                'tipo_documento': record.tipo_documento,
                                'residencia_fiscal': record.residencia_fiscal,
                                'residencia_fiscal_desc': record.residencia_fiscal_desc,
                                'num_registro_id_trib': record.num_registro_id_trib,
                                'tipo_comprobante_desc': record.tipo_comprobante_desc,
                                'num_cuenta': record.num_cuenta,
                                'state':'draft',
                                'currency_id':self.env['res.currency'].search([('name', '=', record.moneda)]).id,
                                'amount_untaxed_signed': record.subtotal,
                                }
                comprobantes_objeto = self.env['account.move'].create(recordObject)

                global tax_signed
                global tax_signed_2
                global tax_signed_3
                #variables de control
                tax_signed_2 = True
                tax_signed_3 = False
                if record.total != record.subtotal:
                    tax_signed = record.total - record.subtotal
                    if (tax_signed < 0):
                        tax_signed = tax_signed * (-1)
                        tax_signed_2 = False
                        tax_signed_3 = True
                if record.total == record.subtotal:
                    tax_signed = 0

                # linea agregada para ISR por PRODUCTO
                if record.total != record.subtotal:
                    print(tax_signed, ' XXXXXXXXXXXXXXXXXXXXXXX')
                    recordConceptosObjectISR = {'move_id': comprobantes_objeto.id,
                                                'product_id': None,
                                                'account_id': 34,
                                                'journal_id': 2,
                                                'quantity': 1,
                                                'tax_exigible': True,
                                                'exclude_from_invoice_tab': True,
                                                #no se ocupan los comentados ya que son computados
                                                #'price_unit':tax_signed,
                                                'debit': tax_signed if tax_signed_2 else 0,
                                                'credit': tax_signed if tax_signed_3 else 0,
                                                #'balance': tax_signed,
                                                #'amount_currency': tax_signed,
                                                #'price_subtotal': tax_signed,
                                                #'price_total': tax_signed,
                                                'currency_id': self.env['res.currency'].search([('name', '=', record.moneda)]).id,
                                                'product_uom_id': None,
                                                'parent_state': 'draft',
                                                'company_currency_id': 33,
                                                'partner_id': line.id,
                                                'tax_base_amount': record.subtotal,
                                                'amount_residual': 0,
                                                'amount_residual_currency': 0,
                                                'company_id': 1,
                                                'account_root_id': 54048,
                                                'sequence': 10,
                                                #'tax_repartition_line_id': 50,
                                                #'tax_line_id': 13,
                                                #'tax_group_id': 1,
                                                }
                    crear_conceptos_isr = self.env['account.move.line'].with_context(check_move_validity=False).create(
                        recordConceptosObjectISR)
                #revisado bien
                #diccionario de linea de factura balanceo
                recordConceptosBalanceo = {'move_id':comprobantes_objeto.id,
                                           'journal_id': 2,
                                           'account_id': 18,
                                           'account_root_id':50048,
                                           'quantity': 1,
                                           'price_unit':record.total * (-1),
                                           'debit':0,
                                           'credit':record.total,
                                           'balance':record.total * (-1),
                                           'amount_currency':record.total * (-1),
                                           'price_subtotal':record.total * (-1),
                                           'price_total':record.total * (-1),
                                           'currency_id':self.env['res.currency'].search([('name', '=', record.moneda)]).id,
                                           'partner_id':line.id,
                                           'product_uom_id':None,
                                           'product_id':None,
                                           'tax_base_amount':0,
                                           'tax_exigible':True,
                                           'amount_residual':record.total * (-1),
                                           'amount_residual_currency':record.total * (-1),
                                           'exclude_from_invoice_tab':True,
                                           'parent_state':'draft',
                                           'company_id': 1,
                                           'company_currency_id': 33,
                                           'sequence':10,
                                           }
                crear_conceptos_principal = self.env['account.move.line'].with_context(check_move_validity=False).create(recordConceptosBalanceo)
                #print(recordConceptosBalanceo)
                get_record_guid_document = recordObject.get('guid_document')
                cfdi_conceptos_object = session.query(Conceptos.guid_document,Conceptos.cantidad,Conceptos.valor_unitario,Conceptos.importe,Conceptos.descripcion).filter(
                    Conceptos.guid_document == get_record_guid_document).all()
                print(recordObject)

                #diccionario de linea de factura principal|
                for w in cfdi_conceptos_object:
                 global response_products
                 response_products = ''
                 response_products = {'name': w.descripcion,
                                      'check_metodo_descarga_masiva':'DM',
                                       }
                 #lo agregue para buscar el producto y si existe lo selecciono sino lo creo
                 if self.env['product.template'].search_count([('name','=',w.descripcion)]) >= 1:
                    print('Este producto ya existe')
                    print(self.env['product.template'].search_count([('name', '=', w.descripcion)]))
                 print('Numero de resultados')
                 print(self.env['product.template'].search_count([('name', '=', w.descripcion)]))
                 if self.env['product.template'].search_count([('name','=',w.descripcion)]) == 0:
                    print('El producto no existe')
                    crear_productos = self.env['product.template'].create(response_products)
                    self.env.cr.commit()

                 recordConceptosObject = {'move_id':comprobantes_objeto.id,
                                          'product_id':self.env['product.template'].search([('name','=',w.descripcion)]).id,
                                          'account_id':34,
                                          'journal_id':2,
                                          'quantity':w.cantidad,
                                          'tax_exigible':True,
                                          'exclude_from_invoice_tab':False,
                                          'price_unit':w.valor_unitario,
                                          'debit':w.importe,
                                          'credit':0,
                                          'balance':w.importe,
                                          'amount_currency':w.importe,
                                          'price_subtotal':w.importe,
                                          'price_total':w.importe-tax_signed,
                                          'currency_id':self.env['res.currency'].search([('name', '=', record.moneda)]).id,
                                          'product_uom_id':1,
                                          'parent_state':'draft',
                                          'company_currency_id':33,
                                          'partner_id':line.id,
                                          'tax_base_amount':0,
                                          'amount_residual':0,
                                          'amount_residual_currency':0,
                                          'company_id':1,
                                          'account_root_id':54048,
                                          'sequence':10,
                                          }

                 #print('GUID IMPRESO')
                 #print(w.guid_document)

                 crear_conceptos_balanceo = self.env['account.move.line'].with_context(check_move_validity=False).create(recordConceptosObject)
                 self.env.cr.commit()
                 print(recordConceptosObject)

                # calcular conceptos de NOTAS DE CREDITO
        for rec_notas_credito in cfdi_notas_credito_object:
            global variable_prueba
            global recordObjectNotasCredito


            if self.env['account.move'].search_count([('uuid', '=', rec_notas_credito[0].uuid)]) >= 1:
                print('Cfdi repetido')
            if self.env['account.move'].search_count([('uuid', '=', rec_notas_credito[0].uuid)]) == 0:
             #for line_uuid in cfdi_obj.search([('uuid','=',rec_notas_credito[1].uuid)]):
                 #print('etapa de busqueda')

             variable_prueba = cfdi_obj.search([('uuid','=',rec_notas_credito[1].uuid)])
                # este arreglo busca y obtiene el id del proveedor
             for line_contact_nc in contactos_obj.search([('vat', '=', rec_notas_credito[0].rfc_emisor)]):
                 #diccionario encabezado del tipo nota de credito
                 recordObjectNotasCredito = {'uuid': rec_notas_credito[0].uuid,
                                 'move_type': 'in_refund',
                                 'guid_document': rec_notas_credito[0].guid_document,
                                 'rfc_emisor': rec_notas_credito[0].rfc_emisor,
                                 'nombre_emisor': rec_notas_credito[0].nombre_emisor,
                                 'regimen_emisor': rec_notas_credito[0].regimen_emisor,
                                 'regimen_emisor_desc': rec_notas_credito[0].regimen_emisor_desc,
                                 'partner_id': line_contact_nc.id,
                                 'invoice_date': rec_notas_credito[0].fecha,
                                 'curp_emisor': rec_notas_credito[0].curp_emisor,
                                 'rfc_receptor': rec_notas_credito[0].rfc_receptor,
                                 'nombre_receptor': rec_notas_credito[0].nombre_receptor,
                                 'total_impuestos_retenidos': rec_notas_credito[0].total_impuestos_retenidos,
                                 'total_impuestos_traslado': rec_notas_credito[0].total_impuestos_traslado,
                                 'version': rec_notas_credito[0].version,
                                 'serie': rec_notas_credito[0].serie,
                                 'folio': rec_notas_credito[0].folio,
                                 'fecha_mes': rec_notas_credito[0].fecha_mes,
                                 'fecha_anio': rec_notas_credito[0].fecha_anio,
                                 'forma_de_pago': rec_notas_credito[0].forma_de_pago,
                                 'forma_de_pago_desc': rec_notas_credito[0].forma_de_pago_desc,
                                 'condiciones_de_pago': rec_notas_credito[0].condiciones_de_pago,
                                 'descuento': rec_notas_credito[0].descuento,
                                 'tipo_cambio': rec_notas_credito[0].tipo_cambio,
                                 'moneda': rec_notas_credito[0].moneda,
                                 'moneda_desc': rec_notas_credito[0].moneda_desc,
                                 'tipo_comprobante': rec_notas_credito[0].tipo_comprobante,
                                 'metodo_pago': rec_notas_credito[0].metodo_pago,
                                 'metodo_pago_desc': rec_notas_credito[0].metodo_pago_desc,
                                 'lugar_exp': rec_notas_credito[0].lugar_exp,
                                 'lugar_exp_desc': rec_notas_credito[0].lugar_exp_desc,
                                 'fecha_timbrado': rec_notas_credito[0].fecha_timbrado,
                                 'fecha_timbrado_mes': rec_notas_credito[0].fecha_timbrado_mes,
                                 'fecha_timbrado_anio': rec_notas_credito[0].fecha_timbrado_anio,
                                 'numero_certificado': rec_notas_credito[0].numero_certificado,
                                 'confirmacion': rec_notas_credito[0].confirmacion,
                                 'uso_cfdi': rec_notas_credito[0].uso_cfdi,
                                 'uso_cfdi_desc': rec_notas_credito[0].uso_cfdi_desc,
                                 'tipo_documento': rec_notas_credito[0].tipo_documento,
                                 'residencia_fiscal': rec_notas_credito[0].residencia_fiscal,
                                 'residencia_fiscal_desc': rec_notas_credito[0].residencia_fiscal_desc,
                                 'num_registro_id_trib': rec_notas_credito[0].num_registro_id_trib,
                                 'tipo_comprobante_desc': rec_notas_credito[0].tipo_comprobante_desc,
                                 'num_cuenta': rec_notas_credito[0].num_cuenta,
                                 'state': 'draft',
                                 'payment_reference':'',
                                 'journal_id': 2,
                                 #'payment_id': 16,
                                 'reversed_entry_id': variable_prueba.id,
                                 'payment_state':'not_paid',
                                 'sequence_number':2,
                                 }
                 #objeto que asigna el metodo para registrar el diccionario
                 notas_credito_objeto = self.env['account.move'].create(recordObjectNotasCredito)
                 #self.env.cr.commit()

                 # diccionario de linea de notas de credito balanceo
                 #este esta bien.
                 recordConceptosNcBalanceo = {'move_id': notas_credito_objeto.id, #revisado
                                            'journal_id': 2, #revisado
                                            'account_id': 18, #revisado
                                            'account_root_id': 50048, #revisado
                                            'quantity': 1, #revisado
                                            'price_unit': rec_notas_credito[0].total * (-1), #revisado
                                            'debit': rec_notas_credito[0].total, #revisado
                                            'credit': 0, #revisado
                                            'balance': rec_notas_credito[0].total, #revisado
                                            'amount_currency': rec_notas_credito[0].total, #revisado
                                            'price_subtotal': rec_notas_credito[0].total * (-1), #revisado
                                            'price_total': rec_notas_credito[0].total * (-1), #revisado
                                            'currency_id': self.env['res.currency'].search([('name', '=', rec_notas_credito[0].moneda)]).id, #revisado
                                            'partner_id': line_contact_nc.id, # revisado
                                            'product_uom_id': None, #revisado
                                            'product_id': None, #revisado
                                            'tax_base_amount': 0, #revisado
                                            'tax_exigible': True, #revisado
                                            'amount_residual': rec_notas_credito[0].total, #revisado
                                            'amount_residual_currency': rec_notas_credito[0].total, #revisado
                                            'exclude_from_invoice_tab': True, #revisado
                                            'parent_state': 'draft', #revisado
                                            'company_id': 1, #revisado
                                            'company_currency_id': self.env['res.currency'].search([('name', '=', rec_notas_credito[0].moneda)]).id, #revisado
                                            'sequence': 10 #revisado
                                            }
                 crear_conceptos_principal_balanceo_nc = self.env['account.move.line'].with_context(
                     check_move_validity=False).create(recordConceptosNcBalanceo)
                 self.env.cr.commit()

                 # nueva linea tax

                 if rec_notas_credito[0].total != rec_notas_credito[0].subtotal:
                     recordConceptosTaxLineObject = {'move_id': notas_credito_objeto.id,
                                                     'product_id': None,
                                                     'account_id': 15,
                                                     'journal_id': 2,
                                                     'quantity': 1,
                                                     'tax_exigible': False,
                                                     'exclude_from_invoice_tab': True,
                                                     'price_unit': rec_notas_credito[0].total - rec_notas_credito[0].subtotal,
                                                     'debit': 0,
                                                     'credit': rec_notas_credito[0].total - rec_notas_credito[0].subtotal,
                                                     'balance': (rec_notas_credito[0].total - rec_notas_credito[0].subtotal) * (-1),
                                                     'amount_currency': (rec_notas_credito[0].total - rec_notas_credito[0].subtotal) * (-1),
                                                     'price_subtotal': (rec_notas_credito[0].total - rec_notas_credito[0].subtotal),
                                                     'price_total': (rec_notas_credito[0].total - rec_notas_credito[0].subtotal),
                                                     'currency_id': self.env['res.currency'].search([('name', '=', rec_notas_credito[0].moneda)]).id,
                                                     'product_uom_id': 1,
                                                     'parent_state': 'draft',
                                                     'company_currency_id': self.env['res.currency'].search([('name', '=', rec_notas_credito[0].moneda)]).id,
                                                     'partner_id': line_contact_nc.id,
                                                     'company_id': 1,
                                                     'account_root_id': 49049,
                                                     'sequence': 10,
                                                     'amount_residual': (rec_notas_credito[0].total - rec_notas_credito[0].subtotal) * (-1),
                                                     'amount_residual_currency': (rec_notas_credito[0].total -rec_notas_credito[0].subtotal) * (-1),
                                                     'tax_base_amount': rec_notas_credito[0].subtotal,
                                                     'tax_group_id':3,
                                                     'tax_line_id':10,
                                                     'tax_repartition_line_id':44,

                                                     }



                     notas_credito_detalle_tax_objeto = self.env['account.move.line'].with_context(check_move_validity=False).create(recordConceptosTaxLineObject)
                     self.env.cr.commit()
                 # nueva linea tax fin




                 #aqui empieza el detalle de la nc
                 get_record_guid_document_nc = recordObjectNotasCredito.get('guid_document')
                 cfdi_conceptos_object_nc = session.query(Conceptos.guid_document, Conceptos.cantidad,
                                                       Conceptos.valor_unitario, Conceptos.importe,Conceptos.descripcion).filter(
                     Conceptos.guid_document == get_record_guid_document_nc).all()
                 print(recordObjectNotasCredito)

                 for line_nc_prueba in cfdi_conceptos_object_nc:
                     print('Lista de productos')
                     print(line_nc_prueba.descripcion)

                     global response_products_nc
                     response_products_nc = ''
                     response_products_nc = {'name': line_nc_prueba.descripcion,
                                          'check_metodo_descarga_masiva': 'DM',
                                          }
                     # lo agregue para buscar el producto y si existe lo selecciono sino lo creo
                     if self.env['product.template'].search_count([('name', '=', line_nc_prueba.descripcion)]) >= 1:
                         print('Este producto ya existe')
                         print(self.env['product.template'].search_count([('name', '=', line_nc_prueba.descripcion)]))
                     if self.env['product.template'].search_count([('name', '=', line_nc_prueba.descripcion)]) == 0:
                         print('El producto no existe')
                         crear_productos_nc = self.env['product.template'].create(response_products_nc)
                         self.env.cr.commit()
                     #Datos de cada producto/servicio

                     #Revisar
                     #diccionario detalle de nota de credito
                     global discount_mod
                     discount_mod = 0.0
                     if (((line_nc_prueba.cantidad * line_nc_prueba.valor_unitario) - (line_nc_prueba.importe)) / (line_nc_prueba.importe)) < 0:
                         discount_mod = ((((line_nc_prueba.cantidad * line_nc_prueba.valor_unitario) - (line_nc_prueba.importe)) / (line_nc_prueba.importe)) * (100)) * (-1)
                     if (((line_nc_prueba.cantidad * line_nc_prueba.valor_unitario) - (line_nc_prueba.importe)) / (line_nc_prueba.importe)) == 0:
                         discount_mod = 0.0

                     recordConceptosNcObject = {'move_id': notas_credito_objeto.id,
                                              'product_id': self.env['product.template'].search([('name','=',line_nc_prueba.descripcion)]).id,
                                              'account_id': 34,
                                              'journal_id': 2,
                                              'quantity': line_nc_prueba.cantidad,
                                              'tax_exigible': False,
                                              'exclude_from_invoice_tab': False,
                                              'price_unit': line_nc_prueba.valor_unitario,
                                              'debit': 0,
                                              'credit': line_nc_prueba.importe,
                                              'balance': line_nc_prueba.importe * (-1),
                                              'amount_currency': line_nc_prueba.importe * (-1),
                                              'price_subtotal': line_nc_prueba.importe,
                                              #'price_total': line_nc.importe,
                                              'currency_id': self.env['res.currency'].search([('name', '=', rec_notas_credito[0].moneda)]).id,
                                              'product_uom_id': 1,
                                              'parent_state': 'draft',
                                              'company_currency_id': self.env['res.currency'].search([('name', '=', rec_notas_credito[0].moneda)]).id,
                                              'partner_id': line_contact_nc.id,
                                              'tax_base_amount': 0,
                                              'amount_residual': 0,
                                              'amount_residual_currency': 0,
                                              'company_id': 1,
                                              'account_root_id': 54048,
                                              'sequence': 10,
                                              'discount': discount_mod
                                              }
                     print('RECORDS LINEA CONCEPTOS NC')
                     print(recordConceptosNcObject)

                     notas_credito_detalle_objeto = self.env['account.move.line'].with_context(
                     check_move_validity=False).create(recordConceptosNcObject)
                     self.env.cr.commit()

                 #Descarga de pagos (REP'S)
        cfdis_objeto_pago = session.query(PagosDocRel).filter(
            PagosDocRel.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).all()

        for cfdi_pago in cfdis_objeto_pago:
            print('Pagos')

            if self.env['pagos_doctos_rel'].search_count([('id_pago', '=', str(cfdi_pago.id_pago))]) > 0:
                print('EL FOLIO DE PAGO YA EXISTE')

            if self.env['pagos_doctos_rel'].search_count([('id_pago', '=', str(cfdi_pago.id_pago))]) == 0:
                dic_cfdi_pago = {'name': str(cfdi_pago.guid_document),
                                 'id_pago': cfdi_pago.id_pago,
                                 'id_documento': cfdi_pago.id_documento,
                                 'serie': cfdi_pago.serie,
                                 'folio': cfdi_pago.folio,
                                 'moneda_dr': cfdi_pago.moneda_dr,
                                 'moneda_dr_desc': cfdi_pago.moneda_dr_desc,
                                 'tipo_cambio_dr': cfdi_pago.tipo_cambio_dr,
                                 'metodo_pago_dr': cfdi_pago.metodo_pago_dr,
                                 'metodo_pago_dr_desc': cfdi_pago.metodo_pago_dr_desc,
                                 'num_parcialidad': cfdi_pago.num_parcialidad,
                                 'imp_saldo_ant': cfdi_pago.imp_saldo_ant,
                                 'imp_pagado': cfdi_pago.imp_pagado,
                                 'imp_saldo_insoluto': cfdi_pago.imp_saldo_insoluto,
                                 'fecha':cfdi_pago.fecha,
                                 'account_move_pagos_rel':self.env['account.move'].search([('uuid', 'ilike', str(cfdi_pago.id_documento))]).id}
                print(dic_cfdi_pago)

                cfdi_rep_record = self.env['pagos_doctos_rel'].create(dic_cfdi_pago)
                self.env.cr.commit()

        session.close()
        engine.dispose()