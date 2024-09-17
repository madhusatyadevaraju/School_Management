

from odoo import api, fields, models
from datetime import datetime

#Changes in Invoicing Module
class InvoicingOrder(models.Model):
    _inherit = "account.move" #Inherit the sale.order model in this module
#Below two fields are added to the Invoicing under customer Field
    parent_name=fields.Char(string="Parent Name") #adding a text field into sale.order from here
    parent_mobile=fields.Char(string="Parent Mobile")
    bank_name=fields.Char(string="Bank Name")
    ifsc_code = fields.Char(string="IFSC Code")
    account_number = fields.Char(string="Account Number")
    branch = fields.Char(string="Branch")


class ProductOrder(models.Model):
    _inherit = "account.move.line" #Inherit the sale.order model in this module
#add this many2one field_id beside of the product in Invoicing
    fees_id=fields.Many2one('fees.structure' , string="Fees")














