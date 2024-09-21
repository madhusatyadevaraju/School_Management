from odoo import api, fields, models
from datetime import datetime


class InventoryDelivery(models.Model):
    _inherit = "stock.picking" #Inherit the stock.picking model in this module

    bank_name= fields.Char(string="Bank Name")
    iban_code = fields.Char(string="IBAN No")
    account_name=fields.Char(string="Account Name")
    account_number = fields.Char(string="Account No")
    branch = fields.Char(string="Branch")