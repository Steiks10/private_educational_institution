from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Student(models.Model):
    _name = "student.student"
    _inherit = ['mail.thread']
    _description = "Student"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string='Code', readonly=True)
    birth_date = fields.Date(string='Birth Date', required=True)
    identification = fields.Char(string='Identification', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address', required=True)
    gender = fields.Selection(selection=[
                ('M', 'Masculino'),
                ('F', 'Femenino'),
                ('N/A', 'No responder')],
                string="Gender", required=True)
    enrollment_date = fields.Date(string='Enrollment Date', required=True, default=datetime.today())
    graduation_date = fields.Date(string='Graduation Date')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('registered', 'Registered'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
        ('expelled', 'Expelled')
    ], string="State", required=True)
    academic_record_ids = fields.Many2many(comodel_name='course.course', string='Academic Record')
    thesis = fields.Binary(string='Thesis')
    image = fields.Image(string='Image')
    res_user_id = fields.Many2one(comodel_name='res.users', string='Usuario')

    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].sudo().next_by_code('sequence_student_private_institution')
        return super(Student, self).create(vals)

