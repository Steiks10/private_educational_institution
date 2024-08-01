from odoo import models, fields, api

class CalendarCourses(models.Model):
   _inherit = 'calendar.event'
   _description = 'Calendar Courses'

   course_id = fields.Many2one(comodel_name='course.course', string='course')
   teacher_id = fields.Many2one(comodel_name='teacher.teacher', related='course_id.teacher_id', string='Teacher')
   code = fields.Char(related='course_id.code', string='Code')
   semester = fields.Many2one(comodel_name='semester.semester', compute='get_semester_and_hours_from_course_id', string='Semester')
   limit_students = fields.Integer(related='course_id.limit_students', string='Max capacity')
   current_inscribed = fields.Integer(related='course_id.current_inscribed', string='Current inscribed')
   practice_hours = fields.Integer(string='Current inscribed', readonly=True)
   theory_hours = fields.Integer(string='Current inscribed', readonly=True)

   @api.depends('course_id')
   def get_semester_and_hours_from_course_id(self):
       for record in self:
           record.semester = record.course_id.subject_id.semester_id.id
           record.theory_hours = record.course_id.subject_id.theory_hours
           record.practice_hours = record.course_id.subject_id.practice_hours
