from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class CourseGrade(models.Model):
    _name = "course.course"
    _inherit = ['mail.thread']
    _description = "Course Grade"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string='Code', required=True)
    score = fields.Char(string='Score', required=True)
    calendar_event_ids = fields.Many2many(comodel_name='calendar.event', string='Calendar')
    student_ids = fields.Many2many(comodel_name='student.student', string='Students')
    subject_id = fields.Many2one(comodel_name='subject.subject', string='Subject')
    limit_students = fields.Integer(string='Max capacity')
    current_inscribed = fields.Integer(string='Current inscribed')
    # calendar_event_ids = fields.Many2many(comodel_name='calendar.event', string='Calendar')

