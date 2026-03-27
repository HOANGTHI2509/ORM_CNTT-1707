from odoo import models, fields, api

class ChiTietDatPhong(models.Model):
    _name = "chi_tiet_dat_phong"
    _description = "Chi tiết di kèm của đơn đặt phòng"

    dat_phong_id = fields.Many2one("dat_phong", string="Đơn đặt phòng", required=True, ondelete="cascade")
    
    loai_chi_tiet = fields.Selection([
        ('tai_san', 'Tài sản / Thiết bị'),
        ('dich_vu', 'Dịch vụ')
    ], string="Loại chi tiết", required=True, default='tai_san')
    
    tai_san_id = fields.Many2one("tai_san", string="Tài sản", domain=[('trang_thai', '=', 'LuuTru')])
    dich_vu_id = fields.Many2one("dich_vu_di_kem", string="Dịch vụ")
    
    so_luong = fields.Integer(string="Số lượng", default=1, required=True)
    ghi_chu = fields.Char(string="Ghi chú")
