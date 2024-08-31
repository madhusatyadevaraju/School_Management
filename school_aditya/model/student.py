

from odoo import api, fields, models
from datetime import datetime


class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "Student Master"

    name=fields.Char(string="Name")
    address=fields.Char(string="Address")
    gaurdien_name=fields.Char(string="Guardien Name")
    mobile=fields.Char(string="Mobile")
    date_of_birth = fields.Date(string="Date Of Birth")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    joining_of_date=fields.Date(string="Joining Date")
    teacher=fields.Many2one(comodel_name="school.teacher",string="Class Teacher")
    teacher_ids=fields.Many2many(comodel_name="school.teacher",
                                 string="other subjects teachers",
                                 help="Mention the teachers who teach other subjects as well")

    state=fields.Selection([("not selected","Not Selected"),("selected","Selected")],
                             string="Selected",default="not selected")
    student_fees=fields.One2many(comodel_name="fees.structure", inverse_name="student_id",
                                 string="Fees Structure")
    consultant_no=fields.Char(String="Teacher No")

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True
        # Optionally, store the computed value in the database
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
            rec.state="selected"

    @api.onchange("teacher")
    def _onchange_teacher(self):
        if self.teacher:
            self.consultant_no=self.teacher.mobile




