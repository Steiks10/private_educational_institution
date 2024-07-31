from odoo import models, fields, api

class ResConfig(models.TransientModel):
   _inherit = ['res.config.settings']

   value_of_unit_credit = fields.Float(string='Unit Credit', related='company_id.value_of_unit_credit', readonly=False)
