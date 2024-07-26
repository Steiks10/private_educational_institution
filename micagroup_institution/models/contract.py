from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Contract(models.Model):
    _name = "inscription.contract"
    _inherit = ['mail.thread']
    _description = "Contract"

    name = fields.Char(string="Name", required=True)
    is_active = fields.Boolean(string="Is Active", required=True)
    code = fields.Char(string='Code', required=True)
    credits = fields.Integer(string='Credits', required=True)
    theory_hours = fields.Integer(string='Theory Hours')
    practice_hours = fields.Integer(string='Practice Hours')
    limit_students = fields.Integer(string='Max capacity')

    # calendar_event_ids = fields.Many2many(comodel_name='calendar.event', string='Calendar')

