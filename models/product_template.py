# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_infra_resource = fields.Boolean(
        'Recurso LTD Infra', default=False,
        help='Marca productos provenientes del B-3 Precios Elementales.')
    infra_resource_type = fields.Selection([
        ('material', 'Material'),
        ('labor', 'Mano de Obra'),
        ('equipment', 'Equipo / Maquinaria'),
    ], string='Tipo Recurso Infra', tracking=True)
    infra_resource_code = fields.Char(
        'Código B-3', tracking=True,
        help='Código interno del recurso en el formulario B-3.')

    price_base_oruro = fields.Float(
        'Precio Base Oruro (Bs)', digits=(12, 2), tracking=True,
        help='Precio unitario elemental — base Oruro-Challapata.')
    adjustment_factor = fields.Float(
        'Factor Ajuste', digits=(6, 3), default=1.0, tracking=True,
        help='Factor de ajuste Oruro→Uyuni (ej. 1.40 = +40%).')
    price_uyuni = fields.Float(
        'Precio Uyuni (Bs)', digits=(12, 2),
        compute='_compute_price_uyuni', store=True,
        help='Precio ajustado = Base × Factor.')
    variation_pct = fields.Float(
        'Variación (%)', digits=(6, 2),
        compute='_compute_price_uyuni', store=True)
    infra_justification = fields.Text(
        'Justificación Ajuste',
        help='Razón del factor de ajuste (transporte, diesel, etc.).')

    @api.depends('price_base_oruro', 'adjustment_factor')
    def _compute_price_uyuni(self):
        for rec in self:
            rec.price_uyuni = rec.price_base_oruro * rec.adjustment_factor
            rec.variation_pct = (rec.adjustment_factor - 1.0) * 100.0 if rec.adjustment_factor else 0.0
