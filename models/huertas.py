# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Huertas(models.Model):
    _name = "huertas"
    #heredo libreria imagen
    _inherit = ['image.mixin']

    name = fields.Char(string='Huerta')
    #boton para archivar
    active = fields.Boolean(string='Activo', default=True)

    sader = fields.Char(string='Sader')

    fda = fields.Char(string='Registro FDA')

    productor = fields.Many2one(comodel_name='res.partner',
                                string='Productor')
    ubicacion = fields.Char(string='Ubicación')

    estado = fields.Many2one(

        comodel_name='estado',
        string='Estado'
    )

    ciudad = fields.Many2one(

        comodel_name='ciudad', string='Ciudad'

    )

    localidad = fields.Many2one(

        comodel_name='localidad',
        string='Localidad'
    )

    producto = fields.Char(string='Producto')

    encargado_huerta = fields.Many2one(comodel_name='res.partner',
                                       string='Encargado Huerta')

    observaciones = fields.Char(string="Observaciones")

    #busca productor por medio de la categoria y solo obtiene lo productores
    categoria_productor_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Productor',
        # segunda version
        default=lambda self: self.env.ref('cuentas_por_pagar.category_productor')
        # primera version
        #  default=lambda self: self.env['res.partner.category'].search([('name','=','Productor')])
    )

    #se obtiene fecha de la creacion
    fecha_creacion = fields.Datetime(string="Fecha creacion", copy=False, default=lambda self: fields.Datetime.now())
    #se agrega un many2many con el modelo de las certificaciones
    registros_certificaciones = fields.One2many('certificaciones_registros','registro_certificaciones_huertas_rel',string="Registro de certificaciones")
    #variable que valida con un boolean si hay tarjeta apeam o no
    es_tarjeta_apeam = fields.Boolean(string='Tarjeta APEAM')
    #variable que almacena la tarjeta apeam en un binario
    tarjeta_apeam = fields.Binary(string='Archivo Tarjeta APEAM')
    # variable que guarda el nombre del binario
    tarjeta_apeam_filename = fields.Char(string='Nombre del archivo')
    #variable que habilita el campo de contrato de terceros
    es_contrato_terceros = fields.Boolean(string='Contrato terceros')
    #many2many que despliega el form de contrato para terceros
    contrato_terceros_lista = fields.One2many('huertas_contratos_terceros','huertas_contratos_terceros_huertas_rel',string='Contratos')



