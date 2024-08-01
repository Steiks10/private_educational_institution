from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Career(models.Model):
    _name = "career.career"
    _description = "Career"

    name = fields.Char(string="Name", required=True)