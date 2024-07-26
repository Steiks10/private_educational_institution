from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Teacher(models.Model):
    _name = "teacher.teacher"
    _inherit = ['mail.thread']
    _description = "Teacher"

    name = fields.Char(string="Name", required=True)
    birth_date = fields.Date(string='Birth Date', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address', required=True)
    gender = fields.Selection(selection=[
                ('M', 'Masculino'),
                ('F', 'Femenino'),
                ('N/A', 'No responder')],
                string="Gender", required=True)
    date_of_admision = fields.Date(string='Enrollment Date', required=True, default=datetime.today())

