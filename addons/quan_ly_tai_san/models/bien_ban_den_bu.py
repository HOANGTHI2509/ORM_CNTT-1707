# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BienBanDenBu(models.Model):
    _name = 'bien_ban_den_bu'
    _description = 'Biên bản đền bù tài sản'
    _rec_name = 'ma_bien_ban'
    _order = 'create_date desc'

    ma_bien_ban = fields.Char(string='Mã Biên Bản', required=True, copy=False, readonly=True, default='New')
    
    nhan_vien_id = fields.Many2one('hr.employee', string='Người đền bù (Bị phạt)', required=True)
    nguoi_lap_bien_ban_id = fields.Many2one('hr.employee', string='Người lập biên bản (HR)', default=lambda self: self.env.user.employee_id.id if hasattr(self.env.user, 'employee_id') else False)
    
    tai_san_id = fields.Many2one('tai_san', string='Tài sản làm hỏng', required=True)
    tinh_trang_thiet_bi = fields.Text(string='Mô tả Tình trạng', required=True)
    so_tien_phat = fields.Float(string='Số tiền đền bù (VNĐ)')
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ Cấp trên / HR duyệt'),
        ('da_duyet', 'Đã duyệt (Chờ trừ lương)'),
        ('da_huy', 'Đã hủy')
    ], string='Trạng thái', default='nhap', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('ma_bien_ban', 'New') == 'New':
            last_record = self.search([], order='ma_bien_ban desc', limit=1)
            if last_record and last_record.ma_bien_ban.startswith('BB-'):
                last_number = int(last_record.ma_bien_ban.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ma_bien_ban'] = f'BB-{new_number:05d}'
            
        return super(BienBanDenBu, self).create(vals)

    def action_gui_duyet(self):
        for record in self:
            record.trang_thai = 'cho_duyet'

    def action_duyet(self):
        for record in self:
            record.trang_thai = 'da_duyet'
            if record.tai_san_id:
                record.tai_san_id.trang_thai = 'Hong'

    def action_huy(self):
        for record in self:
            record.trang_thai = 'da_huy'
