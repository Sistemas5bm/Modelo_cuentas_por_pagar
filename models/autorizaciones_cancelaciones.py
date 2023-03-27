# -*- coding:utf-8 -*-
import base64
from odoo import fields, models, api
import logging
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
logger = logging.getLogger(__name__)

class AutorizacionesCancelaciones(models.Model):

    _name = "autorizaciones_cancelaciones"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Many2one('res.users',string='Solicitante',default=lambda self: self.env.user,readonly=True,tracking=True,track_visibility='always',store=True)

    invoice = fields.Many2one('account.move',string='Factura a cancelar',
                              domain = [('move_type', '=', 'in_invoice'),('payment_state','!=','not_paid')]
                              ,context="{'tree_view_ref':'account.view_in_invoice_tree'}",tracking=True,track_visibility='always',store=True)

    cancel_motive = fields.Selection(selection=[
        ('bad_invoice', 'Factura erronea'),
        ('invoice_dateless', 'Factura fuera de tiempo'),
        ('other','Otros')], default='bad_invoice', string='Motivo de cancelación', copy=False,tracking=True,track_visibility='always',store=True)

    motive = fields.Text(string='Motivo de cancelacion',tracking=True,track_visibility='always',store=True)

    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado')

    ], default='borrador', string='Estados', copy=False,tracking=True,track_visibility='always',store=True)



    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    type_user_cxp = fields.Selection(selection=([('solicitante', 'Solicitante'),
                                                 ('autorizador', 'Autorizador')]))
    type_user_char = fields.Char(string='User', compute='comute_tes')
    compute_permisos = fields.Boolean(string='Compute de permisos', compute='comute_tes' )


    def comute_tes(self):
        for l in self:
            l.type_user_char = self.env.user.id
            l.compute_permisos = True
            query_permisos_usuarios=f"""select ru .login,
                                        rp."name" ,
                                        ru .partner_id,
                                        pu.type_user ,
                                        pu .id ,
                                        ru.id 
                                        from permisos_usuarios pu 
                                        left join res_users ru on ru .id = pu ."name"  
                                        left join res_partner rp on rp .id  = ru .partner_id
                                        where ru.id = {l.type_user_char} 
                                     """
            self._cr.execute(query_permisos_usuarios)
            resul= self._cr.fetchall()
            print('query ',resul )
            for x in resul:
                l.type_user_cxp = x[3]


    @api.onchange("invoice")
    @api.model
    def hide_button(self):
        for l in self:
            l.type_user_char = self.env.user.id
            l.compute_permisos = True
            query_permisos_usuarios=f"""select ru .login,
                                        rp."name" ,
                                        ru .partner_id,
                                        pu.type_user ,
                                        pu .id ,
                                        ru.id 
                                        from permisos_usuarios pu 
                                        left join res_users ru on ru .id = pu ."name"  
                                        left join res_partner rp on rp .id  = ru .partner_id
                                        where ru.id = {l.type_user_char} 
                                     """
            self._cr.execute(query_permisos_usuarios)
            resul= self._cr.fetchall()
            print('query ',resul )
            for x in resul:
                l.type_user_cxp = x[3]

    def confirmar(self):
        self.state = 'aprobado'
        #self.env['account.move'].write()
        inv_search = self.env['account.move'].search([('id', '=', self.invoice.id)], limit=1)

        self._cr.execute('update account_move set lock_validate=%s where id=%s', (True, inv_search.id))
    def cancelar(self):
        self.state = 'cancelado'
        inv_search = self.env['account.move'].search([('id', '=', self.invoice.id)], limit=1)

        self._cr.execute('update account_move set lock_validate=%s where id=%s', (None, inv_search.id))

