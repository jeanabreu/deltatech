# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008 Deltatech All Rights Reserved
#                    Dorin Hongu <dhongu(@)gmail(.)com       
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import date, datetime
from dateutil import relativedelta

import time
from odoo.exceptions import except_orm, Warning, RedirectWarning
 
from odoo import models, fields, api, _
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo import SUPERUSER_ID, api

import odoo.addons.decimal_precision as dp


class stock_pack_operation(models.Model):
    _inherit = "stock.pack.operation"

    @api.model
    def create(self,   vals ):

        if vals.get("picking_id"):
            picking = self.env["stock.picking"].browse( vals['picking_id'])
            vals['date'] = picking.min_date  # trebuie sa fie minimul dintre data curenta si data din picking
        res_id = super(stock_pack_operation, self).create( vals)
        return res_id


class stock_quant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _quant_create_from_move(self, qty, move, lot_id=False, owner_id=False,
                                src_package_id=False, dest_package_id=False,
                                force_location_from=False, force_location_to=False):
        quant = super(stock_quant, self)._quant_create_from_move( qty, move, lot_id=lot_id, owner_id=owner_id,
                                 src_package_id=src_package_id, dest_package_id=dest_package_id,
                                 force_location_from=force_location_from, force_location_to=force_location_to)
        quant.write({'in_date': move.date})
        return quant    
    
          
                   
    
class stock_move(models.Model):
    _inherit = 'stock.move'


    @api.multi
    def write(self,vals):   
        date_fields = set(['date', 'date_expected'])
        if date_fields.intersection(vals):
            for move in self:
                today = fields.Date.today()
                if 'date' in vals:
                    if move.date_expected[:10] < today and move.date_expected < vals['date']: 
                        vals['date'] =  move.date_expected
                    if move.date[:10] < today and move.date < vals['date']:
                        vals['date'] =  move.date
                    move.quant_ids.write({'in_date':vals['date']}) 
                                         
                if 'date_expected' in vals:
                    move_date = vals.get('date',move.date)
                    if move_date[:10] < today and move_date < vals['date_expected']:
                        vals['date_expected'] =  move_date
                           
        return  super(stock_move, self).write( vals)     

 
 


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
