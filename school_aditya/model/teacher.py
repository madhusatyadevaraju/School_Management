from odoo import api, fields, models


class SchoolPatient(models.Model):
    _name = "school.teacher"
    _description = "Teacher Master"

    name=fields.Char(string="Name")
    address=fields.Char(string="Address")
    mobile=fields.Char(string="Mobile")
    date_of_birth = fields.Date(string="Date Of Birth")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    is_teacher=fields.Boolean(string="Is_teacher")
