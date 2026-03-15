# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraModuloObra(models.Model):
    _name = 'infra.modulo.obra'
    _description = 'Módulo de Obra'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'tramo_id, numero'

    name = fields.Char('Nombre del Módulo', required=True, tracking=True)
    numero = fields.Integer('N° Módulo', tracking=True)
    tramo_id = fields.Many2one(
        'infra.tramo', 'Tramo', required=True,
        ondelete='cascade')
    project_id = fields.Many2one(
        'project.project', related='tramo_id.project_id',
        string='Proyecto', store=True)

    item_ids = fields.One2many('infra.item.obra', 'modulo_id', 'Ítems')

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

    @api.depends('subtotal', 'tramo_id.subtotal')
    def _compute_incidencia(self):
        for rec in self:
            total = rec.tramo_id.subtotal
            rec.incidencia_pct = (
                (rec.subtotal / total * 100.0) if total else 0.0)
