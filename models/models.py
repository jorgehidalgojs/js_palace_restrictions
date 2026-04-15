from odoo import models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare



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



                    if comparison != 0:
                        raise UserError(_(
                            "Não é permitido alterar a quantidade demandada após a transferência sair do estado Rascunho."
                        ))

        return super().write(vals)