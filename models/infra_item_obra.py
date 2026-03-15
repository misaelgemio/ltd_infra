# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraItemObra(models.Model):
    _name = 'infra.item.obra'
    _description = 'Ítem de Presupuesto (B-1)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'tramo_id, modulo_id, numero'

    numero = fields.Integer('N° Ítem', tracking=True)
    name = fields.Char('Descripción del Trabajo', required=True, tracking=True)
    unidad = fields.Char('Unidad', tracking=True,
                         help='HA, M3, ML, M2, M3-KM, KG, TON, PZA, etc.')

    tramo_id = fields.Many2one(
        'infra.tramo', 'Tramo', required=True,
        ondelete='cascade')
    modulo_id = fields.Many2one(
        'infra.modulo.obra', 'Módulo',
        domain="[('tramo_id', '=', tramo_id)]",
        tracking=True)
    project_id = fields.Many2one(
        'project.project', related='tramo_id.project_id',
        string='Proyecto', store=True)

    apu_id = fields.Many2one(
        'infra.apu', 'APU',
        tracking=True,
        help='Análisis de Precio Unitario vinculado.')

    cantidad = fields.Float(
        'Cantidad', digits=(12, 2), tracking=True,
        help='Volumen de obra del ítem.')
    precio_unitario = fields.Float(
        'Precio Unitario (Bs)', digits=(12, 2),
        compute='_compute_precio_unitario', store=True, readonly=False,
        tracking=True,
        help='Precio desde APU adoptado, o ingreso manual.')
    total = fields.Float(
        'Precio Total (Bs)', digits=(14, 2),
        compute='_compute_total', store=True)

    @api.depends('apu_id.precio_unitario_adoptado')
    def _compute_precio_unitario(self):
        for rec in self:
            if rec.apu_id:
                rec.precio_unitario = rec.apu_id.precio_unitario_adoptado

    @api.depends('cantidad', 'precio_unitario')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.cantidad * rec.precio_unitario
