

from odoo import api, fields, models
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order" #Inherit the sale.order model in this module

    customer_note=fields.Text(String="Customer Note") #adding a text field into sale.order from here

















