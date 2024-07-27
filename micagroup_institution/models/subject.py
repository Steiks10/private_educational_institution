from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta

# semester_order_map = {
#   'first_semester': 1,
#   'second_semester': 2,
#   'third_semester': 3,
#   'fourth_semester': 4,
#   'fifth_semester': 5,
#   'sixth_semester': 6,
#   'seventh_semester': 7,
#   'eighth_semester': 8,
#   'nineth_semester': 9,
#   'tenth_semester': 10,
# }
class Subject(models.Model):
    _name = "subject.subject"
    _inherit = ['mail.thread']
    _description = "Subject"

    name = fields.Char(string="Name", required=True)
    is_active = fields.Boolean(string="Is Active", required=True)
    code = fields.Char(string='Code', readonly=True)
    credits = fields.Integer(string='Credits', required=True)
    theory_hours = fields.Integer(string='Theory Hours')
    practice_hours = fields.Integer(string='Practice Hours')
    # semester = fields.Selection(selection=[
    #     ('first_semester', 'First semester'),
    #     ('second_semester', 'Second semester'),
    #     ('third_semester', 'Third semester'),
    #     ('fourth_semester', 'Fourth semester'),
    #     ('fifth_semester', 'Fifth semester'),
    #     ('sixth_semester', 'Sixth semester'),
    #     ('seventh_semester', 'Seventh semester'),
    #     ('eighth_semester', 'Eighth semester'),
    #     ('nineth_semester', 'Ninth semester'),
    #     ('tenth_semester', 'Tenth semester'),
    # ], string='Semester', required=True)
    semester_id = fields.Many2one(comodel_name='semester.semester', string='Semester')
    career_id = fields.Many2one(comodel_name='career.career',  string='Career')
    image = fields.Image(string='Imagen')
    # sequence = fields.Integer(string='sequence', compute="_compute_semester_order")

    # @api.depends('semester')
    # def _compute_semester_order(self):
    #     for record in self:
    #         semester = record.semester
    #         record.sequence = semester_order_map.get(semester, 0)


    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].sudo().next_by_code('sequence_subject_private_institution')
        subject =  super(Subject, self).create(vals)
        return subject
