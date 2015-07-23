# This file is part stock_lot_inventory_qty module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from collections import defaultdict
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Inventory']
__metaclass__ = PoolMeta


class Inventory:
    __name__ = 'stock.inventory'

    @classmethod
    def update_lines(cls, inventories):
        '''
        Update the inventory lines
        '''
        pool = Pool()
        Line = pool.get('stock.inventory.line')
        Product = pool.get('product.product')

        super(Inventory, cls).update_lines(inventories)

        for inventory in inventories:
            product2lines = defaultdict(list)
            for line in inventory.lines:
                if (line.product.lot_is_required(inventory.location,
                            inventory.lost_found)
                        or line.product.lot_is_required(inventory.lost_found,
                            inventory.location)):
                    product2lines[line.product.id].append(line)

            if not product2lines:
                continue
    
            # Compute product quantities
            with Transaction().set_context(stock_date_end=inventory.date):
                pbl = Product.products_by_location([inventory.location.id],
                    product_ids=product2lines.keys(),
                    grouping=('product', 'lot'))

                product_qty = defaultdict(dict)
                for (location_id, product_id, lot_id), quantity \
                        in pbl.iteritems():
                    product_qty[product_id][lot_id] = quantity

                products = Product.browse(product_qty.keys())
                product2uom = dict((p.id, p.default_uom.id) for p in products)

                for product_id, lines in product2lines.iteritems():
                    quantities = product_qty[product_id]
                    uom_id = product2uom[product_id]
                    for line in lines:
                        lot_id = line.lot.id if line.lot else None
                        if lot_id in quantities:
                            quantity = quantities.pop(lot_id)
                        elif lot_id is None and quantities:
                            lot_id = quantities.keys()[0]
                            quantity = quantities.pop(lot_id)
                        else:
                            lot_id = None
                            quantity = 0.0

                        values = line.update_values4complete(quantity, uom_id)
                        if (values or lot_id != (line.lot.id
                                    if line.lot else None)):
                            values['lot'] = lot_id
                            Line.write([line], values)
