from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DotBaoDuong(models.Model):
    _name = 'dot_bao_duong'
    _description = 'Đợt bảo dưỡng tài sản'
    _rec_name = 'ten_dot_bao_duong'

    ma_dot = fields.Char(string="Mã đợt", readonly=True, copy=False, default="New")
    ten_dot_bao_duong = fields.Char(string="Tên đợt bảo dưỡng", required=True)
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc dự kiến")
    nha_cung_cap_id = fields.Many2one('nha_cung_cap', string="Đơn vị bảo dưỡng")
    chi_phi_tong = fields.Float(string="Tổng chi phí", compute="_compute_chi_phi_tong", store=True)
    
    lich_su_bao_tri_ids = fields.One2many('lich_su_bao_tri', 'dot_bao_duong_id', string="Danh sách tài sản bảo trì")

    trang_thai = fields.Selection([
        ('moi', 'Mới tạo'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành')
    ], string="Trạng thái", default='moi')

    @api.depends('lich_su_bao_tri_ids.chi_phi')
    def _compute_chi_phi_tong(self):
        for record in self:
            record.chi_phi_tong = sum(record.lich_su_bao_tri_ids.mapped('chi_phi'))

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau > record.ngay_ket_thuc:
                raise ValidationError("Ngày bắt đầu không được lớn hơn ngày kết thúc!")
                
    @api.model
    def create(self, vals):
        if vals.get('ma_dot', 'New') == 'New':
            last_record = self.search([], order='ma_dot desc', limit=1)
            if last_record and last_record.ma_dot.startswith('MNT-'):
                last_number = int(last_record.ma_dot.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ma_dot'] = f'MNT-{new_number:05d}'
        return super(DotBaoDuong, self).create(vals)

    def action_thuc_hien(self):
        for record in self:
            for item in record.lich_su_bao_tri_ids:
                item.tai_san_id.write({'trang_thai': 'BaoTri'})
            record.write({'trang_thai': 'dang_thuc_hien'})

    def action_hoan_thanh(self):
        for record in self:
            for item in record.lich_su_bao_tri_ids:
                item.tai_san_id.write({'trang_thai': 'LuuTru'})
            record.write({'trang_thai': 'hoan_thanh'})
