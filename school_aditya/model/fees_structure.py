from odoo import api, fields, models


class FeesStructure(models.Model):
    _name = 'fees.structure'
    _rec_name = "fees_amount"


    fees_amount = fields.Float(string='Fees Amount')
    due_date = fields.Date(string='Due Date')
    fee_type=fields.Selection([('tuition fee','Tuition Fee'),('admission fee','Admission Fee'),('lab fee','Lab Fee'),('books fee','Books Fee')],string="Fee Type")
    student_id=fields.Many2one(comodel_name="school.student",string="Student")
    status=fields.Selection([("unpaid","Unpaid"),("paid","Paid")], default="unpaid")
    tax = fields.Many2many('account.tax', string="Tax")
    tax_amount = fields.Float(string='Tax Amount', compute='_compute_tax_amount', default=0.0, store=True)
    total_amount = fields.Float(string='Total', compute='_compute_total_amount', store=True)

    def action_confirm(self):
        for rec in self:
            rec.status = "paid"

    @api.depends('fees_amount', 'tax')
    def _compute_tax_amount(self):
        for rec in self:
            total_tax_amount = 0.0
            if rec.tax:
                for tax in rec.tax:
                    total_tax_amount += (rec.fees_amount * tax.amount / 100)
                rec.tax_amount = total_tax_amount
            else:
                rec.tax_amount = 0

    @api.depends('fees_amount', 'tax_amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.fees_amount + rec.tax_amount

