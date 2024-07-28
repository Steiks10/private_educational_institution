from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
class CourseGrade(models.Model):
    _name = "course.course"
    _inherit = ['mail.thread']
    _description = "Course Grade"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string='Code', readonly=True)
    # score = fields.Float(string='Score', required=True)
    calendar_event_ids = fields.Many2many(comodel_name='calendar.event', string='Calendar', compute='get_classes_from_calendar_event')
    subject_id = fields.Many2one(comodel_name='subject.subject', string='Subject')
    limit_students = fields.Integer(string='Max capacity')
    current_inscribed = fields.Integer(string='Current inscribed', compute='get_numbers_of_students_inscribed')
    credits = fields.Integer(related_name='subject_id.credits', string='Credits')
    # state = fields.Selection(selection=[
    #     ('in_progress', 'In progress'),
    #     ('passed', 'Passed'),
    #     ('reproved', 'Reproved'),
    # ])
    teacher_id = fields.Many2one(comodel_name='teacher.teacher', string="Teacher")
    student_grade_ids = fields.One2many(comodel_name='course.course.line', inverse_name='course_grade_id', compute='get_student_inscribed_in_the_course')


    @api.depends('student_grade_ids')
    def get_numbers_of_students_inscribed(self):
        for record in self:
            if record.student_grade_ids:
                record.current_inscribed = len(record.student_grade_ids)
            else:
                record.current_inscribed = 0

    @api.depends('calendar_event_ids')
    def get_classes_from_calendar_event(self):
        for record in self:
            # self.calendar_event_ids.unlink()
            classes_in_course = self.env['calendar.event'].search([('course_id', '=', record.id)])
            if classes_in_course:
                record.calendar_event_ids = classes_in_course.ids
            else:
                record.calendar_event_ids = False


    def get_student_inscribed_in_the_course(self):
        for record in self:
            # self.student_grade_ids.unlink()
            students_inscribed = self.env['inscription.contract'].search([('is_paid', '=', True), ('course_ids', 'in', record.id)]).mapped('student_id')
            if students_inscribed:
                values = []
                for student in students_inscribed:
                    if student.id not in record.student_grade_ids.ids:

                        values.append({
                            'course_grade_id': record.id,
                            'student_id': student.id,
                        })
                if values:
                    record.student_grade_ids.create(values)
            else:
                record.student_grade_ids = False

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].sudo().next_by_code('sequence_course_private_institution')
        return super(CourseGrade, self).create(vals)

class CourseGradeLine(models.Model):
    _name = "course.course.line"
    _description = "Course Grade Line"

    course_grade_id = fields.Many2one(comodel_name='course.course', string='Course Grade')
    student_id = fields.Many2one(comodel_name='student.student', string='Student')
    student_id_email = fields.Char(related='student_id.email', string='Email')
    student_id_phone = fields.Char(related='student_id.phone', string='Phone')
    student_id_identification = fields.Char(related='student_id.identification', string='Identification')
    student_id_image = fields.Image(related='student_id.image', string="Image")
    score = fields.Float(string="Score", readonly=False)
