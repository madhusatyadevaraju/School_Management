from odoo import api, fields, models,_



class FeesStructure(models.Model):
    _name = 'fees.structure'
    _rec_name = "fee_type"


    fees_amount = fields.Float(string='Fees Amount')
    due_date = fields.Date(string='Due Date')
    fee_type=fields.Selection([('tuition fee','Tuition Fee'),('admission fee','Admission Fee'),('lab fee','Lab Fee'),('books fee','Books Fee')],string="Fee Type")
    student_id=fields.Many2one(comodel_name="school.student",string="Student")
    status=fields.Selection([("unpaid","Unpaid"),("paid","Paid")], default="unpaid",compute="_compute_status_payment")
    tax = fields.Many2many('account.tax', string="Tax")
    tax_amount = fields.Float(string='Tax Amount', compute='_compute_tax_amount', default=0.0, store=True)
    total_amount = fields.Float(string='Total', compute='_compute_total_amount', store=True)
    product_id=fields.Many2one('product.template',string="Product")
    invoice_id=fields.Many2one("account.move")

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

    def action_payment(self):
            print(self,"Button clicked")
            self.ensure_one()
            if self.invoice_id:
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Invoice'),
                    'res_model': 'account.move',
                    'res_id': self.invoice_id.id,
                    'view_mode': 'form',
                    'target': 'current',
                }

            else:
                # Example: Creating an invoice (dummy logic, adjust according to your needs)
                invoice = self.env['account.move'].create({
                        'partner_id': self.student_id.user_id.partner_id.id,  # Assuming you have a partner_id in school.student model
                        'parent_name':self.student_id.gaurdien_name,
                        'move_type': 'out_invoice',
                        'invoice_date': fields.Date.today(),
                        'invoice_line_ids': [(0, 0, {
                            'product_id':self.product_id.id,
                            'fees_id': self.id,
                            'name': 'Fee for %s' % self.fee_type,
                            'quantity': 1,
                            'price_unit': self.total_amount,
                            'tax_ids': [(6, 0, self.tax.ids)],
                        })],
                    })
                self.invoice_id=invoice.id
                # Optionally, open the created invoice
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Invoice'),
                    'res_model': 'account.move',
                    'res_id': invoice.id,
                    'view_mode': 'form',
                    'target': 'current',
                    }

    def _compute_status_payment(self):
        for record in self:
            if record.invoice_id:
                payment_state = record.invoice_id.payment_state
                if payment_state == "paid":
                    record.status = "paid"
                else:
                    record.status = "unpaid"
            else:
                record.status = "unpaid"