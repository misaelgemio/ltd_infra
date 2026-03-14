# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraGastoGeneral(models.Model):
    """B-6 — Análisis de Gastos Generales (línea de detalle)."""
    _name = 'infra.gasto.general'
    _description = 'Gasto General (B-6)'
    _order = 'proyecto_id, seccion, numero'

    proyecto_id = fields.Many2one(
        'infra.proyecto', 'Proyecto', required=True, ondelete='cascade')
    seccion = fields.Selection([
        ('admin_central', 'A. Administración Central'),
        ('admin_campo', 'B. Administración de Campo'),
    ], string='Sección', required=True)
    numero = fields.Integer('N°', required=True)
    name = fields.Char('Descripción', required=True)
    unidad = fields.Char('Unidad', default='MES')
    cantidad = fields.Float('Cantidad', digits=(10, 2))
    precio_unitario = fields.Float('Precio Unit. (Bs)', digits=(12, 2))
    costo_mensual = fields.Float('Costo Mensual (Bs)', digits=(12, 2))
    costo_total = fields.Float(
        'Costo Total (Bs)', digits=(14, 2),
        compute='_compute_costo_total', store=True)

    @api.depends('cantidad', 'precio_unitario')
    def _compute_costo_total(self):
        for rec in self:
            rec.costo_total = rec.cantidad * rec.precio_unitario


class InfraCargaSocial(models.Model):
    """B-7 — Análisis de Cargas Sociales."""
    _name = 'infra.carga.social'
    _description = 'Carga Social (B-7)'
    _order = 'proyecto_id, seccion, numero'

    proyecto_id = fields.Many2one(
        'infra.proyecto', 'Proyecto', required=True, ondelete='cascade')
    seccion = fields.Selection([
        ('aportes', 'A. Aportes Patronales'),
        ('beneficios', 'B. Beneficios Sociales'),
    ], string='Sección', required=True)
    numero = fields.Integer('N°', required=True)
    name = fields.Char('Concepto', required=True)
    porcentaje = fields.Float('Porcentaje (%)', digits=(6, 4))
    incidencia = fields.Float('Incidencia', digits=(6, 4))
    base_legal = fields.Char('Base Legal / Referencia')
