# -*- coding: utf-8 -*-
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    job_position_id = fields.Many2one(
        "res.partner.job_position",
        "Categorized job position",
        oldname="job_position")
    representer_ids = fields.Many2one(
        )

    @api.model
    def _commercial_fields(self):
        """Add company_ids to the commercial fields that will be synced with
         childs. Ideal would be that this field is isolated from company field,
         but it involves a lot of development (default value, incoherences
         parent/child...).
        :return: List of field names to be synced.
        """
        fields = super(ResPartner, self)._commercial_fields()
        fields += ['representer_ids']
        return fields


class ResPartnerJobPosition(models.Model):
    _name = "res.partner.job_position"
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Job position"

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one(
        "res.partner.job_position",
        "Parent", ondelete='restrict')
    child_ids = fields.One2many(
        "res.partner.job_position",
        "parent_id",
        "Children",
        oldname="children")
    type = fields.Selection( [('representing','Person Responsible Representing'), ('warehouseman','Person Responsible Warehouse'), ('accountant','Person Responsible Accountant'), ('other','Other Responsible Person')], 'Type of job position', required=True)

    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    
