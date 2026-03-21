from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PhieuBanGiao(models.Model):
    _name = 'phieu_ban_giao'
    _description = 'Phiếu bàn giao / thu hồi tài sản'
    _rec_name = 'ma_phieu'
    _order = 'ngay_ban_giao desc'

    ma_phieu = fields.Char(string="Mã phiếu", default="New", readonly=True, copy=False)
    loai_phieu = fields.Selection([
        ('giao_moi', 'Bàn giao tài sản'),
        ('thu_hoi', 'Thu hồi tài sản')
    ], string="Loại phiếu", required=True, default='giao_moi')
    
    ngay_ban_giao = fields.Date(string="Ngày thực hiện", required=True, default=fields.Date.context_today)
    
    nguoi_giao_id = fields.Many2one('nhan_vien', string="Người giao", required=True)
    nguoi_nhan_id = fields.Many2one('nhan_vien', string="Người nhận", required=True)
    
    chi_tiet_ids = fields.One2many('chi_tiet_ban_giao', 'phieu_id', string="Chi tiết tài sản")

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Đã Hủy')
    ], string="Trạng thái", default='nhap')

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            last_record = self.search([], order='ma_phieu desc', limit=1)
            if last_record and last_record.ma_phieu.startswith('PBG-'):
                last_number = int(last_record.ma_phieu.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ma_phieu'] = f'PBG-{new_number:05d}'
        return super(PhieuBanGiao, self).create(vals)

    def action_hoan_thanh(self):
        for record in self:
            if not record.chi_tiet_ids:
                raise ValidationError("Vui lòng thêm ít nhất 1 tài sản vào phiếu!")
                
            for chi_tiet in record.chi_tiet_ids:
                if record.loai_phieu == 'giao_moi':
                    chi_tiet.tai_san_id.write({
                        'trang_thai': 'Muon',
                        'nguoi_dang_dung_id': record.nguoi_nhan_id.id
                    })
                else: # Thu hồi
                    chi_tiet.tai_san_id.write({
                        'trang_thai': 'LuuTru',
                        'nguoi_dang_dung_id': False
                    })
            record.write({'trang_thai': 'hoan_thanh'})

    def action_huy(self):
        self.write({'trang_thai': 'huy'})


class ChiTietBanGiao(models.Model):
    _name = 'chi_tiet_ban_giao'
    _description = 'Chi tiết phiếu bàn giao'

    phieu_id = fields.Many2one('phieu_ban_giao', string="Phiếu bàn giao", ondelete='cascade')
    tai_san_id = fields.Many2one('tai_san', string="Tài sản", required=True)
    tinh_trang = fields.Selection([
        ('binh_thuong', 'Bình thường'),
        ('hong_hoc', 'Hỏng hóc'),
        ('mat', 'Mất')
    ], string="Tình trạng", default='binh_thuong')
    ghi_chu = fields.Char(string="Ghi chú")
