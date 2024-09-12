from odoo import api, fields, models
from datetime import datetime


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Brand Master"
    _rec_name ="brand_name"
    brand_name=fields.Char(string="Brand Name")



class ProductBrandInTemplate(models.Model):
    _inherit = "product.template"
    _description = "Product Brand In Product Template"
    brand_ids=fields.Many2one('product.brand',string="Product Brand")





