from odoo import models, fields, api

class QuanLyPhongHop(models.Model):
    _name = "quan_ly_phong_hop"
    _description = "Quản lý phòng họp, hội trường"

    name = fields.Char(string="Tên phòng họp", required=True)
    hinh_anh = fields.Image(string="Hình ảnh phòng")

    suc_chua = fields.Integer(string="Sức chứa")
    
    loai_phong = fields.Selection([
        ('phong_hop_nho', 'Phòng họp nhỏ'),
        ('hoi_truong_lon', 'Hội trường lớn')
    ], string="Loại phòng", default='phong_hop_nho', required=True)

    trang_thai = fields.Selection([
        ("Trống", "Trống"),
        ("Đã_mượn", "Đã mượn"),
        ("Đang_sử_dụng", "Đang sử dụng"),
    ], string="Trạng thái", compute="_compute_trang_thai")

    vi_tri_id = fields.Many2one('vi_tri', string="Vị trí vật lý (Tự động tạo)", readonly=True)
    dat_phong_ids = fields.One2many("dat_phong", "phong_id", string="Lịch sử mượn phòng")
    
    thiet_bi_ids = fields.One2many(
        comodel_name="tai_san",
        compute="_compute_thiet_bi_ids",
        string="Thiết bị trong phòng (Lấy từ Kho)",
        readonly=True
    )
    
    def _compute_thiet_bi_ids(self):
        for record in self:
            if record.vi_tri_id:
                record.thiet_bi_ids = self.env['tai_san'].search([('vi_tri_hien_tai_id', '=', record.vi_tri_id.id)])
            else:
                record.thiet_bi_ids = False

    # Chỉ hiển thị các trạng thái "Đã duyệt" và "Đang sử dụng"
    lich_dat_phong_ids = fields.One2many(
        "dat_phong", "phong_id",
        string="Lịch đặt phòng",
        domain=[("trang_thai", "in", ["cho_duyet_cap_2", "đã_duyệt", "đang_sử_dụng"])]
    )

    # Lịch sử mượn trả (Chỉ hiển thị các trạng thái "Đã trả")
    lich_su_thay_doi_ids = fields.One2many(
        "dat_phong", "phong_id",
        string="Lịch sử mượn trả",
        domain=[("trang_thai", "=", "đã_trả")]
    )

    @api.depends("dat_phong_ids.trang_thai")
    def _compute_trang_thai(self):
        for record in self:
            trang_thai_dat_phong = record.dat_phong_ids.filtered(lambda r: r.trang_thai in ["cho_duyet_cap_2", "đã_duyệt", "đang_sử_dụng"])
            trang_thai_dang_su_dung = record.dat_phong_ids.filtered(lambda r: r.trang_thai == "đang_sử_dụng")
            trang_thai_da_huy_da_tra = record.dat_phong_ids.filtered(lambda r: r.trang_thai in ["đã_hủy", "đã_trả"])

            if trang_thai_dang_su_dung:
                record.trang_thai = "Đang_sử_dụng"
            elif trang_thai_dat_phong:
                record.trang_thai = "Đã_mượn"
            elif trang_thai_da_huy_da_tra:
                record.trang_thai = "Trống"
            else:
                record.trang_thai = "Trống"

    @api.model
    def create(self, vals):
        res = super(QuanLyPhongHop, self).create(vals)
        # Tự động tạo 1 vị trí VẬT LÝ bên phân hệ Vị trí tải sản khi tạo phòng họp
        vi_tri_moi = self.env['vi_tri'].create({'ten_vi_tri': f"Phòng họp: {res.name}"})
        res.write({'vi_tri_id': vi_tri_moi.id})
        return res

    def write(self, vals):
        res = super(QuanLyPhongHop, self).write(vals)
        for record in self:
            # FIX CHO CÁC PHÒNG CŨ: Nếu phòng chưa có vi_tri_id (do tạo từ trước khi có code auto-sync), thì tạo bù
            if not record.vi_tri_id:
                vi_tri_moi = self.env['vi_tri'].create({'ten_vi_tri': f"Phòng họp: {record.name}"})
                record.vi_tri_id = vi_tri_moi.id

            # Cập nhật tên vị trí nếu đổi tên phòng
            if 'name' in vals and record.vi_tri_id:
                record.vi_tri_id.update({'ten_vi_tri': f"Phòng họp: {record.name}"})
        return res
