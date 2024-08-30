from odoo import api, fields, models


class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "Student Master"

    name=fields.Char(string="Name")
    address=fields.Char(string="Address")
    gaurdien_name=fields.Char(string="Guardien_Name")
    mobile=fields.Char(string="Mobile")
    date_of_birth = fields.Date(string="DOM")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    joining_of_date=fields.Date(string="JOD")
    teacher=fields.Many2one(comodel_name="school.teacher",string="Class Teacher")
    teacher_ids=fields.Many2many(comodel_name="school.teacher",
                                 string="other subjects teachers",
                                 help="Mention the teachers who teach other subjects as well")

    state=fields.Selection([("not selected","Not Selected"),("selected","Selected")],
                             string="Selected",default="not selected")
    student_fees=fields.One2many(comodel_name="fees.structure", inverse_name="student_id",
                                 string="Fees Structure")

    def action_confirm(self):
        for rec in self:
            rec.state="selected"






