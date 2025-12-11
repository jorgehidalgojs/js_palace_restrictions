
from odoo import models
from odoo.exceptions import UserError
class Stock_move(models.Model):
    _inherit = 'stock.move'

    def write(self, vals):
        if 'product_uom_qty' in vals:
            for move in self:
                if move.picking_id and move.picking_id.state != 'draft':
                    raise UserError("Não é permitido alterar a quantidade depois que o picking sair do estado Draft.")

        return super(Stock_move, self).write(vals)