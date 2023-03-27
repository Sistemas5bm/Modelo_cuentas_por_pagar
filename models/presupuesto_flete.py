# -*- coding:utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import sqlalchemy as sa
import pandas as pd
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String, Float, SmallInteger, Numeric, DateTime, Date
from datetime import date,timedelta
from sqlalchemy import distinct
import logging


class PresupuestoFlete(models.Model):
    _name = "presupuesto_flete"

    _description = "Presupuesto de fletes"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin','report.report_xlsx.abstract']

    name = fields.Char(string='Referencia de presupuesto')

    fecha = fields.Datetime(string='Fecha de presupuesto')

    fletes_provisionados = fields.Many2many('fletes_modelo_tts', string='Fletes Presupuestados')
    fletes_provisionados_db = fields.Char(string='ids ')

    state = fields.Selection(string='Estatus',selection=[
        ('validate', 'Validado'),
        ('draft', 'Borrador'),

    ],copy=False, tracking=True, track_visibility='always', readonly=True,store=True,default='draft')

    invoice_rel = fields.Many2one(string='Invoice Rel',related='fletes_provisionados.data_rel')

    budget_total = fields.Float(string='Total Presupuesto', compute='get_sum_budget')
    #budget_total_db = fields.Float(string='Total presupuesto db', related='budget_total')

    facturas_adicionales = fields.One2many('account.move', 'presupuesto_flete_fac_adic_rel', store=True)

    lotes_total = fields.Float(string='Total fletes',compute='get_sum_lotes')

    aditional_invoices_total = fields.Float(string='Facturas adicionales Total', compute='get_sum_aditional_invoices')

    alerta_beneficiario = fields.Char(string='Alerta de beneficiario vacio', compute='alert_beneficiario')
    beneficiario_blanco = fields.Boolean(default=False, store=True )

    clonar_fletes = fields.Boolean(compute='clonar_datos_antiguos')



    #estrae los ids de los fletes en el many2many para los reportes
    def clonar_datos_antiguos(self):
        for rec in self:
            rec.clonar_fletes = True
            ids_almacenados = []
            test = ' '
            for c in rec.fletes_provisionados:
                test = test +' '+ c.name
                ids_almacenados.append(c.name)
            rec.fletes_provisionados_db= ids_almacenados




    #@api.onchange('fletes_provisionados')
    def no_create(self):
        for rec in self:
            rec.beneficiario_blanco = False

            for beneficiario in rec.fletes_provisionados:
                beneficiario.bloqueo_seleccion_presupuesto = False
                if beneficiario.regimen_resico is True:
                    importe_resico = 0.0
                    importe_resico_impuestos = 0.0
                    res_tarifa_amount = beneficiario.env['tarifas_fletes'].search(
                        [('name', '=', beneficiario.municipio.id)])
                    for tarifa in res_tarifa_amount:
                        print('dentro de tarifas')
                        print(tarifa.importe)
                        importe_resico = tarifa.importe - (tarifa.importe * 0.0125)
                        res_impuesto = 0.0
                        res_impuesto2 = 0.0
                        print('importe resico inicial', importe_resico)
                        for rec_line in tarifa.impuestos:
                            if rec_line.tipo_afectacion == 'positive':
                                res_impuesto = (importe_resico) * (rec_line.factor / 100)
                            if rec_line.tipo_afectacion == 'negative':
                                res_impuesto2 = (importe_resico) * ((rec_line.factor / 100) * (-1))

                        importe_resico_impuestos = res_impuesto + res_impuesto2 + importe_resico
                        print(importe_resico_impuestos, 'con resico')
                    cajas_extra_impuestos = 0.0
                    if beneficiario.cajas_mixtos_fletes > 300:
                        cajas_extra_impuestos = (((beneficiario.cajas_mixtos_fletes - 300) * (
                                    15 - (15 * 0.0125))) * 1.16) \
                                                - (((beneficiario.cajas_mixtos_fletes - 300) * (
                                    15 - (15 * 0.0125))) * .04)
                    beneficiario.importe_mas_retencion = cajas_extra_impuestos + importe_resico_impuestos
                    print(cajas_extra_impuestos)
                    print(importe_resico_impuestos,'importe')

                #beneficiario.bloqueo_seleccion_presupuesto = True


                if beneficiario.beneficiario_pdf == '':
                     rec.beneficiario_blanco = True






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
                'active_ids': self.invoice_rel.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }





    def get_sum_aditional_invoices(self):
        total_facturas_adicionales = 0
        for l in self.facturas_adicionales:
            total_facturas_adicionales = total_facturas_adicionales + l.amount_residual_signed
        print(total_facturas_adicionales)
        self.aditional_invoices_total = (total_facturas_adicionales * -1)

    def get_sum_budget(self):
        acumulador = 0
        for line in self:
            for line2 in line.fletes_provisionados:
                acumulador = acumulador + line2.importe_mas_retencion
            self.budget_total = acumulador

    def alert_beneficiario(self):
        for rec_beneficiario in self:
            rec_beneficiario.alerta_beneficiario = ''
            for beneficiario in rec_beneficiario.fletes_provisionados:
                if beneficiario.beneficiario_pdf == '':
                    rec_beneficiario.alerta_beneficiario = '****NO EXISTE BENEFICIARIO EN ALGUN REGISTRO****'
                    rec_beneficiario.beneficiario_blanco = True
                else:
                    rec_beneficiario.alerta_beneficiario = ''



    def budget_validate_flete(self):
        for rec_presupuesto_validate in self:
            beneficiario_blanco = False
            rec_presupuesto_validate.state = 'validate'
            suma_resico = 0.0
            for beneficiario in rec_presupuesto_validate.fletes_provisionados:
                if beneficiario.beneficiario_pdf == '':
                    rec_presupuesto_validate.state = 'draft'



    @api.model
    def create(self,variables):
        if variables['beneficiario_blanco'] is False:
            if 'fletes_provicionados' in variables:
                for rec1 in variables['fletes_provisionados']:
                    acum_name = ''
                    for rec2 in rec1[2]:
                        query_name = f"""
                                        select name
                                        from fletes_modelo_tts
                                        where id = {rec2}
                                      """
                        self._cr.execute(query_name)
                        name_id = self._cr.fetchall()
                        print(name_id, 'query')
                        acum_name2 = name_id[0]
                        print(acum_name2, 'acum2')

                        print(acum_name2, 'acum')
                        acum_name = acum_name + ' ' + "'" + acum_name2[0] + "'"
                    variables['fletes_provisionados_db'] = acum_name

            return super(PresupuestoFlete, self).create(variables)
        else:
            raise UserError('NO EXISTE BENEFICICIARION EN ALGUN REGISTRO')

    def unlink(self):
        for rec in self:
            print(rec.fletes_provisionados)
            for rec_unlink in rec.fletes_provisionados:
                rel_fletes = self.env['fletes_modelo_tts'].search([('id', '=', rec_unlink.id)])
                for rec_fletes in rel_fletes:
                    rec_fletes.bloqueo_seleccion_presupuesto = False
        super(PresupuestoFlete, self).unlink()

    def write(self, variables):
        if 'fletes_provicionados' in variables:
            for rec2 in variables['fletes_provisionados']:
                print(rec2[2], 'ids')
                name_sum = ''
                for l in rec2[2]:
                    query_name = f"""
                                                               select name
                                                               from fletes_modelo_tts
                                                               where id = {l}
                                                             """
                    self._cr.execute(query_name)
                    name_id = self._cr.fetchall()
                    cadena = name_id[0]
                    name_sum = name_sum + " " + str(cadena)
                    name_sum = name_sum.replace('(', '')
                    name_sum = name_sum.replace(')', '')
                print('name', name_id)
                print('suma,cadena', name_sum)
            variables['fletes_provisionados_db'] = name_sum
        return super(PresupuestoFlete, self).write(variables)




    def budget_draft_flete(self):
        for rec_presupuesto_draft in self:
            rec_presupuesto_draft.state = 'draft'
            '''for rec in rec_presupuesto_draft.fletes_provisionados:
                rec.importe_mas_retencion = rec.importe_mas_retencion2'''






