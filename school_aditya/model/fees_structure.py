from odoo import api, fields, models


class FeesStructure(models.Model):
    _name = 'fees.structure'
    _rec_name = "fees_amount"


    fees_amount = fields.Float(string='Fees Amount')
    due_date = fields.Date(string='Due Date')
    fee_type=fields.Selection([('1','Tuition Fee'),('2','Admission Fee'),('3','Lab Fee'),('4','Books Fee')],string="Fee Type")
    student_id=fields.Many2one(comodel_name="school.student",string="Student")
    status=fields.Selection([("unpaid","Unpaid"),("paid","Paid")], default="unpaid")

    def action_confirm(self):
        for rec in self:
            rec.status = "paid"

