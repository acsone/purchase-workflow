# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#        Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields
import openerp.addons.decimal_precision as dp


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    discount = fields.Float(
        string='Discount (%)', digits_compute=dp.get_precision('Discount'))
