# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class PlaneacionVentasOrdenes(models.Model):
    _name = 'planeacion.ordenes'
    _rec_name = "folio"
    _inherit = ['mail.thread']

    folio = fields.Char(string="Folio", default="Nuevo", track_visibility='onchange')
    cliente_id = fields.Many2one('res.partner', string="Cliente", track_visibility='onchange')
    fecha_pedido = fields.Datetime(string="Fecha de Pedido", default=fields.Date.today(), track_visibility='onchange')
    fecha_terminacion = fields.Datetime(string="Fecha de Terminacion", track_visibility='onchange')
    productos_ids = fields.Many2many('sale.order.line', string="Productos")
    estado = fields.Selection([('creado', 'Nuevo'),('proceso', 'En proceso'),('cancelado', 'Cancelado'),
                               ('finalizado', 'Finalizado')], default='creado', string="Estado", track_visibility='onchange')

    def finalizar(self):
    	for r in self:
    		r.estado = 'finalizado'
    		r.fecha_terminacion = datetime.datetime.now()

    def cancelar(self):
        for r in self:
            r.estado = 'cancelado'
            ventas = self.env['sale.order'].search([('planeacion_orden_id','=',r.id)])
            for venta in ventas:
                venta.planeacion_orden_id = False

    @api.model
    def create(self, vals):
    	if vals.get('folio','Nuevo') == 'Nuevo':
    		vals['folio'] = self.env['ir.sequence'].next_by_code('planeacion.ordenes') or "Nuevo"
    	return super(PlaneacionVentasOrdenes, self).create(vals)