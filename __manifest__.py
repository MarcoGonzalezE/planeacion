# -*- coding: utf-8 -*-
{
    'name': "Planeacion",
    'version': '1.0.0',
    'license':'LGPL-3',
    'category': 'Inventory',
    'summary': "Inventario, Ventas, Fabricacion, Transferencias",
    'description': """
Control de Inventario - No Contable
===================================

Este modulo le permite llevar un control de inventario no contable, gestionado por fabricaciones y ventas.

Manejando el flujo de entradas y salidas:

* **Fabricacion** -> **Inventario** -> **Pedidos de Ventas** -> **Transferencias**
----------------------------------------------------------------------------------

* Entradas: Fabricaciones, Transferencias, Ajustes de Inventario, Devoluciones.
* Salidas: Ventas, Transferencias, Consumos, Ajustes de Inventario, Devoluciones de Productos, Re-procesos.
    """,

    'author': "Marco Gonzalez",
    'website': "http://www.grupoalvamex.com", 
    
    # Modulos necesarios para que este funcione correctamente
    'depends': ['base','sale','mrp','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/planeacion_data.xml',        
        'views/planeacion_ordenes_views.xml',
        'views/planeacion_sale_order_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,    
}