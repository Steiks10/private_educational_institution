from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class Evaluation(models.Model):
    _name = "evaluation.evaluation"
    _description = "Evaluation"

    name = fields.Char(string="Name", required=True)
    course_id = fields.Many2one(comodel_name='course.course', string='Course', required=True)
    instructions = fields.Text(string='Instructions')
    date_evaluation = fields.Date(string='Date Start', required=True)
    content_of_course = fields.Text(string='Content')
    document = fields.Binary(string='Document')