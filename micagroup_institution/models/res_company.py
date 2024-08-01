from odoo import models, fields, api

class ResCompany(models.Model):
   _inherit = 'res.company'
   _description = 'Company'

   value_of_unit_credit = fields.Float('Unit Credit')