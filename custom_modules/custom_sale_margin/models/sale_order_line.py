from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    purchase_price = fields.Float(string="Purchase Price")
    price_unit = fields.Float(string="Unit Price", required=True)

    @api.onchange('product_id', 'product_uom_qty')
    def _onchange_product_and_quantity(self):
        """
        Dynamically calculate and set the weighted average purchase price and
        selling price with a 10% margin.
        """
        self._compute_prices()

    def _compute_prices(self):
        """
        Core logic for fetching lot-based purchase prices, calculating weighted
        averages, and determining selling price.
        """

        if self.product_id:
                # Fetch available lots with quantities for the selected product
                available_quants = self.env['stock.quant'].search([
                    ('product_id', '=', self.product_id.id),
                    ('quantity', '>', 0),
                    ('location_id.usage', '=', 'internal')  # Only internal stock locations
                ])

                required_quantity = self.product_uom_qty
                selected_lots = []
                purchase_price = []
                remaining_quantity = required_quantity

                for quant in available_quants:
                    if remaining_quantity <= 0:
                        break
                    if quant.quantity > 0:
                        selected_lots.append(quant.lot_id.id)
                        remaining_quantity -= quant.quantity

                        # Fetch the purchase order price for the lot
                        lot = quant.lot_id
                        print(lot.name)
                        if lot:
                            stock_moves = self.env['stock.move.line'].search([('lot_id', '=', lot.id)])
                            for move_line in stock_moves:
                                stock_picking = move_line.move_id.picking_id
                                if not stock_picking or not stock_picking.origin:
                                    continue  # Skip if no picking or origin
                                # Step 4: Trace the purchase order using the origin field
                                purchase_order = self.env['purchase.order'].search([('name', '=', stock_picking.origin)],
                                                                                   limit=1)
                                if not purchase_order:
                                    continue

                                # Step 5: Match the product in the lot with the purchase order line
                                po_line = purchase_order.order_line.filtered(
                                    lambda line: line.product_id == lot.product_id)
                                if po_line:
                                    purchase_price.append(po_line[0].price_unit)
                                    print('unit_price',po_line[0].price_unit)
                                    # return {'unit_price': po_line[0].price_unit}

                                print("stock move" , )
                            # if stock_moves:
                            #     purchase_line = stock_moves.purchase_line_id
                            #     purchase_price.append(purchase_line.price_unit)
                if len(purchase_price)>1 :
                    raise ValidationError("You cannot increase the quantity of this product by adding items from different serial numbers. Please ensure all selected quantities belong to the same serial number.")
                purchase_price_c = purchase_price[0] if purchase_price else 0
                if selected_lots and purchase_price_c:
                    selling_price = purchase_price_c / 0.9 if purchase_price_c > 0 else 0.0
                    self.purchase_price = purchase_price_c
                    self.price_unit = selling_price
                    print(f"Selected Lots: {selected_lots}")
                    print(f"Selected Lots: {remaining_quantity}")
                    print(f"Purchase Price: {purchase_price}")
                else:
                    raise ValidationError("Insufficient Stock")


    @api.model
    def create(self, vals):
        """
        Override create to persist calculated prices.
        """
        record = super(SaleOrderLine, self).create(vals)
        if 'product_id' in vals or 'product_uom_qty' in vals:
            record._compute_prices()
        return record

    def write(self, vals):
        """
        Override write to persist calculated prices.
        """
        result = super(SaleOrderLine, self).write(vals)
        if 'product_id' in vals or 'product_uom_qty' in vals:
            for record in self:
                record._compute_prices()
        return result


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """
        When the partner changes, ensure that the sales order lines preserve
        their computed prices.
        """
        for line in self.order_line:
           line._compute_prices()

















# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     purchase_price = fields.Float(string="Purchase Price")
#     price_unit = fields.Float(
#         string="Unit Price", required=True)
#
#     @api.onchange('product_id')
#     def _onchange_product_and_quantity(self):
#         """
#         Dynamically calculate and set the weighted average purchase price and
#         selling price with a 10% margin.
#         """
#         self._compute_prices()
#
#     def _compute_prices(self):
#         """
#         Core logic for fetching lot-based purchase prices, calculating weighted
#         averages, and determining selling price.
#         """
#         if self.product_id:
#             available_quants = self.env['stock.quant'].search([
#                 ('product_id', '=', self.product_id.id),
#                 ('quantity', '>', 0),
#                 ('location_id.usage', '=', 'internal')  # Only internal stock locations
#             ])
#
#             required_quantity = self.product_uom_qty
#             purchase_price_data = []  # To store tuples of (quantity, price)
#             remaining_quantity = required_quantity
#
#             for quant in available_quants:
#                 if remaining_quantity <= 0:
#                     break
#
#                 if quant.quantity > 0:
#                     lot_quantity = min(quant.quantity, remaining_quantity)
#                     remaining_quantity -= lot_quantity
#
#                     lot = quant.lot_id
#                     if lot:
#                         stock_moves = self.env['stock.move.line'].search([('lot_id', '=', lot.id)])
#                         for move_line in stock_moves:
#                             stock_picking = move_line.move_id.picking_id
#                             if not stock_picking or not stock_picking.origin:
#                                 continue
#
#                             purchase_order = self.env['purchase.order'].search([('name', '=', stock_picking.origin)],
#                                                                                limit=1)
#                             if not purchase_order:
#                                 continue
#
#                             po_line = purchase_order.order_line.filtered(
#                                 lambda line: line.product_id == lot.product_id)
#                             if po_line:
#                                 unit_price = po_line[0].price_unit
#                                 purchase_price_data.append((lot_quantity, unit_price))
#                                 break
#
#             # Calculate weighted average price
#             total_price = sum(qty * price for qty, price in purchase_price_data)
#             total_quantity = sum(qty for qty, _ in purchase_price_data)
#             weighted_average_price = total_price / total_quantity if total_quantity > 0 else 0.0
#
#             # Calculate selling price with 10% margin
#             selling_price = weighted_average_price / 0.9 if weighted_average_price > 0 else 0.0
#
#             self.purchase_price = weighted_average_price
#             self.price_unit = selling_price
#
#     @api.model
#     def create(self, vals):
#         """
#         Override create to persist calculated prices.
#         """
#         record = super(SaleOrderLine, self).create(vals)
#         record._compute_prices()
#         return record

    # def write(self, vals):
    #     """
    #     Override write to persist calculated prices.
    #     """
    #     result = super(SaleOrderLine, self).write(vals)
    #     for record in self:
    #         record._compute_prices()
    #     return result
# from odoo import models, fields, api
#
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     @api.onchange('product_id', 'product_uom_qty')
#     def _onchange_product_and_quantity(self):
#         """
#         Fetch appropriate lot numbers based on the product and required quantity,
#         calculate the weighted average price from purchase orders for those lots,
#         and update the Sales Order Line with price_unit (average price + 10% margin)
#         and purchase_price (average price).
#         """
#         if self.product_id:
#             # Fetch available lots with quantities for the selected product
#             available_quants = self.env['stock.quant'].search([
#                 ('product_id', '=', self.product_id.id),
#                 ('quantity', '>', 0),
#                 ('location_id.usage', '=', 'internal')  # Only internal stock locations
#             ])
#
#             required_quantity = self.product_uom_qty
#             selected_lots = []
#             purchase_price_data = []  # To store tuples of (quantity, price)
#             remaining_quantity = required_quantity
#
#             for quant in available_quants:
#                 if remaining_quantity <= 0:
#                     break
#
#                 if quant.quantity > 0:
#                     selected_lots.append(quant.lot_id.id)
#
#                     # Determine the quantity to use from the current lot
#                     lot_quantity = min(quant.quantity, remaining_quantity)
#                     remaining_quantity -= lot_quantity
#
#                     # Fetch the purchase order price for the lot
#                     lot = quant.lot_id
#                     if lot:
#                         stock_moves = self.env['stock.move.line'].search([('lot_id', '=', lot.id)])
#                         for move_line in stock_moves:
#                             stock_picking = move_line.move_id.picking_id
#                             if not stock_picking or not stock_picking.origin:
#                                 continue  # Skip if no picking or origin
#
#                             # Trace the purchase order using the origin field
#                             purchase_order = self.env['purchase.order'].search([('name', '=', stock_picking.origin)],
#                                                                                limit=1)
#                             if not purchase_order:
#                                 continue
#
#                             # Match the product in the lot with the purchase order line
#                             po_line = purchase_order.order_line.filtered(
#                                 lambda line: line.product_id == lot.product_id)
#                             if po_line:
#                                 unit_price = po_line[0].price_unit
#                                 purchase_price_data.append((lot_quantity, unit_price))
#                                 break  # Use the first matching purchase order
#
#             # Calculate the weighted average price
#             total_price = sum(qty * price for qty, price in purchase_price_data)
#             total_quantity = sum(qty for qty, _ in purchase_price_data)
#             weighted_average_price = total_price / total_quantity if total_quantity > 0 else 0.0
#
#             # Calculate the selling price with a 10% margin
#             selling_price = weighted_average_price / 0.9 if weighted_average_price > 0 else 0.0
#
#             # Update the Sales Order Line fields
#             self.purchase_price = weighted_average_price  # Average purchase price
#             self.price_unit = selling_price  # Selling price with 10% margin
#
#             if selected_lots:
#                 print(f"Selected Lots: {selected_lots}")
#                 print(f"Remaining Quantity: {remaining_quantity}")
#                 print(f"Purchase Price Data: {purchase_price_data}")
#                 print(f"Weighted Average Price: {weighted_average_price}")
#                 print(f"Selling Price with 10% Margin: {selling_price}")
#             else:
#                 return {
#                     'warning': {
#                         'title': "Insufficient Stock",
#                         'message': f"No sufficient quantity available for {self.product_id.display_name}."
#                     }
#                 }

    # @api.onchange('product_id', 'product_uom_qty')
    # def _onchange_product_and_quantity(self):
    #     """
    #     Fetch appropriate lot numbers based on the product and required quantity
    #     and retrieve the weighted average purchase price for those lots.
    #     """
    #     if self.product_id:
    #         # Fetch available lots with quantities for the selected product
    #         available_quants = self.env['stock.quant'].search([
    #             ('product_id', '=', self.product_id.id),
    #             ('quantity', '>', 0),
    #             ('location_id.usage', '=', 'internal')  # Only internal stock locations
    #         ], order='lot_id, id')
    #
    #         required_quantity = self.product_qty
    #         selected_lots = []
    #         purchase_price_data = []  # To store tuples of (quantity, price)
    #         remaining_quantity = required_quantity
    #
    #         for quant in available_quants:
    #             if remaining_quantity <= 0:
    #                 break
    #
    #             if quant.quantity > 0:
    #                 selected_lots.append(quant.lot_id.id)
    #
    #                 # Determine the quantity to use from the current lot
    #                 lot_quantity = min(quant.quantity, remaining_quantity)
    #                 remaining_quantity -= lot_quantity
    #
    #                 # Fetch the purchase order price for the lot
    #                 lot = quant.lot_id
    #                 if lot:
    #                     stock_moves = self.env['stock.move.line'].search([('lot_id', '=', lot.id)])
    #                     for move_line in stock_moves:
    #                         stock_picking = move_line.move_id.picking_id
    #                         if not stock_picking or not stock_picking.origin:
    #                             continue  # Skip if no picking or origin
    #
    #                         # Trace the purchase order using the origin field
    #                         purchase_order = self.env['purchase.order'].search([('name', '=', stock_picking.origin)],
    #                                                                            limit=1)
    #                         if not purchase_order:
    #                             continue
    #
    #                         # Match the product in the lot with the purchase order line
    #                         po_line = purchase_order.order_line.filtered(
    #                             lambda line: line.product_id == lot.product_id)
    #                         if po_line:
    #                             unit_price = po_line[0].price_unit
    #                             purchase_price_data.append((lot_quantity, unit_price))
    #                             break  # Use the first matching purchase order
    #
    #         # Calculate the weighted average price
    #         total_price = sum(qty * price for qty, price in purchase_price_data)
    #         total_quantity = sum(qty for qty, _ in purchase_price_data)
    #         weighted_average_price = total_price / total_quantity if total_quantity > 0 else 0.0
    #
    #         if selected_lots:
    #             print(f"Selected Lots: {selected_lots}")
    #             print(f"Remaining Quantity: {remaining_quantity}")
    #             print(f"Purchase Price Data: {purchase_price_data}")
    #             print(f"Weighted Average Price: {weighted_average_price}")
    #         else:
    #             return {
    #                 'warning': {
    #                     'title': "Insufficient Stock",
    #                     'message': f"No sufficient quantity available for {self.product_id.display_name}."
    #                 }
    #             }




    # @api.onchange('product_id', 'product_uom_qty')
    # def _onchange_product_and_quantity(self):
    #     """
    #     Fetch appropriate lot numbers based on the product and required quantity
    #     and retrieve the purchase price for those lots.
    #     """
    #     if self.product_id:
    #         # Fetch available lots with quantities for the selected product
    #         available_quants = self.env['stock.quant'].search([
    #             ('product_id', '=', self.product_id.id),
    #             ('quantity', '>', 0),
    #             ('location_id.usage', '=', 'internal')  # Only internal stock locations
    #         ], order='lot_id, id')
    #
    #         required_quantity = self.product_qty
    #         selected_lots = []
    #         purchase_price = []
    #         remaining_quantity = required_quantity
    #
    #         for quant in available_quants:
    #             if remaining_quantity <= 0:
    #                 break
    #             if quant.quantity > 0:
    #                 selected_lots.append(quant.lot_id.id)
    #                 remaining_quantity -= quant.quantity
    #
    #                 # Fetch the purchase order price for the lot
    #                 lot = quant.lot_id
    #                 print(lot.name)
    #                 if lot:
    #                     stock_moves = self.env['stock.move.line'].search([('lot_id', '=', lot.id)])
    #                     for move_line in stock_moves:
    #                         stock_picking = move_line.move_id.picking_id
    #                         if not stock_picking or not stock_picking.origin:
    #                             continue  # Skip if no picking or origin
    #                         # Step 4: Trace the purchase order using the origin field
    #                         purchase_order = self.env['purchase.order'].search([('name', '=', stock_picking.origin)],
    #                                                                            limit=1)
    #                         if not purchase_order:
    #                             continue
    #
    #                         # Step 5: Match the product in the lot with the purchase order line
    #                         po_line = purchase_order.order_line.filtered(
    #                             lambda line: line.product_id == lot.product_id)
    #                         if po_line:
    #                             purchase_price.append(po_line[0].price_unit)
    #                             print('unit_price',po_line[0].price_unit)
    #                             # return {'unit_price': po_line[0].price_unit}
    #
    #                         print("stock move" , )
    #                     # if stock_moves:
    #                     #     purchase_line = stock_moves.purchase_line_id
    #                     #     purchase_price.append(purchase_line.price_unit)
    #
    #         if selected_lots:
    #             print(f"Selected Lots: {selected_lots}")
    #             print(f"Selected Lots: {remaining_quantity}")
    #             print(f"Purchase Price: {purchase_price}")
    #         else:
    #             return {
    #                 'warning': {
    #                     'title': "Insufficient Stock",
    #                     'message': f"No sufficient quantity available for {self.product_id.display_name}."
    #                 }
    #             }


    # @api.onchange('product_id', 'product_uom_qty')
    # def _onchange_product_and_quantity(self):
    #     """
    #     Fetch appropriate lot numbers based on the product and required quantity.
    #     """
    #     if self.product_id:
    #         # Fetch available lots with quantities for the selected product
    #         available_quants = self.env['stock.quant'].search([
    #             ('product_id', '=', self.product_id.id),
    #             ('quantity', '>', 0),
    #             ('location_id.usage', '=', 'internal')  # Only internal stock locations
    #         ], order='lot_id, id')
    #         print(available_quants)
    #         required_quantity = self.product_qty
    #         selected_lots = []
    #
    #         for quant in available_quants:
    #             if required_quantity <= 0:
    #                 break
    #             if quant.quantity > 0:
    #                 selected_lots.append(quant.lot_id.id)
    #                 required_quantity -= quant.quantity
    #         print(required_quantity , selected_lots)
    #         if selected_lots:
    #             print(selected_lots)
    #         else:
    #             return {
    #                 'warning': {
    #                     'title': "Insufficient Stock",
    #                     'message': f"No sufficient quantity available for {self.product_id.display_name}."
    #                 }
    #             }
