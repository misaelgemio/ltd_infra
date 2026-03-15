# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectProject(models.Model):
    """Hereda project.project para vincular datos de licitación B-1 a B-9."""
    _inherit = 'project.project'

    is_infra_project = fields.Boolean('Proyecto de Infraestructura')
    configuracion_id = fields.Many2one(
        'infra.configuracion', 'Configuración Infra',
        help='Parámetros de licitación (B-6, B-7).')
    codigo_cuce = fields.Char('CUCE / Código Licitación')
    plazo_meses = fields.Integer('Plazo (meses)', default=36)

    presupuesto_total = fields.Float(
        'Presupuesto Total (Bs)', digits=(14, 2),
        compute='_compute_presupuesto_infra', store=True)

    # --- Tramos ---
    tramo_ids = fields.One2many(
        'infra.tramo', 'project_id', 'Tramos')

    # --- One2many a datos B-4 a B-9 ---
    cronograma_ejecucion_ids = fields.One2many(
        'infra.cronograma.ejecucion', 'proyecto_id',
        'Cronograma Ejecución (B-4)')
    movilizacion_equipo_ids = fields.One2many(
        'infra.movilizacion.equipo', 'proyecto_id',
        'Movilización Equipo (B-5)')
    gasto_general_ids = fields.One2many(
        'infra.gasto.general', 'proyecto_id',
        'Gastos Generales (B-6)')
    carga_social_ids = fields.One2many(
        'infra.carga.social', 'proyecto_id',
        'Cargas Sociales (B-7)')
    cronograma_financiero_ids = fields.One2many(
        'infra.cronograma.financiero', 'proyecto_id',
        'Cronograma Financiero (B-8)')
    desembolso_ids = fields.One2many(
        'infra.desembolso', 'proyecto_id',
        'Desembolsos (B-9)')

    # --- Contadores ---
    tramo_count = fields.Integer(
        compute='_compute_infra_counts', store=True)
    item_count = fields.Integer(
        compute='_compute_infra_counts', store=True)
    apu_count = fields.Integer(
        compute='_compute_apu_count')

    @api.depends('tramo_ids', 'tramo_ids.subtotal')
    def _compute_presupuesto_infra(self):
        for rec in self:
            if rec.is_infra_project:
                rec.presupuesto_total = sum(
                    rec.tramo_ids.mapped('subtotal'))
            else:
                rec.presupuesto_total = 0

    @api.depends('tramo_ids', 'tramo_ids.item_ids')
    def _compute_infra_counts(self):
        for rec in self:
            rec.tramo_count = len(rec.tramo_ids)
            rec.item_count = sum(len(t.item_ids) for t in rec.tramo_ids)

    def _compute_apu_count(self):
        for rec in self:
            rec.apu_count = self.env['infra.apu'].search_count(
                [('proyecto_id', '=', rec.id)])

    # --- Smart buttons ---
    def action_view_infra_apu(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'APU (B-2)',
            'res_model': 'infra.apu',
            'view_mode': 'list,form',
            'domain': [('proyecto_id', '=', self.id)],
            'context': {'default_proyecto_id': self.id},
        }

    def action_view_tramos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tramos',
            'res_model': 'infra.tramo',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_items(self):
        self.ensure_one()
        tramo_ids = self.tramo_ids.ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ítems de Obra',
            'res_model': 'infra.item.obra',
            'view_mode': 'list,form',
            'domain': [('tramo_id', 'in', tramo_ids)],
        }


class ProjectTask(models.Model):
    """Hereda project.task para usarlo como ítem de obra (B-1)."""
    _inherit = 'project.task'

    is_infra_task = fields.Boolean(
        related='project_id.is_infra_project', store=True)

    # Campos B-1
    numero_item = fields.Integer('N° Ítem')
    unidad = fields.Char('Unidad',
                         help='HA, M3, ML, M2, KG, TON, PZA, GLB, etc.')
    cantidad = fields.Float('Cantidad', digits=(12, 2))
    precio_unitario = fields.Float(
        'Precio Unitario (Bs)', digits=(12, 2),
        compute='_compute_precio_unitario', store=True, readonly=False)
    total = fields.Float(
        'Precio Total (Bs)', digits=(14, 2),
        compute='_compute_total_item', store=True)

    # Vinculación con APU
    apu_id = fields.Many2one('infra.apu', 'APU (B-2)')

    # Módulo / agrupador
    modulo_obra = fields.Char('Módulo de Obra',
                              help='Ej: MOVIMIENTO DE TIERRAS, PAVIMENTACIÓN')
    tramo_id = fields.Many2one('infra.tramo', 'Tramo')

    @api.depends('apu_id.precio_unitario_adoptado')
    def _compute_precio_unitario(self):
        for rec in self:
            if rec.apu_id:
                rec.precio_unitario = rec.apu_id.precio_unitario_adoptado

    @api.depends('cantidad', 'precio_unitario')
    def _compute_total_item(self):
        for rec in self:
            rec.total = rec.cantidad * rec.precio_unitario
