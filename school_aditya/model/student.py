import base64
from email.policy import default
from lib2to3.fixes.fix_input import context

from odoo import api, fields, models, _
from datetime import datetime

from odoo.exceptions import UserError


class SchoolStudent(models.Model):
    _name = "school.student"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = "Student Master"
    _rec_name = 'name'

    active = fields.Boolean(default=True)
    name = fields.Char(string="Name", tracking=True, required=True)
    email = fields.Char(string="Email")
    address = fields.Char(string="Address")
    gaurdien_name = fields.Char(string="Guardien Name")
    mobile = fields.Char(string="Mobile")
    date_of_birth = fields.Date(string="Date Of Birth")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    joining_of_date = fields.Date(string="Joining Date")
    teacher = fields.Many2one(comodel_name="school.teacher", string="Class Teacher")
    teacher_ids = fields.Many2many(comodel_name="school.teacher",
                                   string="other subjects teachers",
                                   help="Mention the teachers who teach other subjects as well")

    state = fields.Selection([("not selected", "Not Selected"), ("selected", "Selected")],
                             string="Selected", default="not selected")
    student_fees = fields.One2many(comodel_name="fees.structure", inverse_name="student_id",
                                   string="Fees Structure")
    consultant_no = fields.Char(string="Teacher No")
    user_id = fields.Many2one('res.users', string='Login User')

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True
        # Optionally, store the computed value in the database
    )
    student_status = fields.Char(string="Status")
    suggestion_count = fields.Integer(string="Suggestion", compute='_suggestion_count')
    invoice_count = fields.Integer(string='Invoices', compute='_compute_invoice_count')

    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True, readonly=True)
    untaxed_amount = fields.Float(string="Untaxed Amount", store=True, readonly=True)
    taxed_amount = fields.Float(string="Total tax Amount", store=True, readonly=True)
    # partner_id = fields.Many2one('res.partner', string='Partner')

    student_img=fields.Image(string="Student Image")

    @api.depends('student_fees.total_amount', 'student_fees.fees_amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(i.total_amount for i in rec.student_fees)
            rec.untaxed_amount = sum(j.fees_amount for j in rec.student_fees)
            rec.taxed_amount = rec.total_amount - rec.untaxed_amount

    def _suggestion_count(self):
        self.suggestion_count = self.env['school.student.suggestion'].search_count(
            domain=[('student_name', '=', self.name)]
        )
    # Compute the invoices and return the inovices


    def _compute_invoice_count(self):
        for student in self:
            student.invoice_count = self.env['account.move'].search_count(domain=[('partner_id', '=', student.name), ('move_type', '=', 'out_invoice')])

    def action_view_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.user_id.partner_id.id), ('move_type', '=', 'out_invoice')],
            'context': dict(self.env.context),
        }

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                # Calculate the age
                today = datetime.today()
                dob = fields.Date.from_string(record.date_of_birth)
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                record.age = age
            else:
                record.age = 0

    def action_confirm(self):
        for rec in self:
            rec.state = "selected"
            user_vals = {
                'name': self.name,
                'login': self.name,
                'email': self.email,
                'password': self.name,
                'groups_id': [(6, 0, [self.env.ref('school_aditya.group_school_student').id])]
            }
            user = self.env['res.users'].create(user_vals)
            for record in self:
                record.user_id = user.id

    @api.onchange("teacher")
    def _onchange_teacher(self):
        if self.teacher:
            self.consultant_no = self.teacher.mobile

# For creating a Wizard in school.student model
    def action_suggestion(self):
        return {
            'name': _('Suggestion'),
            'type': 'ir.actions.act_window',
            'res_model': 'student.suggestion',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_student_name': self.name}

        }

    def action_open_suggestion_wizard(self):
        return {
            'name': _('Suggestion'),
            'type': 'ir.actions.act_window',
            'res_model': 'school.student.suggestion',
            'view_mode': 'tree',
            'domain': [('student_name', '=', self.name)]

        }
        # for creating a users

    def action_send_email(self):
        template = self.env.ref('school_aditya.email_template_student_guardian')
        mail=template.send_mail(self.id, force_send=True)
        print("hello working",mail)

    # fee due date rremainders
    @api.model
    def send_end_date_notifications_cron(self):
        today = datetime.today().date()
        due_students = self.search([('student_fees.due_date', '=', today)])
        for student in due_students:
            message = f"Fees for the student with ID {student.id} are due today!"
            student.message_post(body=message)
            template = self.env.ref('school_aditya.student_due_date_reminder_email_template')
            mail = template.send_mail(student.id, force_send=True)
            print("hello working", mail)







