from odoo import api, fields, models
from datetime import datetime

from odoo.addons.test_new_api.tests.test_new_fields import select
from odoo.exceptions import ValidationError


class SchoolAdmission(models.Model):
    _name = "school.query"
    _description = "Admissions can be done here"

    name = fields.Char(string="Name")
    guardian_name = fields.Char(string="Guardian Name")
    parent_mobile=fields.Char(String="Mobile")
    status=fields.Selection([('draft','Draft'),('admit','Admit')],default='draft')
    joining_of_date=fields.Date(string="Admission Date")

    def action_create_student(self):

        student_id=self.env['school.student'].search([('mobile','=',self.parent_mobile)])

        print("StudentIds",student_id)
        for student in student_id:
            print(student.name,"Student Names")
        if student_id:
            raise ValidationError("There is a student with the same phone number !!!!")
        student = self.env['school.student']
        self.status = 'admit'
        today = datetime.today()
        for record in self:
            # Create a new student record in the school.student model
            student.create({
                'name': record.name,
                # Assuming class maps to standard
                'gaurdien_name': record.guardian_name,
                'mobile': record.parent_mobile,
                'student_status':record.status,
                "joining_of_date" :today

            })







