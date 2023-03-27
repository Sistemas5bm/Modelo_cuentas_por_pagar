# -*- coding:utf-8 -*-
import requests

from odoo import fields, models, api
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String, Float, SmallInteger, Numeric, DateTime, Date
from sqlalchemy import distinct
import logging

_logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

Base = declarative_base()

#Clase de movimientos de recepcion
class CortesData(Base):
    __tablename__ = 'ZZZ_RecepcionLotes2'
    id_acuerdo = Column('IdAcuerdo', Integer())
    id_orden_corte = Column('IdOrdenCorte', Integer())
    id_lote_recepcion = Column('IdLoteRecepcion', Integer(), primary_key=True)
    nombre_productor = Column('Nombre', String(500))
    huerta = Column('Huerta',String(500))
    sader = Column('NoRegistro',String(500))
    fecha = Column('Fecha',DateTime)
    poblacion = Column('Poblacion', String(500))
    tipo_corte = Column('TipoCorte', String(500))
    precio = Column('Precio',Float)
    transportista = Column('Expr2', String(500))
    empresa_corte = Column('Expr3', String(500))
    jefe_acopio = Column('Expr4',String(200))
    candado = Column('Candado',String(200))
    cajas_entregadas = Column('CajasCortadas',Integer())
    peso_neto = Column('PesoNeto',Float)
    peso_productor = Column('PesoBasculaProductor',Float)
    bico = Column('COPREF',String(200))
    ticket = Column('Ticket', String(200))
    id_productor = Column('IdProductor',Integer())
    id_jefe_cuadrilla = Column('IdJefeCuadrilla',Integer())
    id_lote = Column('IdLote', Integer())

#Clase de movimientos de recepcion para proveedor
class CorteCatData(Base):
  #  __table_args__ = {'extend_existing': True}
    __tablename__ = 'ODOO_CuentasPorPagarCorteCatalogoProveedores'
    id_lote_recepcion = Column('IdLoteRecepcion',Integer(), primary_key=True)
    fecha = Column('Fecha', DateTime)
    empresa_corte = Column('Expr3', String(500))
    id_jefe_cuadrilla = Column('IdJefeCuadrilla',Integer())
    id_productor = Column('IdProductor',Integer())

#Clase de movimientos de recepcion para huertos
class CorteCatHuertasData(Base):
    #  __table_args__ = {'extend_existing': True}
    __tablename__ = 'ODOO_CuentasPorPagarCorteCatalogoHuertas'
    id_lote_recepcion = Column('IdLoteRecepcion', Integer(), primary_key=True)
    huerta = Column('huerta', String(500))
    sader = Column('NoRegistro',String(500))
    id_productor = Column('IdProductor',Integer())
    fecha = Column('Fecha', DateTime)

#Clase de movimientos de recepcion para Productores
class CorteCatProductorData(Base):
    __tablename__ = 'ODOO_CuentasPorPagarCorteCatalogoProductores'
    id_lote_recepcion = Column('IdLoteRecepcion', Integer(), primary_key=True)
    nombre = Column('Nombre', String(500))
    id_productor = Column('IdProductor',Integer())
    fecha = Column('Fecha', DateTime)

#Clase de movimientos de recepcion para jefe de acopio
class CorteCatJefeAcopioData(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'ODOO_CuentasPorPagarCorteCatalogoProveedores'
    id_lote_recepcion = Column('IdLoteRecepcion', Integer(), primary_key=True)
    nombre = Column('Expr4', String(500))
    fecha = Column('Fecha', DateTime)

class Session():
    def session(engine):
        Session = sessionmaker(bind=engine)
        # session = Session()
        session = scoped_session(Session)

        return session

    def engine():
        #server_addres = '192.168.88.214' + ":" + "49703"
        server_addres = 'e3210dfde5c7.sn.mynetname.net' + ":" + "49703"
        database = 'TTS'
        username = 'sa'
        password = 'HideMyPassBm123*'

        arguments = dict(server=server_addres, user=username,
                         password=password, database=database, charset="utf8")

        engine = sa.create_engine('mssql+pymssql:///', connect_args=arguments)
        return engine

    # Modelo de odoo


class Cortes(models.Model):
    _name = "cortes"
    _inherit=['mail.thread','mail.activity.mixin','portal.mixin']
    _description = 'Cortes Module'
    # reestriccion por db para id del lote type_unique=(name)
    _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Datos duplicados en el rango solicitado, revisa tu rango')]

#    @api.constrains('name')
 #   def _name_valid(self):

  #          raise exceptions.ValidationError("Datos duplicados en el rango solicitado, revisa tu rango")

    name = fields.Integer(string='Id Lote Recepcion')

    id_acuerdo = fields.Integer(string='Id Acuerdo')

    id_orden_corte = fields.Integer(string='Id Orden Corte')

    nombre_productor = fields.Many2one(string='Nombre del productor',comodel_name='res.partner')

    huerta = fields.Char(string='Huerta')

    sader = fields.Many2one(String='Sader',comodel_name='huertas')

    fecha = fields.Datetime(String='Fecha')

    poblacion = fields.Char(string='Poblacion')

    tipo_corte = fields.Char(string='Tipo De Corte')

    transportista = fields.Char(string='Trasnportista')

    empresa_corte = fields.Many2one(string='Empresa de corte', comodel_name='res.partner')

    jefe_acopio = fields.Many2one(string='Jefe Acopio',comodel_name='res.partner')

    candado = fields.Char(string='Candado')

    cajas_entregadas = fields.Integer(string='Cajas Cortadas')

    peso_neto = fields.Float(string='Peso Neto')

    peso_productor = fields.Float(string='Peso Productor')

    bico = fields.Char(string='Bico')

    ticket = fields.Char(string='Ticket')

    active = fields.Boolean(string='Activo', default=True)

    #campo one2many apunta al campo many2one de cuadrillas para relacionar los campos
    cuadrilla = fields.One2many('cuadrillas','cuadrilla_rel',string='Cuadrillas')

    id_productor = fields.Integer(string='Id Productor')

    id_jefe_cuadrilla = fields.Integer(string='Id Jefe Cuadrilla')

    kilogramos_ajuste = fields.Float(string='Kilogramos de ajuste')

    total_ajuste = fields.Float(string='Total Ajuste',compute='importe_ajuste')

    total_importe = fields.Float(string='Importe',compute='total_cuadrillas')

    id_lote = fields.Integer(string='Id Lote')

    def add_salida_falso(self):
        for linea in self:
            id_salida_falso = self.env['tipo_cuadrillas'].search([('name', '=', 'SALIDA EN FALSO')], limit=1)
            recordObjectAjuste = {'name': id_salida_falso.id,
                                  'cuadrilla_rel': linea.id,
                                  'importe': 3800, }
            insert_cuadrilla_normal = self.env['cuadrillas'].create(recordObjectAjuste)
            return True
    @api.depends('total_ajuste')
    def importe_ajuste(self):
        id_ajuste = self.env['tipo_cuadrillas'].search([('name', '=', 'AJUSTE')], limit=1)
        for line in self:
            records_sum = sum(self.env["cuadrillas"].search([('cuadrilla_rel.name', '=', line.name),('name','=',id_ajuste.id)]).mapped('importe'))*(-1)
            print(records_sum)
            line.total_ajuste = records_sum


    def open_wizard_entrada_kilogramos(self):
        return {'type':'ir.actions.act_window',
                'res_model':'cuadrillas_kilogramos',
                'view_mode':'form',
                'target':'new'}

    @api.depends('total_importe')
    def total_cuadrillas(self):
        for line in self:
            records_sum = sum(line.env["cuadrillas"].search([('cuadrilla_rel.id', '=', line.id)]).mapped('importe'))
            line.total_importe = records_sum


    # calcula las cuadrillas extras y modifica las cuadrillas normales en caso de que las reglas lo requieran
    def calcularCuadrillasExtra(self):
        id = self.env['tipo_cuadrillas'].search([('name', '=', 'CUADRILLA EXTRA')], limit=1)
        id_cuadrilla_normal = self.env['tipo_cuadrillas'].search([('name', '=', 'CUADRILLA NORMAL')], limit=1)
        for linea in self:

            # calculador de tarifa de cuadrilla
            tarifa = 0
            tarifa_2 = 0
            cuadrilla_normal_search = self.env['cuadrillas'].search([('cuadrilla_rel', '=', linea.id),('name','=',id_cuadrilla_normal.id)], limit=1)
            print(cuadrilla_normal_search.id)
            cuadrilla_browse = self.env['cuadrillas'].browse([cuadrilla_normal_search.id])
            if cuadrilla_normal_search.id:

               if linea.peso_productor > 6000:
                  tarifa = 4800
                  tarifa_2 =  linea.peso_productor * 1.65
               if linea.peso_productor < 6000:
                  tarifa = 7500
                  tarifa_2 = 7500
               cuadrilla_browse.write({'importe': tarifa_2})
               self.env.cr.commit()
               print('Logger')
               print(tarifa_2)
            # objeto de datos obtenidos name = cuadrillas normal, cudrilla rel = el id que arrojara el almacenamiento
            # del objeto anterior de los cortes, importe = calculo de cuadrilla por Kilogramos
            recordObjectCuadrillasExtraPorCorte =    {'name': id.id,
                                                      'cuadrilla_rel': linea.id,
                                                      'importe': tarifa}
            insert_cuadrilla_normal = self.env['cuadrillas'].create(recordObjectCuadrillasExtraPorCorte)
            self.env.cr.commit()



    def download_data(self):

        engine = Session.engine()
        session = Session.session(engine)

        # valores globales para llamar el objeto fuera del modelo
        global cortes_object
        # ordenar por nombre
        # lote_inicial_object.search([],order='name')
        rango_cortes_obj = self.env['cortes_wizard']
        contactos_obj = self.env['res.partner']
        huertas_obj = self.env['huertas']
        productor_obj = self.env['res.partner']
        jefe_acopio_obj = self.env['res.partner']
        huerta_prod_obj = self.env['res.partner']

        for i in rango_cortes_obj.search([], order='id desc', limit=1):
            # ordenar por nombre
            # lote_inicial_object.search([],order='name')
            i.fecha_inicial
            i.fecha_final
        #Query que genera unico el catalogo de productores dependiendo del rango de lotes
        cortes_object_cat_empresa_corte = session.query(distinct(CorteCatData.id_jefe_cuadrilla),CorteCatData.empresa_corte).order_by(
                CorteCatData.empresa_corte).filter(CorteCatData.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).all()
        cortes_object_cat_huertas = session.query(distinct(CorteCatHuertasData.sader),CorteCatHuertasData.huerta,CorteCatHuertasData.id_productor).order_by(
            CorteCatHuertasData.sader).filter(CorteCatHuertasData.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).all()
        cortes_object_cat_productores = session.query(distinct(CorteCatProductorData.id_productor),CorteCatProductorData.nombre).order_by(
                CorteCatProductorData.nombre).filter(CorteCatProductorData.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).all()
        cortes_object_cat_jefe_acopio = session.query(distinct(CorteCatJefeAcopioData.nombre)).order_by(
                CorteCatJefeAcopioData.nombre).filter(CorteCatJefeAcopioData.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).all()


        #arreglo que recorre el objeto
        for record2 in cortes_object_cat_empresa_corte:
            #variable global para respuesta del query
            global response
            response = ''
            id_category_jefe_cuadrilla = self.env.ref('cuentas_por_pagar.category_corte')
            #agregar datos de al diccionario python
            response = {'id_jefe_cuadrilla': record2[0],
                        'name': record2[1],
                        'category_id': id_category_jefe_cuadrilla}
            if self.env['res.partner'].search_count([('id_jefe_cuadrilla', '=', record2[0])]) >= 1:
                print('Este contacto ya existe')
                print(self.env['res.partner'].search_count([('id_jefe_cuadrilla', '=', record2[0])]))
            if self.env['res.partner'].search_count([('id_jefe_cuadrilla', '=', record2[0])]) == 0:
                rec = self.env['res.partner'].create(response)
                self.env.cr.commit()
                print(response)

        for record4 in cortes_object_cat_productores:
                # variable global para respuesta del query
            global response3
            response3 = ''
            id_category_productor = self.env.ref('cuentas_por_pagar.category_productor')
                # agregar datos de al diccionario python
            response3 = {'name': record4[1],
                         'id_productor': record4[0],
                         'category_id': id_category_productor}
                # valida que no halla registros repetidos contado los registros coincidentes
            if self.env['res.partner'].search_count([('name', '=', record4[0])]) >= 1:
                    print('Este contacto ya existe')
                    print(self.env['res.partner'].search_count([('name', '=', record4[0])]))
                # valida y si no hay registros coincidentes almacena un nuevo registro
            if self.env['res.partner'].search_count([('name', '=', record4[0])]) == 0:
                    rec3 = self.env['res.partner'].create(response3)
                    self.env.cr.commit()
                    print(response3)




        for record3 in cortes_object_cat_huertas:
                # variable global para respuesta del query
            global response2
            response2 = ''
            for x in contactos_obj.search([('id_productor', '=', record3.id_productor)]):
             x.id
                # agregar datos de al diccionario python
            response2 = {'name': record3[1],
                         'sader': record3[0],
                          'productor':x.id}
                # valida que no halla registros repetidos contado los registros coincidentes
            if self.env['huertas'].search_count([('sader', '=', record3[0])]) >= 1:
                print('Este huerto ya existe')
                print(self.env['huertas'].search_count([('sader', '=', record3[0])]))
                # valida y si no hay registros coincidentes almacena un nuevo registro
            if self.env['huertas'].search_count([('sader', '=', record3[0])]) == 0:
                rec2 = self.env['huertas'].create(response2)
                self.env.cr.commit()
                print(response2)




        #agregar id jefe cuadrilla Modificar
        for record5 in cortes_object_cat_jefe_acopio:
                # variable global para respuesta del query
            global response4
            response4 = ''
            id_category_jefe_cuadrilla = self.env.ref('cuentas_por_pagar.category_jefe_acopio')
                # agregar datos de al diccionario python
            response4 = {'name': record5[0],
                         'category_id': id_category_jefe_cuadrilla}
                # valida que no halla registros repetidos contado los registros coincidentes
            if self.env['res.partner'].search_count([('name', '=', record5[0])]) >= 1:
                    print('Este contacto ya existe')
                    print(self.env['res.partner'].search_count([('name', '=', record5[0])]))
                # valida y si no hay registros coincidentes almacena un nuevo registro
            if self.env['res.partner'].search_count([('name', '=', record5[0])]) == 0:
                    rec4 = self.env['res.partner'].create(response4)
                    self.env.cr.commit()
                    print(response4)
        #query para filtrar por rango los lotes
        cortes_object = session.query(CortesData).filter(CortesData.fecha.cast(Date).between(i.fecha_inicial, i.fecha_final)).all()
        #este arreglo recorre el query
        for record in cortes_object:
            global recordObject

            if self.env['cortes'].search_count([('name', '=', record.id_lote_recepcion)]) >= 1:
             print('Folio de corte repetido')
            if self.env['cortes'].search_count([('name', '=', record.id_lote_recepcion)]) == 0:
            #este arreglo busca coincidencias con el nombre del productor en odoo y lo relaciona si ya esta dado de alta
             for line in contactos_obj.search([('name', '=', record.empresa_corte)]):
                line.id
                # este arreglo busca coincidencias con el nombre del productor en odoo y lo relaciona si ya esta dado de alta
             for line2 in huertas_obj.search([('sader', '=', record.sader)]):
                 line2.id
             for line3 in productor_obj.search([('id_productor', '=', record.id_productor)]):
                 line3.id
             for line4 in jefe_acopio_obj.search([('id_jefe_cuadrilla', '=', record.id_jefe_cuadrilla)]):
                 line4.id
             recordObject = {'name': record.id_lote_recepcion,
                            'id_acuerdo': record.id_acuerdo,
                            'id_orden_corte': record.id_orden_corte,
                            'nombre_productor': line3.id,
                            'huerta': record.huerta,
                            'sader': line2.id,
                            'fecha': record.fecha,
                            'poblacion': record.poblacion,
                            'tipo_corte': record.tipo_corte,
                            'transportista': record.transportista,
                            'empresa_corte': line.id,
                            'jefe_acopio': line4.id,
                            'candado':record.candado,
                            'cajas_entregadas': record.cajas_entregadas,
                            'peso_neto': record.peso_neto,
                            'peso_productor': record.peso_productor,
                            'bico': record.bico,
                            'ticket': record.ticket,
                             'id_lote':record.id_lote,}
             insert_cortes = self.env['cortes'].create(recordObject)
             self.env.cr.commit()
             print(recordObject)
             #obtiene el id externo del gasto de cuadrilla normal
             id = self.env['tipo_cuadrillas'].search([('name', '=', 'CUADRILLA NORMAL')], limit=1)
             #calculador de tarifa de cuadrilla
             tarifa = 0
             if record.peso_productor > 5000:
                 tarifa = record.peso_productor * 1.65
             if record.peso_productor < 5000:
                 tarifa = 7500


             # objeto de datos obtenidos name = cuadrillas normal, cudrilla rel = el id que arrojara el almacenamiento
             # del objeto anterior de los cortes, importe = calculo de cuadrilla por Kilogramos
             recordObjectCuadrillasPorCorte = {'name':id.id,
                                               'cuadrilla_rel':insert_cortes.id,
                                               'importe':tarifa}
             insert_cuadrilla_normal = self.env['cuadrillas'].create(recordObjectCuadrillasPorCorte)
             self.env.cr.commit()

        session.close()
        engine.dispose()