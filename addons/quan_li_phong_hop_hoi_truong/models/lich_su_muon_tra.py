from odoo import models, fields, api
from datetime import datetime, timedelta

class LichSuMuonTra(models.Model):
    _name = "lich_su_muon_tra"
    _description = "Lịch sử sử dụng phòng họp"
    _order = "ngay_su_dung desc, phong_id asc"

    ngay_su_dung = fields.Date(string="📅 Ngày", required=True, default=fields.Date.today)
    phong_id = fields.Many2one("quan_ly_phong_hop", string="🏢 Phòng", required=True)    
    dat_phong_id = fields.Many2one('dat_phong', string='Phiếu Đặt Phòng', ondelete='cascade')
    ma_phieu = fields.Char(related='dat_phong_id.ma_phieu', string="Mã Phiếu", store=True)
    nguoi_muon_id = fields.Many2one('hr.employee', related='dat_phong_id.nguoi_muon_id', string="Người mượn", store=True)
    tai_san_ids = fields.Many2many("tai_san", related="dat_phong_id.tai_san_ids", string="Tài sản mượn kèm")
    dich_vu_ids = fields.Many2many("quan_ly_dich_vu", related="dat_phong_id.dich_vu_ids", string="Dịch vụ đi kèm")
    tong_thoi_gian_su_dung = fields.Char(string="⏳ Tổng thời gian sử dụng", compute="_compute_tong_thoi_gian", store=True)



    @api.depends("dat_phong_id", "ngay_su_dung")
    def _compute_tong_thoi_gian(self):
        """ Tính tổng thời gian sử dụng phòng theo giờ:phút:giây """
        for record in self:
            if not record.dat_phong_id:
                record.tong_thoi_gian_su_dung = "00:00:00"
                continue
            
            usage = record.dat_phong_id
            if usage.thoi_gian_muon_thuc_te and usage.thoi_gian_tra_thuc_te:
                delta = usage.thoi_gian_tra_thuc_te - usage.thoi_gian_muon_thuc_te
                total_seconds = delta.total_seconds()
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                record.tong_thoi_gian_su_dung = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            else:
                record.tong_thoi_gian_su_dung = "00:00:00"

    @api.model
    def update_lich_su_muon_tra(self):
        """ Cập nhật dữ liệu lịch sử mượn trả mỗi khi có phòng được trả """
        today = fields.Date.today()
        dat_phong_records = self.env["dat_phong"].search([("trang_thai", "=", "đã_trả"), ("thoi_gian_tra_thuc_te", "!=", False)])

        # Tạo danh sách chứa các bản ghi lịch sử theo ngày và phòng
        data_to_create = {}

        for record in dat_phong_records:
            ngay_muon = record.thoi_gian_muon_thuc_te.date()
            ngay_tra = record.thoi_gian_tra_thuc_te.date()

            for date in (ngay_muon + timedelta(days=n) for n in range((ngay_tra - ngay_muon).days + 1)):
                key = (date, record.phong_id.id, record.id)
                
                if key not in data_to_create:
                    data_to_create[key] = {
                        "ngay_su_dung": date,
                        "phong_id": record.phong_id.id,
                        "dat_phong_id": record.id,
                    }
        
        # Xóa lịch sử cũ và cập nhật mới
        self.env["lich_su_muon_tra"].search([]).unlink()
        for data in data_to_create.values():
            self.create(data)
