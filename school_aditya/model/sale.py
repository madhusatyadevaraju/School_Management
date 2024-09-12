

from odoo import api, fields, models
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order" #Inherit the sale.order model in this module

    customer_note=fields.Text(string="Customer Note") #adding a text field into sale.order from here
    bank_name=fields.Char(string="Bank Name")
    ifsc_code=fields.Char(string="IFSC Code")
    account_number=fields.Float(string="Account Number")
    branch=fields.Char(string="Branch")


















