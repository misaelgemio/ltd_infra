# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraProyecto(models.Model):
    _name = 'infra.proyecto'
    _description = 'Proyecto de Obra'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Nombre del Proyecto', required=True, tracking=True)
    codigo = fields.Char('CUCE / Código', tracking=True)
    configuracion_id = fields.Many2one(
        'infra.configuracion', 'Configuración',
        tracking=True, help='Parámetros de licitación aplicables.')
    responsable_id = fields.Many2one(
        'res.users', 'Responsable', tracking=True,
        default=lambda self: self.env.user)

    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('activo', 'Activo'),
        ('adjudicado', 'Adjudicado'),
        ('en_ejecucion', 'En Ejecución'),
        ('completado', 'Completado'),
    ], string='Estado', default='borrador', tracking=True)

    fecha_inicio = fields.Date('Fecha Inicio')
    plazo_meses = fields.Integer('Plazo (meses)', default=36, tracking=True)
    currency_id = fields.Many2one(
        'res.currency', 'Moneda',
        default=lambda self: self.env.ref('base.BOB', raise_if_not_found=False))
    note = fields.Html('Notas')

    tramo_ids = fields.One2many('infra.tramo', 'proyecto_id', 'Tramos')
    cronograma_ejecucion_ids = fields.One2many(
        'infra.cronograma.ejecucion', 'proyecto_id', 'Cronograma Ejecución (B-4)')
    movilizacion_equipo_ids = fields.One2many(
        'infra.movilizacion.equipo', 'proyecto_id', 'Movilización Equipo (B-5)')
    gasto_general_ids = fields.One2many(
        'infra.gasto.general', 'proyecto_id', 'Gastos Generales (B-6)')
    carga_social_ids = fields.One2many(
        'infra.carga.social', 'proyecto_id', 'Cargas Sociales (B-7)')
    cronograma_financiero_ids = fields.One2many(
        'infra.cronograma.financiero', 'proyecto_id', 'Cronograma Financiero (B-8)')
    desembolso_ids = fields.One2many(
        'infra.desembolso', 'proyecto_id', 'Desembolsos (B-9)')
    tramo_count = fields.Integer(compute='_compute_counts', store=True)
    item_count = fields.Integer(compute='_compute_counts', store=True)

    presupuesto_total = fields.Float(
        'Presupuesto Total (Bs)', digits=(14, 2),
        compute='_compute_presupuesto', store=True)

    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)',
         'El código CUCE del proyecto debe ser único.'),
    ]

    @api.depends('tramo_ids', 'tramo_ids.subtotal')
    def _compute_presupuesto(self):
        for rec in self:
            rec.presupuesto_total = sum(rec.tramo_ids.mapped('subtotal'))

    @api.depends('tramo_ids', 'tramo_ids.item_ids')
    def _compute_counts(self):
        for rec in self:
            rec.tramo_count = len(rec.tramo_ids)
            rec.item_count = sum(len(t.item_ids) for t in rec.tramo_ids)

    def action_activar(self):
        self.write({'state': 'activo'})

    def action_adjudicar(self):
        self.write({'state': 'adjudicado'})

    def action_ejecutar(self):
        self.write({'state': 'en_ejecucion'})

    def action_completar(self):
        self.write({'state': 'completado'})

    def action_borrador(self):
        self.write({'state': 'borrador'})

    def action_view_tramos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tramos',
            'res_model': 'infra.tramo',
            'view_mode': 'list,form',
            'domain': [('proyecto_id', '=', self.id)],
            'context': {'default_proyecto_id': self.id},
        }

    def action_view_items(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ítems de Obra',
            'res_model': 'infra.item.obra',
            'view_mode': 'list,form',
            'domain': [('proyecto_id', '=', self.id)],
        }
