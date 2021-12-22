# -*- coding: utf-8 -*-

from odoo import _, fields, models, api

#Pedidos de Venta
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    planeacion_orden_id = fields.Many2one('planeacion.ordenes', string="Orden de Planeacion")

    @api.multi
    def action_confirm(self):
        rec = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.planeacion_orden_id:
                order.planeacion_orden_id.estado = 'finalizado'            
        return rec

    @api.multi
    def action_cancel(self):
        rec = super(SaleOrder, self).action_cancel()
        for order in self:
            if order.planeacion_orden_id:
                order.planeacion_orden_id.estado = 'cancelado'
                order.planeacion_orden_id = False
        return rec

  
    def open_wizard_button(self, cr, uid, ids, context=None):
        return {
            'name': ('Assignment Sub'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ru.assignments.sub',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

#Envio de Ventas a Orden de Planeacion
class PlaneacionSaleOrder(models.TransientModel):
    _name = 'planeacion.sale.order'
    _description = "Envio de pedidos de venta a orden de planeacion"

    @api.model
    def default_get(self, default_fields):
        res = super(PlaneacionSaleOrder, self).default_get(default_fields)
        ventas_id = self._context.get('active_ids')
        ventas = self.env['sale.order'].browse(ventas_id)
        self.validate(ventas)
        return res

    @api.multi
    def crear_planeacion(self):
        ventas = self.env['sale.order'].browse(self._context.get('active_ids'))        
        orden = self.env['planeacion.ordenes'].create({
            'cliente_id': ventas[0].partner_id.id,
            'fecha_pedido': ventas[0].date_order,
            'estado': 'proceso'
        })
        for venta in ventas:
            #lineas_ventas = self.env['sale.order.line'].search([('order_id','=',venta.id)])
            message = _('<strong>Planeacion:</strong> %s </br>') % (', '.join(orden.mapped('folio')))
            venta.message_post(body=message)
            venta.planeacion_orden_id = orden.id
            for linea in venta.order_line:
                orden.write({'productos_ids':[(4, linea.id)]})

        return{
            'name': 'Planeacion',
            'view_id': self.env.ref('planeacion.planeacion_ordenes_form').id,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'planeacion.ordenes',
            'res_id': orden.id,
            'type': 'ir.actions.act_window'
        }

    @api.model
    def validate(self, reports):
        if len(reports.mapped('planeacion_orden_id')):
            raise ValidationError(
                 _('El pedido ya tiene asignado una Orden de Planeacion \n Cancelé la planeacion activa para generar una nueva'))
        if len(reports.mapped('partner_id')) > 1:
            raise ValidationError(
                _('Todos los pedidos deben de tener el mismo CLIENTE'))