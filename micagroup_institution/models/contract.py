from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Contract(models.Model):
    _name = "inscription.contract"
    _inherit = ['mail.thread']
    _description = "Inscription Contract"

    name = fields.Char(string="Name", compute='get_name_according_to_student')
    is_paid = fields.Boolean(string="Is paid", default=False)
    code = fields.Char(string='Code', required=True)
    credits = fields.Integer(string='Credits', required=True)
    theory_hours = fields.Integer(string='Theory Hours')
    practice_hours = fields.Integer(string='Practice Hours')
    student_id = fields.Many2one(comodel_name='student.student', string='Student', required=False)
    # student_contract_id = fields.Many2one(comodel_name='student.student', string)
    course_ids = fields.Many2many(comodel_name='course.course', string='Courses')

    @api.depends('student_id')
    def get_name_according_to_student(self):
        for record in self:
            if record.student_id:
                record.name = f"Contract for {record.student_id.name}"
            else:
                record.name = False
                print(record)