from odoo import models, fields

class TaiSan(models.Model):
    _inherit = 'tai_san'
    
    phong_id = fields.Many2one('quan_ly_phong_hop', string="Thuộc phòng họp (Cố định)", help="Nếu tài sản này được gắn cố định vào một phòng họp cụ thể.")
