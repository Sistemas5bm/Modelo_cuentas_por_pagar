# -*- coding:utf-8 -*-

from odoo import fields, models, api


class CortesCuadrillasAjusteWizard(models.TransientModel):

    _name = "cuadrillas_kilogramos"

    cantidad = fields.Float(string="Cantidad")

    def update_qty(self):
        for linea in self:
            linea.env['cortes'].browse(linea._context.get("active_ids")).update({'kilogramos_ajuste':linea.cantidad})
            kilogramos_productor = linea.env['cortes'].browse(linea._context.get("active_ids")).peso_productor
            id_corte = linea.env['cortes'].browse(linea._context.get("active_ids")).id
            id_cuadrilla_normal = self.env['tipo_cuadrillas'].search([('name', '=', 'CUADRILLA NORMAL')], limit=1)
            id_ajuste = self.env['tipo_cuadrillas'].search([('name', '=', 'AJUSTE')], limit=1)
            cuadrilla_normal_search = self.env['cuadrillas'].search([('cuadrilla_rel', '=', id_corte), ('name', '=', id_cuadrilla_normal.id)], limit=1)
            cuadrilla_browse = self.env['cuadrillas'].browse([cuadrilla_normal_search.id])
            importe_cuadrilla = cuadrilla_normal_search.importe
            print(kilogramos_productor)
            print(cuadrilla_normal_search.id)
            kilogramos_ajuste = linea.env['cortes'].browse(linea._context.get("active_ids")).kilogramos_ajuste
            kilogramos_ajuste_final = kilogramos_ajuste
            print(id_ajuste.id)
            recordObjectAjuste = {'name':id_ajuste.id,
                                  'cuadrilla_rel':id_corte,
                                  'importe':((importe_cuadrilla/kilogramos_productor)*(kilogramos_ajuste_final)) * (-1),}
            #cuadrilla_browse.write({'importe': (importe_cuadrilla)-((importe_cuadrilla/kilogramos_productor)*(kilogramos_ajuste_final))})
            insert_cuadrilla_normal = self.env['cuadrillas'].create(recordObjectAjuste)
            return True
