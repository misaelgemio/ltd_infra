# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraConfiguracion(models.Model):
    _name = 'infra.configuracion'
    _description = 'Parámetros de Licitación'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre', required=True, tracking=True)
    active = fields.Boolean(default=True)

    # --- B-7 Cargas Sociales ---
    cargas_sociales_pct = fields.Float(
        'Cargas Sociales (% MO Directa)', digits=(6, 4),
        default=0.4681, tracking=True,
        help='Aportes patronales + beneficios sociales. B-7.')
    mo_indirecta_pct = fields.Float(
        'MO Indirecta (% MO Directa)', digits=(6, 4),
        default=0.05, tracking=True)
    iva_mano_obra_pct = fields.Float(
        'IVA Mano de Obra (%)', digits=(6, 4),
        default=0.1494, tracking=True)

    # --- B-6 / APU ---
    herramientas_pct = fields.Float(
        'Herramientas (% Total MO)', digits=(6, 4),
        default=0.05, tracking=True)
    gastos_generales_pct = fields.Float(
        'Gastos Generales (% MAT+MO+EQ)', digits=(6, 4),
        default=0.10, tracking=True,
        help='B-6: Administración central y campo.')
    gastos_financieros_pct = fields.Float(
        'Gastos Financieros (%)', digits=(6, 4),
        default=0.0, tracking=True)
    utilidad_pct = fields.Float(
        'Utilidad (% MAT+MO+EQ+GG)', digits=(6, 4),
        default=0.10, tracking=True)
    impuesto_it_pct = fields.Float(
        'Impuesto IT (%)', digits=(6, 4),
        default=0.0309, tracking=True,
        help='Impuesto a las Transacciones — Ley 843.')

    # --- Calibración presupuesto ---
    presupuesto_base_bs = fields.Float(
        'Presupuesto Base (Bs)', digits=(14, 2), tracking=True)
    incremento_objetivo_pct = fields.Float(
        'Incremento Objetivo (%)', digits=(6, 4),
        default=0.42, tracking=True)
    factor_calibracion = fields.Float(
        'Factor Calibración Global', digits=(8, 6),
        default=0.881638, tracking=True)

    presupuesto_objetivo = fields.Float(
        'Presupuesto Objetivo (Bs)', digits=(14, 2),
        compute='_compute_presupuesto_objetivo', store=True)

    currency_id = fields.Many2one(
        'res.currency', 'Moneda',
        default=lambda self: self.env.ref('base.BOB', raise_if_not_found=False))

    @api.depends('presupuesto_base_bs', 'incremento_objetivo_pct')
    def _compute_presupuesto_objetivo(self):
        for rec in self:
            rec.presupuesto_objetivo = (
                rec.presupuesto_base_bs * (1 + rec.incremento_objetivo_pct))
