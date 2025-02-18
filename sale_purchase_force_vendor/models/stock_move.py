# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    propagated_sale_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Propagated SOL",
        compute="_compute_propagated_sale_line_id",
        store=True,
        help="Propagate the sale order line on the chained moves "
        "to get it on the purchase move and "
        "be able to retrieve the forced vendor",
    )

    @api.depends("sale_line_id")
    def _compute_propagated_sale_line_id(self):
        for rec in self:
            rec.propagated_sale_line_id = rec.sale_line_id

    def _prepare_procurement_values(self):
        """Inject the preferred vendor in case of an MTO that first creates the OUT
        move.
        """
        res = super()._prepare_procurement_values()
        # Get all chained moves to get sale line
        moves = self.browse(list(self._rollup_move_dests({self.id})))
        # Propagate the sale line from the dest moves
        if any(m.propagated_sale_line_id for m in moves.move_dest_ids):
            moves.write(
                {
                    "propagated_sale_line_id": moves.move_dest_ids.mapped(
                        "propagated_sale_line_id"
                    )[0].id
                }
            )
        move_sale = moves.filtered("propagated_sale_line_id")[:1]
        if move_sale.propagated_sale_line_id.vendor_id:
            res_order_line = (
                move_sale.propagated_sale_line_id._prepare_procurement_values(
                    group_id=move_sale.group_id
                )
            )
            res.update({"supplierinfo_id": res_order_line["supplierinfo_id"]})
        return res
