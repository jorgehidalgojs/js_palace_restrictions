import logging

from odoo import models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _is_internal_picking_validation(self):
        ctx = self.env.context
        return bool(
            ctx.get('button_validate_picking_ids')
            or ctx.get('skip_backorder')
            or ctx.get('cancel_backorder')
            or ctx.get('picking_ids_not_to_backorder')
        )

    def write(self, vals):
        if self.env.context.get('allow_demand_update_after_draft'):
            return super().write(vals)

        # Permitir cambios internos de Odoo durante la validación
        if self._is_internal_picking_validation():
            _logger.info(
                "STOCK MOVE WRITE ALLOWED DURING PICKING VALIDATION | move_ids=%s | vals=%s | context=%s",
                self.ids, vals, self.env.context
            )
            return super().write(vals)

        if 'product_uom_qty' in vals:
            for move in self:
                if not move.picking_id:
                    continue

                if move.picking_id.state != 'draft':
                    current_qty = move.product_uom_qty
                    new_qty = float(vals.get('product_uom_qty') or 0.0)

                    comparison = float_compare(
                        current_qty,
                        new_qty,
                        precision_rounding=move.product_uom.rounding
                    )

                    _logger.info(
                        "STOCK MOVE WRITE CHECK | move_id=%s | picking_id=%s | state=%s | current=%s | new=%s | comparison=%s | vals=%s",
                        move.id,
                        move.picking_id.id,
                        move.picking_id.state,
                        current_qty,
                        new_qty,
                        comparison,
                        vals,
                    )

                    if comparison != 0:
                        raise UserError(_(
                            "Não é permitido alterar a quantidade demandada após a transferência sair do estado Rascunho."
                        ))

        return super().write(vals)