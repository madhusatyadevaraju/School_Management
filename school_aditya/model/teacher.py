from odoo import api, fields, models



class SchoolPatient(models.Model):
    _name = "school.teacher"
    _description = "Teacher Master"

    name=fields.Char(string="Name",required=True)
    address=fields.Char(string="Address")
    mobile=fields.Char(string="Mobile")
    date_of_birth = fields.Date(string="Date Of Birth")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    is_teacher=fields.Boolean(string="Is_teacher")
    status=fields.Selection([('draft','Draft'),('permanent','Permanent')] , default='draft',
                            string='Status')
    teacher_user_id = fields.Many2one('res.users', string='Login User')

    def action_teacher(self):
        self.status='permanent'

        user_vals = {
            'name': self.name,
            'login': self.name,
            'email': self.name+'@gmail.com',
            'password': self.name,
            'groups_id': [(6, 0, [self.env.ref('school_aditya.group_school_teachers').id])]

        }
        user=self.env['res.users'].create(user_vals)
        for record in self:
            record.teacher_user_id = user.id
