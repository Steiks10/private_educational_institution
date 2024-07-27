from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Student(models.Model):
    _name = "student.student"
    _inherit = ['mail.thread']
    _description = "Student"

    name = fields.Char(string="Name", required=True)
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


