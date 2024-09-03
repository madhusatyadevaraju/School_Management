from email.policy import default
from lib2to3.fixes.fix_input import context

from odoo import api, fields, models


class StudentSuggestion(models.TransientModel):
    _name = 'student.suggestion'
    _description = 'student Suggestion'
    _rec_name = "student_name"

    # student_id = fields.Many2one('school.student', string="Student Name")
    student_name=fields.Char(string="Student Name", readonly=True)
    student_class = fields.Selection([('first', "First"),
                                      ('second', 'Second'),
                                      ('third', 'Third'),
                                      ('fourth', 'Fourth'),
                                      ('fifth', 'Fifth')], string="Student Class")
    suggestion = fields.Text(string="Suggestion")

    def action_save(self):
        self.ensure_one()
        return {'type': "ir.actions.act_window_close"}

    def action_cancel(self):
        self.ensure_one()
        return {'type': "ir.actions.act_window_close"}

    @api.model
    def default_get(self, fields_list):
        # Call the parent method to get the default values
        res = super(StudentSuggestion, self).default_get(fields_list)

        # Retrieve the context
        context = self.env.context

        # Get the default value from the context
        default_student_name = context.get('default_student_name')

        # Update the result dictionary with the default value if it exists
        if default_student_name:
            res.update({
                'student_name': default_student_name,  # Correct the field name to match your model
            })

        return res


