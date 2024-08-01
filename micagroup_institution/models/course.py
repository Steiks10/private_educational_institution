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
    student_ids = fields.Many2many(comodel_name='student.student', compute='get_student_inscribed_in_the_course')
    student_grade_ids = fields.Many2many(comodel_name='course.course.grade.line', string='Students', compute='get_student_grades_of_the_course')


    def get_student_grades_of_the_course(self):
        for record in self:
            grades_in_course = self.env['course.course.grade.line'].search([('course_id', '=', record.id)])
            if grades_in_course:
                record.student_grade_ids = grades_in_course.ids
            else:
                record.student_grade_ids = False
    @api.depends('student_ids')
    def get_numbers_of_students_inscribed(self):
        for record in self:
            if record.student_ids:
                record.current_inscribed = len(record.student_ids)
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
            contracts = self.env['inscription.contract'].sudo().search(['&', ('is_paid', '=', True), ('course_ids', 'in', record.id)])
            students_inscribed = contracts.filtered(lambda c: c.is_paid).mapped('student_id')
            if students_inscribed :
                record.student_ids = students_inscribed.ids
            else:
                record.student_ids = False

    def get_course_grade_of_course(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Grades of course',
            'view_mode': 'tree,form',
            'res_model': 'course.course.grade.line',
            # 'context': "{'create': True}",
            'domain': [('course_id', '=', self.id)],
        }
    def get_evaluation_of_course(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluations of course',
            'view_mode': 'tree',
            'res_model': 'evaluation.evaluation',
            # 'context': "{'create': True}",
            'domain': [('course_id', '=', self.id)],
        }

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].sudo().next_by_code('sequence_course_private_institution')
        return super(CourseGrade, self).create(vals)


class CourseGradeLine(models.Model):
    _name = "course.course.grade.line"
    _description = "Course Grade Lines"

    course_id = fields.Many2one(comodel_name="course.course", string='Course', required=True)
    student_id = fields.Many2one(comodel_name="student.student", string='Student', required=True)
    evaluation_id = fields.Many2one(comodel_name='evaluation.evaluation', string='Evaluation', required=True) #
    score = fields.Float(string='Score')
    is_final_evaluation = fields.Boolean(string='Definitive note')

    @api.onchange('course_id')
    def _get_domain_of_student(self):
        print('hola')
        # course = self.env['course.course'].search([('id', '=', self.course_id.id)])

        domain = {
            'student_id': [('id', '=', self.course_id.student_ids.ids)],
            'evaluation_id': [('course_id', '=', self.course_id.id)]
        }
        return {'domain': domain}
        # return {'domain': {'student_id': [('id', '=', self.course_id.student_ids.ids)]}}
        # return [('id', 'in', students.ids)]
    # @api.depends('course_id')
    # def get_student_evaluations_availables(self):
    #     self.available_students_ids = self.course_id.student_ids.ids
    #     courses_ids = self.env['evaluation.evaluation'].search([('course_id', '=', self.course_id.id)])
    #     self.available_evaluation_ids = courses_ids.ids

    # @api.depends('course_id')
    # def get_evaluation_availables(self):
    #     for record in self:
    #         courses_ids = self.env['evaluation.evaluation'].search([('course_id', '=', record.course_id.id)])
    #         record.available_evaluation_ids = courses_ids.ids

    # @api.onchange('available_students_ids', 'available_evaluation_ids')
    # def _get_students_in_course(self):
    #     domain = {
    #         'student_id': [('id', '=', self.available_students_ids.ids)],
    #         'evaluation_id': [('course_id', 'in', self.available_evaluation_ids.ids)]
    #     }
    #     return {'domain': domain}


        # self.ensure_one()
        # return {'domain': {'evaluation_id': [('course_id', 'in', self.available_evaluation_ids.ids)]}}

    # @api.onchange('course_id')
    # def get_domain_for_fields_in_lines(self):
    #     # self.domain_activation = True
    #     return {'domain': {'student_id': [('id', '=', self.course_id.student_ids.ids)]}}


    # @api.onchange('course_id')
    # def get_domain_for_fields_in_lines(self):
    #     return {'domain': {'evaluation_id': [('course_id', '=', self.course_id.id)]}}