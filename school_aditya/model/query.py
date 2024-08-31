from odoo import api, fields, models
from datetime import datetime

from odoo.addons.test_new_api.tests.test_new_fields import select


class SchoolAdmission(models.Model):
    _name = "school.query"
    _description = "Admissions can be done here"

    name = fields.Char(string="Name")
    guardian_name = fields.Char(string="Guardian Name")
    parent_mobile=fields.Char(String="Mobile")
    status=fields.Selection([('draft','Draft'),('admit','Admit')],default='draft')

    def action_create_student(self):
        self.status='admit'
        student = self.env['school.student']
        for record in self:
            # Create a new student record in the school.student model
            student.create({
                'name': record.name,
                # Assuming class maps to standard
                'gaurdien_name': record.guardian_name,
                'mobile': record.parent_mobile

            })







