from odoo import api, fields, models


class FeesStructure(models.Model):
    _name = 'fees.structure'
    _rec_name = "fees_amount"


    fees_amount = fields.Float(string='Fees Amount')
    due_date = fields.Date(string='Due Date')
    fee_type=fields.Selection([('tuition fee','Tuition Fee'),('admission fee','Admission Fee'),('lab fee','Lab Fee'),('books fee','Books Fee')],string="Fee Type")
    student_id=fields.Many2one(comodel_name="school.student",string="Student")
    status=fields.Selection([("unpaid","Unpaid"),("paid","Paid")], default="unpaid")

    def action_confirm(self):
        for rec in self:
            rec.status = "paid"

