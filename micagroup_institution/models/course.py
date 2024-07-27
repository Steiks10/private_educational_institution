from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class CourseGrade(models.Model):
    _name = "course.course"
    _inherit = ['mail.thread']
    _description = "Course Grade"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string='Code', required=True)
    # score = fields.Float(string='Score', required=True)
    calendar_event_ids = fields.Many2many(comodel_name='calendar.event', string='Calendar')
    subject_id = fields.Many2one(comodel_name='subject.subject', string='Subject')
    limit_students = fields.Integer(string='Max capacity')
    current_inscribed = fields.Integer(string='Current inscribed')
    # state = fields.Selection(selection=[
    #     ('in_progress', 'In progress'),
    #     ('passed', 'Passed'),
    #     ('reproved', 'Reproved'),
    # ])
    teacher_id = fields.Many2one(comodel_name='teacher.teacher', string="Teacher")
    student_grade_ids = fields.One2many(comodel_name='course.course.line', inverse_name='course_grade_id')

class CourseGradeLine(models.Model):
    _name = "course.course.line"
    _description = "Course Grade Line"

    course_grade_id = fields.Many2one(comodel_name='course.course', string='Course Grade')
    student_id = fields.Many2one(comodel_name='student.student', string='Student')
    student_id_email = fields.Char(related='student_id.email', string='Email')
    student_id_phone = fields.Char(related='student_id.phone', string='Phone')
    student_id_identification = fields.Char(related='student_id.identification', string='Identification')
    student_id_image = fields.Image(related='student_id.image', string="Image")
    score = fields.Float(string="Score")
