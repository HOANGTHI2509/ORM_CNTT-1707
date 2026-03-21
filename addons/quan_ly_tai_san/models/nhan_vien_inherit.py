# -*- coding: utf-8 -*-
from odoo import models, fields

class NhanVien(models.Model):
    _inherit = 'nhan_vien'

    phieu_ban_giao_ids = fields.One2many(
        comodel_name='phieu_ban_giao',
        inverse_name='nguoi_nhan_id',
        string="Lịch sử nhận/trả tài sản",
    )

    def write(self, vals):
        res = super(NhanVien, self).write(vals)
        if 'trang_thai_lam_viec' in vals and vals['trang_thai_lam_viec'] == 'nghi_viec':
            for record in self:
                assets = self.env['tai_san'].search([
                    ('nguoi_dang_dung_id', '=', record.id),
                    ('trang_thai', '=', 'Muon')
                ])
                if assets:
                    lines = [(0, 0, {
                        'tai_san_id': asset.id,
                        'tinh_trang': asset.trang_thai_kiem_ke or 'binh_thuong',
                        'ghi_chu': 'Hệ thống tự động tạo do nhân viên nghỉ việc'
                    }) for asset in assets]
                    
                    admin = self.env['nhan_vien'].search([], limit=1)
                    nguoi_nhan_id = admin.id if admin else record.id
                    if hasattr(self.env.user, 'employee_id') and self.env.user.employee_id:
                        nguoi_nhan_id = self.env.user.employee_id.id
                        
                    self.env['phieu_ban_giao'].create({
                        'loai_phieu': 'thu_hoi',
                        'nguoi_giao_id': record.id,
                        'nguoi_nhan_id': nguoi_nhan_id,
                        'chi_tiet_ids': lines,
                        'trang_thai': 'nhap',
                    })
        return res
