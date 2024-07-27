from odoo import models, fields, api

class AccountMove(models.Model):
   _inherit = 'account.move'
   _description = 'Account Moves'

   contract_id = fields.Many2one(comodel_name='inscription.contract', string='Inscription contract')
