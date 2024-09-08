from email.policy import default
from lib2to3.fixes.fix_input import context

from odoo import api, fields, models, _
from datetime import datetime


class SchoolStudent(models.Model):
    _name = "school.student"
    _inherit = ["mail.thread"]
    _description = "Student Master"
    _rec_name = 'name'

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

    def _suggestion_count(self):
        self.suggestion_count = self.env['school.student.suggestion'].search_count(
            domain=[('student_name', '=', self.name)]
        )

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


    # @api.model
    # for the use of reporting returns
    # # def _get_report_values(self, docids, data=None):
    # #     docs = self.env['school.student'].browse(docids)
    # #     return {
    # #         'docs': docs,
    # #     }
