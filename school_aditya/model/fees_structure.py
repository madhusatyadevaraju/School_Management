from odoo import api, fields, models


class FeesStructure(models.Model):
    _name = 'fees.structure'

    fees_amount = fields.Float(string='Fees Amount')
    due_date = fields.Date(string='Due Date')
    student_id=fields.Many2one(comodel_name="school.student",string="Student")
