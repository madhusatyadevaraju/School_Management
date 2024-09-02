

from odoo import api, fields, models
from datetime import datetime


class InvoicingOrder(models.Model):
    _inherit = "account.move" #Inherit the sale.order model in this module

    parent_name=fields.Char(string="Parent Name") #adding a text field into sale.order from here
    parent_mobile=fields.Char(string="Parent Mobile")


class ProductOrder(models.Model):
    _inherit = "account.move.line" #Inherit the sale.order model in this module

    fees_id=fields.Many2one('fees.structure' , string="Fees")














