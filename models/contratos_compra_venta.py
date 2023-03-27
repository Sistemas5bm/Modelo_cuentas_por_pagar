# -*- coding:utf-8 -*-

import logging
from odoo import fields, models, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class ContratosCompraVenta(models.Model):
    _name = "contratos_compra_venta"

    name = fields.Many2one(
        comodel_name='tipo_contrato',
        string="Tipo de contrato"
    )

    # dsc_name = fields.Char(string='Descripcion name')

    active = fields.Boolean(string='Activo', default=True)

    proveedor = fields.Many2one(
        comodel_name='res.partner',
        string='Proveedor'
    )

    fecha_contrato = fields.Date(string='Fecha Contrato')

    estado = fields.Many2one(

        comodel_name='estado',
        string='Estado'
    )

    ciudad = fields.Many2one(

        comodel_name='ciudad',
        string='Ciudad'
    )

    localidad = fields.Many2one(

        comodel_name='localidad',
        string='Localidad'

    )

    huertas = fields.Many2many(

        comodel_name='huertas',
        string='Huertas'

    )

    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado'),

    ], default='borrador', string='Estados', copy=False)

    factura = fields.Many2many(

        comodel_name='account.move',
        string='Factura'

    )

    fecha_aprobacion = fields.Datetime(string='Fecha Aprobado', copy=False)
    num_contrato = fields.Char(string='Numero de contrato',copy = False)

    def aprobar_contrato(self):
        self.state = 'aprobado'
        self.fecha_aprobacion = fields.Datetime.now()

    def cancelar_contrato(self):
        self.state = 'cancelado'

    def unlink(self):
        logger.info('Se disparo la funcion unlink')
        for record in self:
         if record.state == 'cancelado':
            super(ContratosCompraVenta, record).unlink()
         else:
            raise UserError('No se puede eliminar el registro por que no se encuentra en el estado cancelado')

    @api.model
    def create(self, variables):
        logger.info('variables : {0}'.format(variables))
        sequence_obj=self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.contrato')
        variables['num_contrato'] = correlativo
        return super(ContratosCompraVenta, self).create(variables)

    # la funcion write es despues de la funcion create es como un segundo registro
    def write(self, variables):
        logger.info('write variables : {0}'.format(variables))
        # Lee si la fecha contrato ya ha sido creada y no permite modificarla despues de haberla creado
        if 'fecha_contrato' in variables:
            # se manda un error
            raise UserError('La fecha del contrato no se puede editar')
        # se graba el diccionario en la bd
        return super(ContratosCompraVenta, self).write(variables)

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        return super(ContratosCompraVenta, self).copy(default)

# @api.onchange('name')

#    def _onchange_name(self):

#       if self.name:
#          if self.name ==
