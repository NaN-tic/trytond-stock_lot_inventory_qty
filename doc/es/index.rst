===============================================================
Stock. Calcula la cantidad estimada en el inventario según lote
===============================================================

Amplia la funcionalidad del botón para recalcular la cantidad estimada de
producto y lote por cada línea de inventario.

1) Si en la línea de inventario se indica el lote, se calcula la cantidad
estimada de este lote.

2) Si en la línea de inventario no se indica el lote:

  2.a) Si el lote no es requerido en las ubicaciones del inventario, se calcula
  la cantidad estimada total del producto.

  2.b) Si el lote es requerido en las ubicaciones del inventario, se crean
  nuevas líneas de inventario, cada una con un lote del producto y su cantidad
  estimada, siempre que la cantiad estimada sea distinta de cero, para evitar
  rellenar con lotes antiguos que ya no tienen stock.
