from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
class Contract(models.Model):
    _name = "inscription.contract"
    _inherit = ['mail.thread']
    _description = "Inscription Contract"

    name = fields.Char(string="Name", compute='get_name_according_to_student')
    is_paid = fields.Boolean(string="Is paid", default=False, compute='get_payment_state')
    code = fields.Char(string='Code', readonly=True)
    credits = fields.Integer(string='Credits', compute='compute_credits_and_hours_according_to_courses')
    theory_hours = fields.Integer(string='Theory Hours', readonly=True)
    practice_hours = fields.Integer(string='Practice Hours', readonly=True)
    student_id = fields.Many2one(comodel_name='student.student', string='Student', required=False)
    # student_contract_id = fields.Many2one(comodel_name='student.student', string)
    course_ids = fields.Many2many(comodel_name='course.course', string='Courses')

    @api.depends('student_id')
    def get_name_according_to_student(self):
        for record in self:
            if record.student_id:
                record.name = f"Contract for {record.student_id.name}"
            else:
                record.name = False
                print(record)

    @api.depends('course_ids')
    def compute_credits_and_hours_according_to_courses(self):
        for record in self:
            record.credits = sum([course.subject_id.credits for course in record.course_ids])
            record.theory_hours = sum([course.subject_id.theory_hours for course in record.course_ids])
            record.practice_hours = sum([course.subject_id.practice_hours for course in record.course_ids])


    def check_if_exists_the_contract_for_this_student(self, course_id):
        inscription_contract = self.env['inscription.contract'].sudo().search(['&', ('course_id', '=', course_id), ('is_paid', '=', True)])
        if inscription_contract:
            return True
        else:
            return False
    def action_payment_inscription_contract(self):
        str_msg = ''
        for record in self:
            if not record.course_ids:
                raise ValidationError(f'You cannot pay the contract, you need to add a course')
            for course in record.course_ids:
                if course.current_inscribed == course.limit_students:
                    str_msg += f"The course {course.name} is full.\n"
        if str_msg:
            raise ValidationError(f'You cannot pay the contract due to the following: \n {str_msg}')
        else:
            if record.student_id.state != 'registered':
                raise ValidationError('The student must be registered to pay the contract.')
            else:
                lines = []
                # config = self.env['ir.config_parameter'].sudo().get_param('private_institution.value_of_unit_credit')
                lines.append((0, 0, {
                    'product_id': (self.env['product.product'].search([('name', '=', "Inscription")])).id,
                    'quantity': 1,
                    'price_unit': record.credits * self.env.company.value_of_unit_credit,
                    'tax_ids': False,
                }))

                bill = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'journal_id': (self.env['account.journal'].sudo().search([('name', '=', "Customer Invoices")], limit=1)).id,
                    'partner_id': (self.env['res.partner'].sudo().search([('user_ids', '=', record.student_id.res_user_id.id)], limit=1)).id,
                    'contract_id': record.id,
                    'invoice_date': datetime.now(),
                    'line_ids': lines
                })
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Bill',
                    'res_model': 'account.move',
                    # 'res_id': bl_object.id,
                    'view_mode': 'tree,form',
                    'domain': [('id', '=', bill.id)],
                }

    def get_payment_state(self):
        for record in self:
            account = self.env['account.move'].sudo().search([('payment_state', '=', 'paid'), ('contract_id', '=', record.id)], limit=1)
            if account:
                record.is_paid = True
            else:
                record.is_paid = False

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].sudo().next_by_code('sequence_contract_private_institution')
        return super(Contract, self).create(vals)



