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
# Clase de movimientos de recepcion
class CortesDataOrden(Base):
    __tablename__ = 'REP_OrdenesCorte2'
    id_orden_corte = Column('IdOrdenCorte', Integer(), primary_key=True)
    fecha = Column('Fecha', DateTime)
    sader = Column('NoRegistro',String(500))
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
    fecha = Column('Fecha',DateTime)
    cajas_entregadas = Column('CajasMixto',Integer())
    ticket = Column('Ticket', String(200))
    pesototal = Column('PesoNeto',Integer())


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

class FletesCrear(models.Model):
    _name = "fletes_modelo_tts"

    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Id orden corte',tracking=True,track_visibility='always')

    fecha = fields.Date(string='Fecha',tracking=True,track_visibility='always')

    #Un Many2one siempre recibe un entero
    huerta = fields.Many2one(comodel_name='huertas', string='Huerta',tracking=True,track_visibility='always')

    ubicacion_municipio = fields.Many2one(comodel_name='localidad', string='Localidad',tracking=True,track_visibility='always')

    poblacion = fields.Many2one(comodel_name='poblacion', string='Poblacion',tracking=True,track_visibility='always')

    estado = fields.Many2one(comodel_name='estado', string='Estado',tracking=True,track_visibility='always')

    municipio = fields.Many2one(comodel_name='ciudad', string='Municipio',tracking=True,track_visibility='always')

    status = fields.Char(string='Status fruta',tracking=True,track_visibility='always')

    nombre_produtor_modelo_tts = fields.Many2one(comodel_name='res.partner', string='Nombre productor',tracking=True,track_visibility='always')

    nombre_transportista = fields.Many2one(comodel_name='res.partner', string='Nombre transportista',tracking=True,track_visibility='always')

    nombre_jefe_cuadrilla = fields.Many2one(comodel_name='res.partner', string='Jefe de cuadrilla',tracking=True,track_visibility='always')

    observaciones = fields.Text(string='Observaciones',tracking=True,track_visibility='always')

    impuestos = fields.One2many('retenciones', 'fletes_rel', string='Retencion extra',tracking=True,track_visibility='always')

    importe_total_fletes_municipio = fields.Float(string='Importe municipio', compute='_compute_tarifa_final_fleteo',tracking=True,track_visibility='always')

    importe_mas_retencion = fields.Float(string='Tarifa final', compute='_compute_tarifa_final',tracking=True,track_visibility='always')

    beneficiario = fields.Many2one(related='nombre_transportista.beneficiario_flete', string='Beneficiario',tracking=True,track_visibility='always')

    cajas_lote_fletes = fields.Integer(string='Cajas lote')

    cajas_mixtos_fletes = fields.Integer(string='Cajas en camion')

    peso_promedio_caja = fields.Float(string='Peso promedio cajas', )

    state = fields.Selection(selection=[('alerta_exeso', 'Exceso'), ('alerta_faltante', 'Faltante'),
                                        ('margen', 'margen'), ('bloqueo', 'Bloqueo')]
                             , default='margen', string='Estados', copy=False, )
    peso_producto = fields.Float(string='Peso productor')

    alerta_peso_cajas = fields.Char(string='Alerta de Peso')

    def _compute_tarifa_final(self):
        suma = 0.0
        for rec in self:
            for line in rec.impuestos:
                suma = suma + line.importe
            rec.importe_mas_retencion = rec.importe_total_fletes_municipio + suma
            suma = 0.0
    @api.model
    def create(self, variables):
        if variables['peso_promedio_caja'] > 28:
            variables['state'] = 'alerta_exeso'
            variables['alerta_peso_cajas'] = '***CAJAS CON MAS DE 28kg***'
        if variables['peso_promedio_caja'] < 22:
            variables['state'] = 'alerta_faltante'
            variables['alerta_peso_cajas'] = '***CAJAS CON MENOS DE 22kg***'
        return super(FletesCrear, self).create(variables)


    def _compute_tarifa_final_fleteo(self):
        for record_fletes in self:
            importe_municipio_flete = 0.0
            res_tarifa_amount = record_fletes.env['tarifas_fletes'].search([('name', '=',record_fletes.municipio.id)]).tarifa_importe_final_flete_municipio
            record_fletes.importe_total_fletes_municipio = res_tarifa_amount



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
            print(j.fecha_inicial)
        print('que pasa con j')

        # realizo el query en la clase "CortesDataOrden" para obtener un resultado
        #filtrado por fechas

        fletes_object = session.query(CortesDataOrden, CortesCajasTTS) .filter(
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

            # create method for record and search register
            if self.env['res.partner'].search_count([('name','=',record[0].nombre_transportista)]) >= 1:
                id_transportista = self.env['res.partner'].search([('name', '=', record[0].nombre_transportista)],limit=1).id
            if self.env['res.partner'].search_count([('name','=',record[0].nombre_transportista)]) == 0:
               rec_obj_transportista_dic = {'name': record[0].nombre_transportista, }
               id_transportista = self.env['res.partner'].create(rec_obj_transportista_dic)
               id_transportista = id_transportista.id
               self.env.cr.commit()

            if self.env['localidad'].search_count([('name', '=', record[0].ubicacion)]) >= 1:
                id_ubicacion_municipio = self.env['localidad'].search([('name', '=', record[0].ubicacion)],limit=1).id
            if self.env['localidad'].search_count([('name', '=', record[0].ubicacion)]) == 0:
                rec_obj_localidad_dic = {'name': record[0].ubicacion}
                id_ubicacion_municipio = self.env['localidad'].create(rec_obj_localidad_dic)
                id_ubicacion_municipio = id_ubicacion_municipio.id
                self.env.cr.commit()

            if self.env['poblacion'].search_count([('name', '=', record[0].poblacion)]) >= 1:
                id_poblacion = self.env['poblacion'].search([('name', '=', record[0].poblacion)],limit=1).id
            if self.env['poblacion'].search_count([('name', '=', record[0].poblacion)]) == 0:
                rec_obj_poblacion_dic = {'name': record[0].poblacion, }
                id_poblacion = self.env['poblacion'].create(rec_obj_poblacion_dic)
                id_poblacion = id_poblacion.id
                self.env.cr.commit()

            if self.env['ciudad'].search_count([('name','=',record[0].municipio)]) >= 1:
                id_municipio = self.env['ciudad'].search([('name', '=', record[0].municipio)],limit=1).id
            if self.env['ciudad'].search_count([('name', '=', record[0].municipio)]) == 0:
               rec_obj_municipio_dic_dic = {'name': record[0].municipio, }
               id_municipio = self.env['ciudad'].create(rec_obj_municipio_dic_dic)
               id_municipio = id_municipio.id
               self.env.cr.commit()

            if self.env['estado'].search_count([('name','=',record[0].estado)]) >= 1:
                id_estado = self.env['estado'].search([('name', '=', record[0].estado)],limit=1).id
            if self.env['estado'].search_count([('name','=',record[0].estado)]) == 0:
               rec_obj_estado_dic = {'name': record[0].estado, }
               id_estado = self.env['estado'].create(rec_obj_estado_dic)
               id_estado = id_estado.id
               self.env.cr.commit()



            if self.env['res.partner'].search_count([('name','=',record[0].nombre_productor)]) >= 1:
                id_productor = self.env['res.partner'].search([('name', '=', record[0].nombre_productor)],limit=1).id
            if self.env['res.partner'].search_count([('name', '=', record[0].nombre_productor)]) == 0:
               rec_obj_productor_dic = {'name': record[0].nombre_productor, }
               id_productor = self.env['res.partner'].create(rec_obj_productor_dic)
               id_productor = id_productor.id
               self.env.cr.commit()

            if self.env['huertas'].search_count([('sader','=',record[0].sader)]) >= 1:
                id_huerta = self.env['huertas'].search([('sader', '=', record[0].sader)],limit=1).id
            if self.env['huertas'].search_count([('sader','=',record[0].sader)]) == 0:
               rec_obj_huertas_dic = {'name': record[0].huerta,
                                      'sader': record[0].sader,
                                      'productor': self.env['res.partner'].search([('name', '=', record[0].nombre_productor)]).id
                                      }
               id_huerta = self.env['huertas'].create(rec_obj_huertas_dic)
               id_huerta = id_huerta.id
               self.env.cr.commit()

            if self.env['res.partner'].search_count([('name', '=', record[0].nombre_jefe_cuadrilla)]) >= 1:
                id_jefe_cuadrilla = self.env['res.partner'].search(
                    [('name', '=', record[0].nombre_jefe_cuadrilla)],limit=1).id
            if self.env['res.partner'].search_count([('name', '=', record[0].nombre_jefe_cuadrilla)]) == 0:
                rec_obj_jefe_cuadrilla_dic = {'name': record[0].nombre_jefe_cuadrilla, }
                id_jefe_cuadrilla = self.env['res.partner'].create(rec_obj_jefe_cuadrilla_dic)
                id_jefe_cuadrilla = id_jefe_cuadrilla.id
                self.env.cr.commit()



            cajas_camion = record[1].cajas_entregadas
            if cajas_camion == 0:
                cajas_camion = record[1].id_cajas_cortadas

            promediocajas = record[1].pesototal / record[1].id_cajas_cortadas

            rec_obj_fletes_dic = {
                            'name': record[0].id_orden_corte,
                            'fecha': record[0].fecha,
                            'huerta': id_huerta,
                            'poblacion': id_poblacion,
                            'nombre_produtor_modelo_tts': id_productor,
                            'status': record[0].status,
                            'estado': id_estado,
                            'nombre_transportista':id_transportista,
                            'nombre_jefe_cuadrilla':id_jefe_cuadrilla,
                            'municipio': id_municipio,
                            'observaciones': record[0].observaciones,
                            'ubicacion_municipio': id_ubicacion_municipio,
                            'cajas_lote_fletes': record[1].id_cajas_cortadas,
                            'cajas_mixtos_fletes': cajas_camion,
                            'peso_producto': record[1].pesototal,
                            'peso_promedio_caja': promediocajas

                            }
            insert_cajas_de_tts = self.env['fletes_modelo_tts'].create(rec_obj_fletes_dic)


            if record[1].id_cajas_cortadas > 300:
                tarifa_cajas_extra = (((record[1].id_cajas_cortadas - 300) * 15) * 1.16) - (((record[1].id_cajas_cortadas - 300) * 15) * .04)
                id_cajas_extra = self.env['cat_descuentos'].search([('name', '=', 'CAJAS EXTRA')], limit=1)
                recordcajasfletes = {'name': id_cajas_extra.id,
                                     'fletes_rel': insert_cajas_de_tts.id,
                                     'importe': tarifa_cajas_extra, }
                insert_cajas_flete = self.env['retenciones'].create(recordcajasfletes)
                self.env.cr.commit()

            if record[1].cajas_entregadas > 300:
                tarifa_cajas_extra = (((record[1].cajas_entregadas - 300) * 15) * 1.16) - (((record[1].cajas_entregadas - 300) * 15) * .04)
                id_cajas_extra = self.env['cat_descuentos'].search([('name', '=', 'CAJAS EXTRA')], limit=1)
                recordcajasfletes = {'name': id_cajas_extra.id,
                                     'fletes_rel': insert_cajas_de_tts.id,
                                     'importe': tarifa_cajas_extra, }
                insert_cajas_flete = self.env['retenciones'].create(recordcajasfletes)
                self.env.cr.commit()


            print(rec_obj_fletes_dic)
            #response_dic_create = self.env['fletes_modelo_tts'].create(rec_obj_fletes_dic)
            self.env.cr.commit()
        session.close()
        engine.dispose()


