from odoo import api, fields, models


class SchoolSuggestionList(models.Model):
    _name = "school.student.suggestion"
    _description = "All Suggestion List Here"

    student_name=fields.Char(string="Student Name")
    student_class=fields.Char(string="Student Class")
    message=fields.Text(string="Message")

