from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Semester(models.Model):
    _name = "semester.semester"
    _description = "Semester"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence")