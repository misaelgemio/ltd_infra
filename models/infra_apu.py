# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraApu(models.Model):
    _name = 'infra.apu'
    _description = 'Análisis de Precio Unitario (APU)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'numero'

    numero = fields.Integer('APU N°', required=True, tracking=True)
    name = fields.Char('Actividad', required=True, tracking=True)
    unidad = fields.Char('Unidad', tracking=True,
                         help='HA, M3, ML, M2, KG, TON, etc.')
    cantidad_referencia = fields.Float(
        'Cantidad Referencia', digits=(12, 2),
        help='Volumen de obra de referencia (desde B-1).')

    configuracion_id = fields.Many2one(
        'infra.configuracion', 'Configuración', tracking=True)
    proyecto_id = fields.Many2one('project.project', 'Proyecto')

    # --- Líneas de detalle ---
    material_ids = fields.One2many(
        'infra.apu.linea', 'apu_id', 'Materiales',
        domain=[('seccion', '=', 'material')])
    mano_obra_ids = fields.One2many(
        'infra.apu.linea', 'apu_id', 'Mano de Obra',
        domain=[('seccion', '=', 'mano_obra')])
    equipo_ids = fields.One2many(
        'infra.apu.linea', 'apu_id', 'Equipo y Maquinaria',
        domain=[('seccion', '=', 'equipo')])
    linea_ids = fields.One2many(
        'infra.apu.linea', 'apu_id', 'Todas las Líneas')

    # --- Subtotales por sección (computed) ---
    subtotal_materiales = fields.Float(
        'Total Materiales (1)', digits=(12, 2),
        compute='_compute_subtotales', store=True)
    subtotal_mo_directa = fields.Float(
        'Subtotal MO Directa', digits=(12, 2),
        compute='_compute_subtotales', store=True)
    subtotal_mo_indirecta = fields.Float(
        'MO Indirecta', digits=(12, 2),
        compute='_compute_subtotales', store=True)
    subtotal_cargas_sociales = fields.Float(
        'Cargas Sociales', digits=(12, 2),
        compute='_compute_subtotales', store=True)
    subtotal_iva_mo = fields.Float(
        'IVA Mano de Obra', digits=(12, 2),
        compute='_compute_subtotales', store=True)
    subtotal_mano_obra = fields.Float(
        'Total Mano de Obra (2)', digits=(12, 2),
        compute='_compute_subtotales', store=True)
    subtotal_equipo_directo = fields.Float(
        'Subtotal Equipo Directo', digits=(12, 2),
        compute='_compute_subtotales', store=True)
    subtotal_herramientas = fields.Float(
        'Herramientas', digits=(12, 2),
        compute='_compute_subtotales', store=True)
    subtotal_equipo = fields.Float(
        'Total Equipo, Maq. y Herramientas (3)', digits=(12, 2),
        compute='_compute_subtotales', store=True)

    # --- Gastos, utilidad, impuestos ---
    subtotal_gastos_generales = fields.Float(
        'Gastos Generales', digits=(12, 2),
        compute='_compute_indirectos', store=True)
    subtotal_gastos_financieros = fields.Float(
        'Gastos Financieros', digits=(12, 2),
        compute='_compute_indirectos', store=True)
    subtotal_gastos = fields.Float(
        'Total Gastos Generales (4)', digits=(12, 2),
        compute='_compute_indirectos', store=True)
    subtotal_utilidad = fields.Float(
        'Total Utilidad (5)', digits=(12, 2),
        compute='_compute_indirectos', store=True)
    subtotal_impuestos = fields.Float(
        'Total Impuestos IT (6)', digits=(12, 2),
        compute='_compute_indirectos', store=True)

    # --- Precio final ---
    precio_unitario_total = fields.Float(
        'Total Precio Unitario (1+2+3+4+5+6)', digits=(12, 6),
        compute='_compute_indirectos', store=True)
    precio_unitario_adoptado = fields.Float(
        'Precio Unitario Adoptado (Bs)', digits=(12, 2),
        compute='_compute_indirectos', store=True,
        help='Precio redondeado a 2 decimales. Se usa en B-1.')

    @api.depends(
        'linea_ids.costo_total', 'linea_ids.seccion',
        'configuracion_id.cargas_sociales_pct',
        'configuracion_id.mo_indirecta_pct',
        'configuracion_id.iva_mano_obra_pct',
        'configuracion_id.herramientas_pct',
    )
    def _compute_subtotales(self):
        for rec in self:
            cfg = rec.configuracion_id

            # (1) Materiales
            rec.subtotal_materiales = sum(
                l.costo_total for l in rec.linea_ids
                if l.seccion == 'material')

            # (2) Mano de Obra
            mo_directa = sum(
                l.costo_total for l in rec.linea_ids
                if l.seccion == 'mano_obra')
            rec.subtotal_mo_directa = mo_directa

            iva_pct = cfg.iva_mano_obra_pct if cfg else 0.1494
            mo_indirecta_pct = cfg.mo_indirecta_pct if cfg else 0.05
            cargas_pct = cfg.cargas_sociales_pct if cfg else 0.4681

            rec.subtotal_mo_indirecta = mo_directa * iva_pct
            rec.subtotal_cargas_sociales = (
                (mo_directa + rec.subtotal_mo_indirecta) * cargas_pct)
            rec.subtotal_iva_mo = mo_directa * mo_indirecta_pct
            rec.subtotal_mano_obra = (
                mo_directa + rec.subtotal_mo_indirecta
                + rec.subtotal_cargas_sociales + rec.subtotal_iva_mo)

            # (3) Equipo
            eq_directo = sum(
                l.costo_total for l in rec.linea_ids
                if l.seccion == 'equipo')
            rec.subtotal_equipo_directo = eq_directo

            herr_pct = cfg.herramientas_pct if cfg else 0.05
            rec.subtotal_herramientas = rec.subtotal_mano_obra * herr_pct
            rec.subtotal_equipo = eq_directo + rec.subtotal_herramientas

    @api.depends(
        'subtotal_materiales', 'subtotal_mano_obra', 'subtotal_equipo',
        'configuracion_id.gastos_generales_pct',
        'configuracion_id.gastos_financieros_pct',
        'configuracion_id.utilidad_pct',
        'configuracion_id.impuesto_it_pct',
    )
    def _compute_indirectos(self):
        for rec in self:
            cfg = rec.configuracion_id
            base_123 = (rec.subtotal_materiales
                        + rec.subtotal_mano_obra
                        + rec.subtotal_equipo)

            gg_pct = cfg.gastos_generales_pct if cfg else 0.10
            gf_pct = cfg.gastos_financieros_pct if cfg else 0.0
            ut_pct = cfg.utilidad_pct if cfg else 0.10
            it_pct = cfg.impuesto_it_pct if cfg else 0.0309

            # (4) Gastos Generales
            rec.subtotal_gastos_generales = base_123 * gg_pct
            rec.subtotal_gastos_financieros = base_123 * gf_pct
            rec.subtotal_gastos = (
                rec.subtotal_gastos_generales
                + rec.subtotal_gastos_financieros)

            # (5) Utilidad
            rec.subtotal_utilidad = (base_123 + rec.subtotal_gastos) * ut_pct

            # (6) Impuestos IT
            acumulado_12345 = (
                base_123 + rec.subtotal_gastos + rec.subtotal_utilidad)
            rec.subtotal_impuestos = acumulado_12345 * it_pct

            # Total y adoptado
            rec.precio_unitario_total = acumulado_12345 + rec.subtotal_impuestos
            rec.precio_unitario_adoptado = round(
                rec.precio_unitario_total, 2)
