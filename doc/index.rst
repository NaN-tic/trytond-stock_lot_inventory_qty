Stock Inventory Expected Quantity by Lot
########################################

Extends the functionality of the button to compute the expected quantity of
product and lot for each inventory line.

1) If there is a lot in the inventory line, expected quantity of this lot is
computed.

2) If there is not a lot in the inventory line:

   2.a) If the lot is not required at inventory locations, the total expected
   quantiy of the product is computed.

   2.b) If the lot is required at inventory locations, new inventory lines are
   created, each one with a lot of the product and its expected quantity.
