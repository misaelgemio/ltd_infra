# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InfraCronogramaEjecucion(models.Model):
    """B-4 — Cronograma de Ejecución de Obra (línea por actividad)."""
    _name = 'infra.cronograma.ejecucion'
    _description = 'Cronograma de Ejecución (B-4)'
    _order = 'proyecto_id, numero'

    proyecto_id = fields.Many2one(
        'infra.proyecto', 'Proyecto', required=True, ondelete='cascade')
    item_obra_id = fields.Many2one(
        'infra.item.obra', 'Ítem de Obra',
        help='Vinculación con ítem B-1.')
    numero = fields.Integer('Ítem N°', required=True)
    name = fields.Char('Descripción', required=True)
    modulo_nombre = fields.Char(
        'Módulo', help='Nombre del módulo/grupo (ej. MOVIMIENTO DE TIERRAS)')
    duracion_meses = fields.Integer('Duración (meses)', required=True)
    mes_inicio = fields.Integer('Mes Inicio', default=1)
    mes_fin = fields.Integer(
        'Mes Fin', compute='_compute_mes_fin', store=True)

    # Barras por mes (36 meses = campos booleanos)
    m1 = fields.Boolean('M1')
    m2 = fields.Boolean('M2')
    m3 = fields.Boolean('M3')
    m4 = fields.Boolean('M4')
    m5 = fields.Boolean('M5')
    m6 = fields.Boolean('M6')
    m7 = fields.Boolean('M7')
    m8 = fields.Boolean('M8')
    m9 = fields.Boolean('M9')
    m10 = fields.Boolean('M10')
    m11 = fields.Boolean('M11')
    m12 = fields.Boolean('M12')
    m13 = fields.Boolean('M13')
    m14 = fields.Boolean('M14')
    m15 = fields.Boolean('M15')
    m16 = fields.Boolean('M16')
    m17 = fields.Boolean('M17')
    m18 = fields.Boolean('M18')
    m19 = fields.Boolean('M19')
    m20 = fields.Boolean('M20')
    m21 = fields.Boolean('M21')
    m22 = fields.Boolean('M22')
    m23 = fields.Boolean('M23')
    m24 = fields.Boolean('M24')
    m25 = fields.Boolean('M25')
    m26 = fields.Boolean('M26')
    m27 = fields.Boolean('M27')
    m28 = fields.Boolean('M28')
    m29 = fields.Boolean('M29')
    m30 = fields.Boolean('M30')
    m31 = fields.Boolean('M31')
    m32 = fields.Boolean('M32')
    m33 = fields.Boolean('M33')
    m34 = fields.Boolean('M34')
    m35 = fields.Boolean('M35')
    m36 = fields.Boolean('M36')

    @api.depends('mes_inicio', 'duracion_meses')
    def _compute_mes_fin(self):
        for rec in self:
            rec.mes_fin = rec.mes_inicio + rec.duracion_meses - 1


class InfraMovilizacionEquipo(models.Model):
    """B-5 — Cronograma de Movilización de Equipo."""
    _name = 'infra.movilizacion.equipo'
    _description = 'Movilización de Equipo (B-5)'
    _order = 'proyecto_id, numero'

    proyecto_id = fields.Many2one(
        'infra.proyecto', 'Proyecto', required=True, ondelete='cascade')
    numero = fields.Integer('N°', required=True)
    name = fields.Char('Equipo / Maquinaria', required=True)
    product_id = fields.Many2one(
        'product.template', 'Recurso B-3',
        domain="[('is_infra_resource', '=', True),"
               " ('infra_resource_type', '=', 'equipment')]")
    cantidad = fields.Integer('Cantidad', required=True)
    mes_llegada = fields.Integer('Mes Llegada', required=True)
    meses_en_obra = fields.Integer('Meses en Obra')
    mes_desmovilizacion = fields.Integer(
        'Mes Desmovilización',
        compute='_compute_desmovilizacion', store=True)

    @api.depends('mes_llegada', 'meses_en_obra')
    def _compute_desmovilizacion(self):
        for rec in self:
            if rec.meses_en_obra:
                rec.mes_desmovilizacion = rec.mes_llegada + rec.meses_en_obra
            else:
                rec.mes_desmovilizacion = 0
