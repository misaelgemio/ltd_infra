# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraApuLinea(models.Model):
    _name = 'infra.apu.linea'
    _description = 'Línea de APU (recurso)'
    _order = 'apu_id, seccion, sequence'

    apu_id = fields.Many2one(
        'infra.apu', 'APU', required=True, ondelete='cascade')
    sequence = fields.Integer('Secuencia', default=10)

    seccion = fields.Selection([
        ('material', '1. Materiales'),
        ('mano_obra', '2. Mano de Obra'),
        ('equipo', '3. Equipo / Maquinaria'),
    ], string='Sección', required=True)

    product_id = fields.Many2one(
        'product.template', 'Recurso (B-3)',
        domain="[('is_infra_resource', '=', True)]",
        help='Producto del catálogo B-3.')
    name = fields.Char('Descripción', required=True)
    unidad = fields.Char('Unidad')
    cantidad = fields.Float('Cantidad', digits=(10, 4))
    precio_unitario = fields.Float(
        'Precio Unit. (Bs)', digits=(12, 2),
        help='Precio desde B-3 Uyuni.')
    productividad = fields.Float(
        'Productividad', digits=(6, 3), default=1.0,
        help='Factor de productividad (1.0 = normal).')
    costo_total = fields.Float(
        'Costo Total (Bs)', digits=(12, 2),
        compute='_compute_costo', store=True)

    @api.depends('cantidad', 'precio_unitario', 'productividad')
    def _compute_costo(self):
        for rec in self:
            prod = rec.productividad if rec.productividad else 1.0
            rec.costo_total = rec.cantidad * rec.precio_unitario * prod

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.name = self.product_id.name
            self.precio_unitario = self.product_id.price_uyuni
            self.unidad = self.product_id.uom_id.name if self.product_id.uom_id else ''
            if self.product_id.infra_resource_type == 'material':
                self.seccion = 'material'
            elif self.product_id.infra_resource_type == 'labor':
                self.seccion = 'mano_obra'
            elif self.product_id.infra_resource_type == 'equipment':
                self.seccion = 'equipo'
