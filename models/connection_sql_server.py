# -*- coding:utf-8 -*-
import pendulum

from odoo import fields, models, api
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String, Float, SmallInteger, Numeric, DateTime, Date
from sqlalchemy import distinct
import logging
import pandas as pd
_logger = logging.getLogger(__name__)

#esta es una linea de prueba

logger = logging.getLogger(__name__)

Base = declarative_base()

'''class CorridaLote(Base):
    __tablename__ = 'REP_SeleccionPallets'
    id = Column('id',Integer(),primary_key=True)
    id_seleccion = Column('idempaque',Integer())
    fecha = Column('fecha',Date)
    id_lote = Column('idlote',Integer())
    peso_neto = Column('pesoneto',String(500))
    producto = Column('producto',String(500))
    presentacion = Column('presentacion',String(500))
    cajas = Column('cajas',Float)
    kilogramos = Column('kilogramos',Float)
    exportacion = Column('exportacion',Float)
    nacional = Column('nacional',Float)
    merma = Column('merma',Float)
    porc_exportacion = Column('porcentajeexportacion',Float)
    porc_nacional = Column('porcentajenacional', Float)
    porc_merma = Column('porcentajemerma', Float)
    id_no_pallet = Column('idnopallet', Integer())'''

class Categoria(Base):
    __tablename__ = 'MOV_EmpaqueResumenCategoria'
    id_categoria = Column('IdLote', Integer(), primary_key=True)
    categoria = Column('categoria', String(200))
    kilogramos = Column('Kilogramos', Float())

class LotesAbiertos(Base):
    __tablename__ = 'MOV_LotesAbiertos'
    id_lote_abierto = Column('IdLote', Integer(), primary_key=True)
    fecha_abierto = Column('Fecha', Date)
    peso_abierto = Column('PesoNeto', Float())
    cajas_abierto = Column('Cajas', Integer())
    huerta_abierto = Column('Huerta', String(200))

class EmpaqueLote(Base):
    __tablename__ = 'MOV_Empaque'
    id_lote_empaque = Column('IdLote', Integer(), primary_key=True)
    id_empaque = Column('IdEmpaque', Integer())
    exportacion_empaque = Column('Exportacion', Float())
    nacional_empaque = Column('Nacional', Float())
    merma_empaque = Column('Merma', Float())
    porc_exportacion = Column('PorcentajeExportacion', Float())
    porc_nacional = Column('PorcentajeNacional', Float())
    porc_merma = Column('PorcentajeMerma', Float())

class CorridaLote2(Base):
    __tablename__ = 'reporte_seleccion_id'
    #observaciones = Column('observaciones', String(500))
    id = Column('ID', Integer())
    id_lote = Column('IdLote', Integer())
    id_seleccion = Column('IdEmpaque', Integer())
    fecha = Column('Fecha', Date)
    peso_neto = Column('PesoNeto', Float())
    producto = Column('Categoria', String(200), primary_key=True)
    exportacion = Column('Exportacion', Float())
    nacional = Column('Nacional', Float())
    merma = Column('Merma', Float)
    porc_exportacion = Column('PorcentajeExportacion', Float)
    porc_nacional = Column('PorcentajeNacional', Float())
    porc_merma = Column('PorcentajeMerma', Float)
    kilogramos = Column('Kilogramos', Float())
    cajas = Column('Cajas', Float())
    huerta = Column('Huerta', String(200))
    lote_recepcion = Column('IdLoteRecepcion',Integer())
    orden_corte = Column('OrdenCorte', Integer())
    tipo_corte = Column('TipoCorte', String(200))

class LotesData(Base):
    __tablename__ = 'Cuentas_Por_Pagar_Productores_Odoo'
    id_movimiento = Column('IdCreditoMovimiento', Integer(), primary_key=True)
    clave = Column('Clave', String(100))
    id_lote = Column('IdLote', Integer())
    nombre_proveedor = Column('Nombre', String(200))
    huerta = Column('huerta',String(200))
    sader = Column('sader',String(200))
    fecha = Column('FechaRecepcion', Date)
    tipo_movimiento = Column('CreditoTipoMovimiento', String(100))
    precio_u = Column('PrecioU',Float)
    importe = Column('Importe', Float)
    cantidad = Column('Kilogramos', Float)
    poblacion = Column('Poblacion',String(200))
    jefe_acopio = Column('JefeAcopio',String(200))
    cajas = Column('Cajas',Integer())
    tipo_corte = Column('TipoCorte',String(200))
    fecha_empacado = Column('FechaEmpacado',Date)
    tickets = Column('Tickets',String(200))
    referencia = Column('Referencia',String(200))
    observaciones = Column('Observaciones', String(200))
    id_productor = Column('IdProductor', Integer())


class LotesDataProductores(Base):
  #  __table_args__ = {'extend_existing': True}
    __tablename__ = 'CuentasPorPagarProductoresCatalogoOdoo'
    id_lote = Column('IdLote',Integer(), primary_key=True)
    nombre = Column('Nombre', String(200))
    id_productor =Column('IdProductor', Integer())
    fecha = Column('FechaRecepcion', Date)

class LotesDataHuertas(Base):
  #  __table_args__ = {'extend_existing': True}
    __tablename__ = 'CuentasPorPagarHuertasCatalogoOdoo'
    id_lote = Column('IdLote',Integer(), primary_key=True)
    sader = Column('sader', String(200))
    huerta = Column('Huerta',String(500))
    nombre_productor = Column('Nombre',String(500))
    id_productor =Column('IdProductor', Integer())
    fecha = Column('FechaRecepcion', Date)

class LotesDataJefeAcopio(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'CuentasPorPagarProductoresCatalogoOdoo'
    id_lote = Column('IdLote',Integer(), primary_key=True)
    nombre = Column('JefeAcopio', String(200))
    id_productor =Column('IdProductor', Integer())
    fecha = Column('FechaRecepcion', Date)

class RecepcionesPorLote(Base):
    __tablename__ = 'View_RecepcionesLotes_ODOO14'
    id_recepcion = Column('IdLoteRecepcion',Integer(),primary_key=True)
    id_lote = Column('NumeroLote',Integer())
    id_orden_corte = Column('OrdenCorte',String(500))
    fecha = Column('FechaR',Date)
    ticket = Column('Ticket',String(500))
    peso_bruto = Column('PesoBruto',Float)
    peso_tara = Column('PesoTara',Float)
    peso_neto = Column('PesoNeto',Float)
    peso_bascula_productor = Column('PesoBasculaProductor',Float)


class Session():
    def session(engine):
        Session = sessionmaker(bind=engine)
        # session = Session()
        session = scoped_session(Session)

        return session

    def engine():
        server_addres = 'e3210dfde5c7.sn.mynetname.net' + ":" + "49703"
        #server_addres = '192.168.88.214' + ":" + "49703"
        database = 'DLC'
        username = 'sa'
        password = 'HideMyPassBm123*'

        arguments = dict(server=server_addres, user=username,
                         password=password, database=database, charset="utf8")

        engine = sa.create_engine('mssql+pymssql:///', connect_args=arguments)
        return engine

    # Modelo de odoo


class Lotes(models.Model):
    _name = "lotes"
    _inherit=['mail.thread','mail.activity.mixin','portal.mixin']
    _description='Lotes Module'
    # reestriccion por db para id del lote type_unique=(name)
    _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Datos duplicados en el rango solicitado, revisa tu rango')]

  #    @api.constrains('name')
  #   def _name_valid(self):

  #          raise exceptions.ValidationError("Datos duplicados en el rango solicitado, revisa tu rango")

    name = fields.Integer(string='Numero de lote')

    clave = fields.Char(string='Clave')

    id_credito_mov = fields.Integer(string='IdCreditoMovimiento')

    nombre_proveedor = fields.Char(string='Nombre')

    id_partner = fields.Many2one(string='Nombre', comodel_name='res.partner')

    huerta = fields.Char(string='Huerta')

    sader = fields.Many2one(String='Sader',comodel_name='huertas')

    sader_code = fields.Char(String='Sader Codigo', related='sader.sader')

    fecha = fields.Date(string='Fecha')

    tipo_movimiento = fields.Char(string='Tipo de movimiento')

    abono = fields.Float(string='Abono',store=True)

    saldo_pendiente = fields.Float(string='Saldo pendiente')

    kilogramos_pendientes = fields.Float(string='Kg Pendientes',auto_join=True)

    importe = fields.Float(string='Importe',digits='Product Price')

    precio_u = fields.Float(string='Precio Unitario')

    cantidad = fields.Float(string='Kilogramos',store=True)

    observaciones = fields.Char(string='Observaciones')

    poblacion = fields.Char(string='Población')

    jefe_acopio = fields.Many2one(string='Jefe Acopio',comodel_name='res.partner')

    cajas = fields.Char(string='Cajas')

    tipo_corte = fields.Char(String='Tipo de corte')

    fecha_empacado = fields.Date(string='Fecha Empacado')

    tickets = fields.Char(string='Tickets')

    referencia = fields.Char(string='Referencia')

    active = fields.Boolean(string='Activo', default=True)

    es_doc_bico = fields.Boolean(string='¿Bico?',default=True)

    doc_bico = fields.One2many('sat_documentos_lotes','bico_lotes_rel',string='Bico')

    adicionales = fields.Char(string='Adicionales',tracking=True,track_visibility='always') #onchange

    #cfdis_relacionados = fields.Many2many('account.move','lotes_cfdi','lotes_id','account_move_id',tracking=True,track_visibility='onchange',string='Cfdis Relacionados')

    status_facturas = fields.Char(string='Estatus Factura',store=True)

    status_pago = fields.Char(string='Estatus Pago')

    status_provision = fields.Char(string='Provision Lotes',compute='compute_abonos',
                                   copy=False,tracking=True,track_visibility='always',readonly=True,store=False)

    seats = fields.Integer(string='Numeber of seats')

    id_productor = fields.Integer(string='Id Productor In')

    kilogramos_abonados_v = fields.Float(string='Kg abonados')

    kilogramos_pendientes_v = fields.Float(string='Kg Pendientes',compute='compute_abonos',store=True)

    fecha_contabilizacion = fields.Datetime(string='Fecha Aprobado', copy=False,tracking=True,track_visibility='always')

    lotes_detalle = fields.One2many('lotes_account_move_line','name',string='Lotes Detalle')

    no_movimientos = fields.One2many('lotes_account_move_line', 'name', string='No. Movimientos')
    
    reporte_seleccion = fields.One2many('lotes_corrida', 'id_lote2', string='Sincronizar Selección')


    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('Contabilizado Lote', 'Contabilizado Lote'),
        ('Contabilizado Cfdi', 'Contabilizado Cfdi'),

    ], default='borrador', string='Estados', copy=False,tracking=True,track_visibility='always',readonly=True,store=True)

    estado_pago = fields.Selection(related='lotes_detalle.estado_factura',string='Estado Pago')

    uuid = fields.Char(related='lotes_detalle.uuid')

    serie = fields.Char(related='lotes_detalle.serie')

    folio = fields.Char(related='lotes_detalle.folio')

    estado_factura = fields.Selection(string='Estado Factura',related='lotes_detalle.estado_pago')

    uuid = fields.Char(related='lotes_detalle.uuid')

    uuid_search = fields.Char(string='Uuid',compute='listar_datos_cfdi')

    serie_search = fields.Char(string='Serie', compute='listar_datos_cfdi')

    folio_search = fields.Char(string='Folio', compute='listar_datos_cfdi')

    emisor_search = fields.Char(string='Emisor', compute='listar_datos_cfdi')

    fecha_factura_search = fields.Char(string='Fecha Factura',compute='listar_datos_cfdi')

    total_lote_saldos_mod = fields.Float(string='Total Saldo')

    reporte_saldos_rel = fields.Many2one('reporte_saldos',string='Reporte Saldos Rel')

    estatus_pago_res = fields.Char(string='Estatus Res',compute='estatus_prov')

    fecha_descarga_seleccion = fields.Datetime(string='Ultima descarga', default='lambda')
    fecha_descarga_seleccion_string = fields.Char(string='Ultima actualizacion', compute='Fecha_selection')

    user_descarga = fields.Char(string='usuario')
    def Fecha_selection(self):
        for fecha in self:
            fecha.fecha_descarga_seleccion_string = ' '
            if fecha.user_descarga is False:
                fecha.user_descarga = ' '
            if str(fecha.fecha_descarga_seleccion) == 'False':
                fecha.fecha_descarga_seleccion_string = ' '
            else:
                fecha.fecha_descarga_seleccion_string = str(fecha.fecha_descarga_seleccion)+ ' ' + fecha.user_descarga

    def download_corrida_lote(self):
        engine = Session.engine()
        session = Session.session(engine)
        for line in self:
            line.fecha_descarga_seleccion = fields.Datetime.now()
            line.user_descarga = self.env.user.name
            vals = []
            rep_seleccion_dic = [ ]
            suma1 = 0.0
            suma = []
            categoria = ''

            sin_duplicidad = []

            lotes_corrida_query = session.query(EmpaqueLote, LotesAbiertos, Categoria) \
                .filter(EmpaqueLote.id_lote_empaque == line.name)\
                .filter(LotesAbiertos.id_lote_abierto == line.name)\
                .filter(Categoria.id_categoria == line.name).order_by(Categoria.categoria).all()


            lotes_corrida = session.query(CorridaLote2).filter(CorridaLote2.id_lote == line.name).order_by(CorridaLote2.producto).all()
            porcentaje = 0.0
            for line_iterate in lotes_corrida:

                if line_iterate.producto not in sin_duplicidad:
                    sin_duplicidad.append(line_iterate.producto)
                    porcentaje = (line_iterate.kilogramos*100)/line_iterate.peso_neto
                    rep_seleccion_dic =(0,0, {'name': line_iterate.id_seleccion,
                                     'fecha': line_iterate.fecha,
                                     'id_lote': line_iterate.id_lote, #line.env['lotes'].search([('name', '=', line_iterate.id_lote)]).id,
                                     'peso_neto': line_iterate.peso_neto,
                                     'producto': line_iterate.producto,
                                     #'presentacion': line_iterate.presentacion,
                                     'cajas': line_iterate.cajas,
                                     'kilogramos': line_iterate.kilogramos,
                                     'exportacion': line_iterate.exportacion,
                                     'nacional': line_iterate.nacional,
                                     'merma': line_iterate.merma,
                                     'porc_exportacion': line_iterate.porc_exportacion,
                                     'porc_nacional': line_iterate.porc_nacional,
                                     'porc_merma': line_iterate.porc_merma,
                                     'porcentaje_produc': porcentaje,
                                     'lote_recepcion':line_iterate.lote_recepcion,
                                     'orden_corte_lote': line_iterate.orden_corte,
                                     'tipo_corte':line_iterate.tipo_corte,
                                     #'id_no_pallet': line_iterate.id_no_pallet,
                                      })

                    vals.append(rep_seleccion_dic)
            print('valsx', vals)
            line.reporte_seleccion = [5, 0, 0]
            line.reporte_seleccion = vals
            vals = []


    @api.depends('cantidad','abono')
    def estatus_prov(self):
        init = 0
        for line in self:
            init = line.cantidad - line.abono
            if init == 0:
               line.estatus_pago_res = 'Saldado'
            else:
                line.estatus_pago_res = 'Pendiente'


    @api.depends('uuid_search','serie_search','folio_search','emisor_search')
    def listar_datos_cfdi(self):
        for line in self:
            uuid_res = line.env['lotes_account_move_line'].search([('name.name', '=', line.name)]).mapped('uuid')
            serie_res = line.env['lotes_account_move_line'].search([('name.name', '=', line.name)]).mapped('serie')
            folio_res = line.env['lotes_account_move_line'].search([('name.name', '=', line.name)]).mapped('folio')
            emisor_res = line.env['lotes_account_move_line'].search([('name.name', '=', line.name)]).mapped('id_partner.name')
            fecha_factura_res = line.env['lotes_account_move_line'].search([('name.name', '=', line.name)]).mapped('fecha_factura')
            line.uuid_search = uuid_res
            line.serie_search = serie_res
            line.folio_search = folio_res
            line.emisor_search = emisor_res
            line.fecha_factura_search = fecha_factura_res


    def compute_abonos(self):
        for lote in self:
            records_sum = sum(lote.env["lotes_account_move_line"].search([('name.name', '=', lote.name)]).mapped('abono_kilogramos'))
            lote.kilogramos_abonados_v = records_sum
            if lote.cantidad == records_sum:
                lote.status_provision = 'Provisionado Totalmente'
            if lote.cantidad > records_sum and records_sum > 0:
                lote.status_provision = 'Provisinado Parcialmente'
            if records_sum == 0:
                lote.status_provision = 'No Provisionado'
            lote.kilogramos_abonados_v = records_sum
            lote.kilogramos_pendientes_v = lote.cantidad - records_sum
            lote.abono = records_sum


    def contabilizar_lote(self):
        for line in self:
         line.state = 'Contabilizado Lote'
         line.fecha_contabilizacion = fields.Datetime.now()

    def contabilizar_cfdi(self):
        for line in self:
         line.state = 'Contabilizado Cfdi'
         line.fecha_contabilizacion = fields.Datetime.now()


    def convertir_a_borrador(self):
        for line in self:
         line.state = 'borrador'



    @api.depends('cfdis_relacionados')
    def get_importe_factura(self):
        global total
        rec_facturas = 0
        for rec_facturas in self:
            total = 0.0
        for line in rec_facturas.cfdis_relacionados:
         total += line.amount_total
        if self.importe == total:
            self.status_facturas = 'Completo'
        if self.importe != total:
            self.status_facturas = 'Incompleto'


    @api.onchange('cfdis_relacionados')
    def _onchange_cfdis(self):

     if len(self.cfdis_relacionados) == 0:
        print(0)
     if len(self.cfdis_relacionados) > 0:
        return self.get_importe_factura()

    def _onchange_cfdis2(self):

     if len(self.cfdis_relacionados) == 0:
        return self.get_importe_factura()
     if len(self.cfdis_relacionados) > 0:
        return self.get_importe_factura()

#Descarga datos TTS
    def download_data(self):
        engine = Session.engine()
        session = Session.session(engine)

        # valores globales para llamar el objeto fuera del modelo
        global lotes_object
        # ordenar por nombre
        # lote_inicial_object.search([],order='name')
        rango_lotes_obj = self.env['lotes_wizard']
        contactos_obj = self.env['res.partner']
        huertas_obj = self.env['huertas']
        recepciones_lotes_obj = self.env['recepciones_lotes']

        for i in rango_lotes_obj.search([], order='id desc', limit=1):
            # ordenar por nombre
            # lote_inicial_object.search([],order='name')
            i.fecha_inicial
            i.fecha_final
        #Query que genera unico el catalogo de productores dependiendo del rango de lotes
        lotes_object_cat_productores = session.query(distinct(LotesDataProductores.id_productor),LotesDataProductores.nombre)\
            .filter(LotesDataProductores.fecha.between(i.fecha_inicial, i.fecha_final)).all()
        lotes_object_cat_huertas = session.query(distinct(LotesDataHuertas.sader),LotesDataHuertas.huerta,LotesDataHuertas.id_productor)\
            .filter(LotesDataHuertas.fecha.between(i.fecha_inicial, i.fecha_final)).all()
        lotes_object_cat_jefe_acopio = session.query(distinct(LotesDataJefeAcopio.nombre),LotesDataJefeAcopio.nombre)\
            .filter(LotesDataJefeAcopio.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).all()

        #print(recepciones_lotes_object_data)


        #arreglo que recorre el objeto
        for record2 in lotes_object_cat_productores:
            #variable global para respuesta del query
            global response
            response = ''
            #agregar datos de al diccionario python
            id_category_productor = self.env.ref('cuentas_por_pagar.category_productor')
            response = {'id_productor': record2[0],
                        'name': record2[1],
                        'category_id': id_category_productor}
            #valida que no halla registros repetidos contado los registros coincidentes
            if self.env['res.partner'].search_count([('id_productor', '=', record2[0])]) >= 1:
                print('Este contacto ya existe')
                print(self.env['res.partner'].search_count([('id_productor', '=', record2[0])]))
            #valida y si no hay registros coincidentes almacena un nuevo registro
            if self.env['res.partner'].search_count([('id_productor', '=', record2[0])]) == 0:
                rec = self.env['res.partner'].create(response)
                self.env.cr.commit()
                print(response)

                # arreglo que recorre el objeto
        for record3 in lotes_object_cat_huertas:
                # variable global para respuesta del query
            global response2
            response2 = ''
            for row in contactos_obj.search([('id_productor', '=', record3.id_productor)]):
                row.id

                # agregar datos de al diccionario python
            response2 = {'name': record3[1],
                         'sader': record3[0],
                          'productor':row.id}
                # valida que no halla registros repetidos contado los registros coincidentes
            if self.env['huertas'].search_count([('sader', '=', record3[0])]) >= 1:
                print('Este huerto ya existe')
                print(self.env['huertas'].search_count([('sader', '=', record3[0])]))
                # valida y si no hay registros coincidentes almacena un nuevo registro
            if self.env['huertas'].search_count([('sader', '=', record3[0])]) == 0:
                rec2 = self.env['huertas'].create(response2)
                self.env.cr.commit()

        for record4 in lotes_object_cat_jefe_acopio:
                # variable global para respuesta del query
            global response3
            response3 = ''
                # agregar datos de al diccionario python
            response3 = {'name': record4[0]}
                # valida que no halla registros repetidos contado los registros coincidentes
            if self.env['res.partner'].search_count([('name', '=', record4[0])]) >= 1:
                print('Este huerto ya existe')
                print(self.env['res.partner'].search_count([('name', '=', record4[0])]))
                # valida y si no hay registros coincidentes almacena un nuevo registro
            if self.env['res.partner'].search_count([('name', '=', record4[0])]) == 0:
                rec3 = self.env['res.partner'].create(response3)
                self.env.cr.commit()

        #query para filtrar por rango los lotes
        lotes_object = session.query(LotesData).filter(LotesData.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).all()
        #este arreglo recorre el query
        for record in lotes_object:
            global recordObject
            if self.env['lotes'].search_count([('name', '=', record.id_lote)]) >= 1:
             print('Folio de lote repetido')
            if self.env['lotes'].search_count([('name', '=', record.id_lote)]) == 0:
            #este arreglo busca coincidencias con el nombre del productor en odoo y lo relaciona si ya esta dado de alta
             for line in contactos_obj.search([('id_productor', '=', record.id_productor)]):
                line.id
            # este arreglo busca coincidencias con el nombre del productor en odoo y lo relaciona si ya esta dado de alta
             for line2 in huertas_obj.search([('sader', '=', record.sader)]):
                line2.id
             for line3 in contactos_obj.search([('name', '=', record.jefe_acopio)]):
                line3.id
             #Inserta las recepciones de cada linea del lote
             recepciones_lotes_object_data = session.query(RecepcionesPorLote).filter(
                RecepcionesPorLote.fecha.between(i.fecha_inicial, i.fecha_final)).filter(RecepcionesPorLote.id_lote == record.id_lote)\
                 .all()
             for line_recepciones in recepciones_lotes_object_data:
                 global recordRecepcionesObject

                 recordRecepcionesObject = {'name':line_recepciones.id_recepcion,
                                            'id_lote':line_recepciones.id_lote,
                                            'id_orden_corte':line_recepciones.id_orden_corte,
                                            'fecha':line_recepciones.fecha,
                                            'ticket':line_recepciones.ticket,
                                            'peso_bruto':line_recepciones.peso_bruto,
                                            'peso_tara':line_recepciones.peso_tara,
                                            'peso_neto':line_recepciones.peso_neto,
                                            'peso_bascula_productor':line_recepciones.peso_bascula_productor}


                 #insert = self.env['recepciones_lotes'].create(recordRecepcionesObject)
                 #self.env.cr.commit()

             recordObject = {'name': record.id_lote,
                            'id_credito_mov': record.id_movimiento,
                            'clave': record.clave,
                            'id_partner': line.id,
                           # 'huerta': record.huerta,
                            'sader': line2.id,
                            'fecha': record.fecha,
                            'tipo_movimiento': record.tipo_movimiento,
                            'importe': record.precio_u*record.cantidad,
                            'precio_u': record.precio_u,
                            'cantidad': record.cantidad,
                            'observaciones': record.observaciones,
                            'poblacion':record.poblacion,
                            'jefe_acopio':line3.id,
                            'cajas':record.cajas,
                            'tipo_corte': record.tipo_corte,
                            'fecha_empacado': record.fecha_empacado,
                            'tickets': record.tickets,
                            'referencia': record.referencia,
                            'saldo_pendiente':record.cantidad*record.precio_u,
                            'kilogramos_pendientes':record.cantidad}
             insert = self.env['lotes'].create(recordObject)
             self.env.cr.commit()

        session.close()
        engine.dispose()





