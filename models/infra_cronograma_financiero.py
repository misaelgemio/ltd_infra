# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraCronogramaFinanciero(models.Model):
    """B-8 — Cronograma Financiero (curva S por mes)."""
    _name = 'infra.cronograma.financiero'
    _description = 'Cronograma Financiero (B-8)'
    _order = 'proyecto_id, mes'

    proyecto_id = fields.Many2one(
        'infra.proyecto', 'Proyecto', required=True, ondelete='cascade')
    mes = fields.Integer('Mes', required=True)
    inversion_pct = fields.Float(
        'Inversión Mensual (%)', digits=(8, 6))
    inversion_bs = fields.Float(
        'Inversión Mensual (Bs)', digits=(14, 2))
    acumulado_pct = fields.Float(
        'Acumulado (%)', digits=(8, 6))
    acumulado_bs = fields.Float(
        'Acumulado (Bs)', digits=(14, 2))


class InfraDesembolso(models.Model):
    """B-9 — Cronograma de Desembolsos (línea por concepto × mes)."""
    _name = 'infra.desembolso'
    _description = 'Desembolso (B-9)'
    _order = 'proyecto_id, sequence'

    proyecto_id = fields.Many2one(
        'infra.proyecto', 'Proyecto', required=True, ondelete='cascade')
    sequence = fields.Integer('Secuencia', default=10)
    name = fields.Char('Concepto', required=True)
    total_bs = fields.Float('Total (Bs)', digits=(14, 2))
    # Valores mensuales
    m1 = fields.Float('M1', digits=(14, 2))
    m2 = fields.Float('M2', digits=(14, 2))
    m3 = fields.Float('M3', digits=(14, 2))
    m4 = fields.Float('M4', digits=(14, 2))
    m5 = fields.Float('M5', digits=(14, 2))
    m6 = fields.Float('M6', digits=(14, 2))
    m7 = fields.Float('M7', digits=(14, 2))
    m8 = fields.Float('M8', digits=(14, 2))
    m9 = fields.Float('M9', digits=(14, 2))
    m10 = fields.Float('M10', digits=(14, 2))
    m11 = fields.Float('M11', digits=(14, 2))
    m12 = fields.Float('M12', digits=(14, 2))
    m13 = fields.Float('M13', digits=(14, 2))
    m14 = fields.Float('M14', digits=(14, 2))
    m15 = fields.Float('M15', digits=(14, 2))
    m16 = fields.Float('M16', digits=(14, 2))
    m17 = fields.Float('M17', digits=(14, 2))
    m18 = fields.Float('M18', digits=(14, 2))
    m19 = fields.Float('M19', digits=(14, 2))
    m20 = fields.Float('M20', digits=(14, 2))
    m21 = fields.Float('M21', digits=(14, 2))
    m22 = fields.Float('M22', digits=(14, 2))
    m23 = fields.Float('M23', digits=(14, 2))
    m24 = fields.Float('M24', digits=(14, 2))
    m25 = fields.Float('M25', digits=(14, 2))
    m26 = fields.Float('M26', digits=(14, 2))
    m27 = fields.Float('M27', digits=(14, 2))
    m28 = fields.Float('M28', digits=(14, 2))
    m29 = fields.Float('M29', digits=(14, 2))
    m30 = fields.Float('M30', digits=(14, 2))
    m31 = fields.Float('M31', digits=(14, 2))
    m32 = fields.Float('M32', digits=(14, 2))
    m33 = fields.Float('M33', digits=(14, 2))
    m34 = fields.Float('M34', digits=(14, 2))
    m35 = fields.Float('M35', digits=(14, 2))
    m36 = fields.Float('M36', digits=(14, 2))
