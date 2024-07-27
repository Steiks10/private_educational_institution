from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Subject(models.Model):
    _name = "subject.subject"
    _inherit = ['mail.thread']
    _description = "Subject"

    name = fields.Char(string="Name", required=True)
    is_active = fields.Boolean(string="Is Active", required=True)
    code = fields.Char(string='Code', required=True)
    credits = fields.Integer(string='Credits', required=True)
    theory_hours = fields.Integer(string='Theory Hours')
    practice_hours = fields.Integer(string='Practice Hours')
    semester = fields.Selection(selection=[
        ('first_semester', 'First semester'),
        ('second_semester', 'Second semester'),
        ('third_semester', 'Third semester'),
        ('fourth_semester', 'Fourth semester'),
        ('fifth_semester', 'Fifth semester'),
        ('sixth_semester', 'Sixth semester'),
        ('seventh_semester', 'Seventh semester'),
        ('eighth_semester', 'Eighth semester'),
        ('nineth_semester', 'Ninth semester'),
        ('tenth_semester', 'Tenth semester'),
    ], string='Semester', required=True)
    career_id = fields.Many2one(comodel_name='career.career',  string='Career')
    image = fields.Image(string='Imagen')