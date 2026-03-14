# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraTramo(models.Model):
    _name = 'infra.tramo'
    _description = 'Tramo de Proyecto'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'proyecto_id, sequence, name'

    name = fields.Char('Nombre del Tramo', required=True, tracking=True)
    sequence = fields.Integer('Secuencia', default=10)
    proyecto_id = fields.Many2one(
        'infra.proyecto', 'Proyecto', required=True,
        ondelete='cascade', tracking=True)
    configuracion_id = fields.Many2one(
        'infra.configuracion', related='proyecto_id.configuracion_id',
        string='Configuración', store=True)

    modulo_ids = fields.One2many('infra.modulo.obra', 'tramo_id', 'Módulos')
    item_ids = fields.One2many('infra.item.obra', 'tramo_id', 'Ítems')

    subtotal = fields.Float(
        'Subtotal (Bs)', digits=(14, 2),
        compute='_compute_subtotal', store=True)
    incidencia_pct = fields.Float(
        'Incidencia (%)', digits=(6, 2),
        compute='_compute_incidencia', store=True)

    @api.depends('item_ids.total')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = sum(rec.item_ids.mapped('total'))

    @api.depends('subtotal', 'proyecto_id.presupuesto_total')
    def _compute_incidencia(self):
        for rec in self:
            total = rec.proyecto_id.presupuesto_total
            rec.incidencia_pct = (
                (rec.subtotal / total * 100.0) if total else 0.0)
