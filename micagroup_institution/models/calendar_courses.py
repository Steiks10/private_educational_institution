from odoo import models, fields, api

class CalendarCourses(models.Model):
   _inherit = 'calendar.event'
   _description = 'Calendar Courses'

   course_id = fields.Many2one(comodel_name='course.course', string='course')
   teacher_name = fields.Char(related='course_id.name', string='Teacher')
   code = fields.Char(related='course_id.code', string='Code')
   semester = fields.Char(compute='get_semester_from_course_id', string='Semester')
   limit_students = fields.Integer(related='course_id.limit_students', string='Max capacity')
   current_inscribed = fields.Integer(related='course_id.current_inscribed', string='Current inscribed')

   def get_semester_from_course_id(self):
       for record in self:
           record.semester = record.course_id.subject_id.semester