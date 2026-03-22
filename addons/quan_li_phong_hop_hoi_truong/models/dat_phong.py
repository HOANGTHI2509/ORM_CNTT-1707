from odoo import models, fields, api, exceptions
from datetime import datetime
import logging
import requests

_logger = logging.getLogger(__name__)

# ================= CẤU HÌNH TELEGRAM API =================
TELEGRAM_BOT_TOKEN = "8674994673:AAGry6psZQjjR1EMXcXprIEevecQ6Ur4Ei0"
TELEGRAM_CHAT_ID = "8262831605"

def gui_tin_nhan_telegram(message):
    if "THAY_" in TELEGRAM_BOT_TOKEN or "THAY_" in TELEGRAM_CHAT_ID:
        _logger.warning("Chưa cấu hình Telegram Token hoặc Chat ID. Bỏ qua gửi tin nhắn.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}, timeout=5)
    except Exception as e:
        _logger.error("Lỗi gửi Telegram: %s", str(e))
# ==========================================================

_logger.info("DEBUG: Module dat_phong.py ĐÃ ĐƯỢC LOAD")

class DatPhong(models.Model):
    _name = "dat_phong"
    _description = "Đăng ký mượn phòng"

    phong_id = fields.Many2one("quan_ly_phong_hop", string="Phòng họp", required=True)
    ma_phieu = fields.Char(string="Mã Đặt Phòng", required=True, copy=False, readonly=True, default="New")
    nguoi_muon_id = fields.Many2one("hr.employee", string="Người mượn", required=True)  
    email = fields.Char(string="Email nhận thông báo", required=True, help="Vui lòng nhập email @gmail.com")
    thoi_gian_muon_du_kien = fields.Datetime(string="Thời gian mượn dự kiến", required=True)
    thoi_gian_muon_thuc_te = fields.Datetime(string="Thời gian mượn thực tế")
    thoi_gian_tra_du_kien = fields.Datetime(string="Thời gian trả dự kiến", required=True)

    thoi_gian_tra_thuc_te = fields.Datetime(string="Thời gian trả thực tế")
    so_luong = fields.Integer(string="Số lượng", default=1)

    # Liên kết với tài sản (Shared Resource)
    tai_san_ids = fields.Many2many(
        comodel_name="tai_san",
        relation="dat_phong_tai_san_rel",
        column1="dat_phong_id",
        column2="tai_san_id",
        string="Tài sản mượn kèm",
        domain=[('trang_thai', '=', 'LuuTru')]
    )
    
    dich_vu_ids = fields.Many2many(
        comodel_name="dich_vu_di_kem",
        string="Dịch vụ đi kèm"
    )

    kieu_lap = fields.Selection([
        ('khong_lap', 'Không lặp'),
        ('hang_ngay', 'Hàng ngày'),
        ('hang_tuan', 'Hàng tuần'),
        ('hang_thang', 'Hàng tháng')
    ], string="Lặp lại", default='khong_lap', required=True)
    
    ngay_ket_thuc_lap = fields.Date(string="Kết thúc lặp")

    @api.onchange('nguoi_muon_id')
    def _onchange_nguoi_muon_id(self):
        if self.nguoi_muon_id:
            self.email = self.nguoi_muon_id.work_email

    @api.constrains('email')
    def _check_email_gmail(self):
        for record in self:
            if record.email and not record.email.endswith('@gmail.com'):
                raise exceptions.ValidationError("Email nhận thông báo không hợp lệ. Vui lòng sử dụng địa chỉ @gmail.com.")

    @api.constrains('so_luong', 'phong_id')
    def _check_suc_chua(self):
        for record in self:
            if record.phong_id and record.so_luong > record.phong_id.suc_chua:
                raise exceptions.ValidationError(f"Phòng này chỉ chứa được tối đa {record.phong_id.suc_chua} người!")

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            last_record = self.search([('ma_phieu', '=like', 'DP-%')], order='ma_phieu desc', limit=1)
            if last_record:
                last_number = int(last_record.ma_phieu.replace('DP-', ''))
                vals['ma_phieu'] = f'DP-{last_number + 1:05d}'
            else:
                vals['ma_phieu'] = 'DP-00001'

        # Tạo bản ghi gốc
        record = super(DatPhong, self).create(vals)
        
        # Xử lý logic tạo các bản ghi lặp lại
        if vals.get('kieu_lap') and vals.get('kieu_lap') != 'khong_lap' and vals.get('ngay_ket_thuc_lap'):
            record.tao_ban_ghi_lap_lai()
            
        # Gửi thông báo Telegram khi có người vừa đăng ký
        if record.nguoi_muon_id and record.phong_id and record.thoi_gian_muon_du_kien and record.thoi_gian_tra_du_kien:
            tele_msg = f"🆕 <b>YÊU CẦU ĐẶT PHÒNG MỚI ({record.ma_phieu})</b>\nPhòng: {record.phong_id.name}\nNgười mượn: {record.nguoi_muon_id.display_name}\nThời gian: {record.thoi_gian_muon_du_kien.strftime('%H:%M %d/%m')} - {record.thoi_gian_tra_du_kien.strftime('%H:%M %d/%m')}\nTrạng thái: Chờ duyệt"
            gui_tin_nhan_telegram(tele_msg)
            
        return record

    def tao_ban_ghi_lap_lai(self):
        self.ensure_one()
        from dateutil.relativedelta import relativedelta
        import datetime
        
        start_date = self.thoi_gian_muon_du_kien
        end_date = self.thoi_gian_tra_du_kien
        repeat_until = self.ngay_ket_thuc_lap
        
        if not start_date or not end_date or not repeat_until:
            return

        current_start = start_date
        current_end = end_date
        
        while True:
            # Tính toán thời gian tiếp theo
            if self.kieu_lap == 'hang_ngay':
                delta = relativedelta(days=1)
            elif self.kieu_lap == 'hang_tuan':
                delta = relativedelta(weeks=1)
            elif self.kieu_lap == 'hang_thang':
                delta = relativedelta(months=1)
            else:
                break
                
            current_start += delta
            current_end += delta
            
            # Kiểm tra điều kiện dừng
            if current_start.date() > repeat_until:
                break
                
            # Tạo bản ghi mới (copy từ bản ghi gốc)
            self.copy({
                'thoi_gian_muon_du_kien': current_start,
                'thoi_gian_tra_du_kien': current_end,
                'kieu_lap': 'khong_lap', # Bản ghi con không lặp tiếp
                'ngay_ket_thuc_lap': False,
                'trang_thai': 'chờ_duyệt'
            })

    trang_thai = fields.Selection([
        ("chờ_duyệt", "Chờ duyệt"),
        ("cho_duyet_cap_2", "Chờ Lãnh đạo duyệt"),
        ("đã_duyệt", "Đã duyệt"),
        ("đang_sử_dụng", "Đang sử dụng"),
        ("đã_hủy", "Đã hủy"),
        ("đã_trả", "Đã trả")
    ], string="Trạng thái", default="chờ_duyệt")

    lich_su_ids = fields.One2many("lich_su_thay_doi", "dat_phong_id", string="Lịch sử mượn trả")

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.ma_phieu}] {record.phong_id.name} - Người mượn: {record.nguoi_muon_id.display_name}"
            result.append((record.id, name))
        return result

    bien_ban_ids = fields.One2many("bien_ban_den_bu", "dat_phong_id", string="Biên Bản Phạt/Đền Bù")

    def action_lap_bien_ban(self):
        self.ensure_one()
        return {
            'name': 'Lập Biên Bản Đền Bù',
            'type': 'ir.actions.act_window',
            'res_model': 'bien_ban_den_bu',
            'view_mode': 'form',
            'context': {
                'default_dat_phong_id': self.id,
            },
            'target': 'current'
        }

    def _gui_thong_bao_email(self, email_to, subject, message):
        """ Hàm phụ trợ để gửi thông báo Email đơn giản """
        _logger.info("DEBUG: Khởi động _gui_thong_bao_email cho %s", email_to if email_to else "None")
        if email_to:
            _logger.info("DEBUG: Đang tạo bản ghi Email cho: %s", email_to)
            formatted_message = message.replace("\n", "<br/>")
            mail_values = {
                'subject': subject,
                'body_html': f'<div style="font-family: sans-serif;">{formatted_message}</div>',
                'email_to': email_to,
            }
            try:
                mail = self.env['mail.mail'].create(mail_values)
                _logger.info("DEBUG: Đã tạo mail.mail ID: %s", mail.id)
                mail.send()
                _logger.info("============== BẮN THÔNG BÁO EMAIL ==================")
                _logger.info("Tới Email: %s", email_to)
                _logger.info("Tiêu đề: %s", subject)
                _logger.info("=====================================================")
            except Exception as e:
                _logger.error("DEBUG: Lỗi khi tạo/gửi Email: %s", str(e))
        else:
            _logger.warning("Không thể gửi Email vì thiếu địa chỉ Email")


    def xac_nhan_duyet_phong(self):
        """ Xác nhận duyệt phòng và tự động hủy các yêu cầu bị trùng thời gian (cùng phòng hoặc khác phòng) """
        for record in self:
            _logger.info("DEBUG: Chạy xac_nhan_duyet_phong cho bản ghi ID: %s, Trạng thái: %s", record.id, record.trang_thai)
            if record.trang_thai != "chờ_duyệt":
                raise exceptions.UserError("Chỉ có thể duyệt yêu cầu có trạng thái 'Chờ duyệt'.")
            
            # Kiểm tra xung đột tài sản
            for asset in record.tai_san_ids:
                if asset.trang_thai != 'LuuTru':
                     raise exceptions.UserError(f"Tài sản {asset.ten_tai_san} đang không sẵn sàng (Trạng thái: {asset.trang_thai}).")

            # Duyệt yêu cầu hiện tại
            ghi_chu_log = ""
            if record.phong_id.loai_phong == 'hoi_truong_lon':
                _logger.info("DEBUG: Chuyển sang cho_duyet_cap_2 (Hội trường lớn)")
                record.write({"trang_thai": "cho_duyet_cap_2"})
            else:
                _logger.info("DEBUG: Duyệt thành công (Phòng họp nhỏ)")
                record.write({"trang_thai": "đã_duyệt"})
                
                # Thu thập thông tin đồ đã mượn
                assets_str = ", ".join(record.tai_san_ids.mapped('ten_tai_san')) if record.tai_san_ids else "Không có đồ mượn kèm"
                dich_vu_str = ", ".join(record.dich_vu_ids.mapped('name')) if record.dich_vu_ids else "Không có dịch vụ đi kèm"
                
                # Xây dựng nội dung thông báo chi tiết
                msg = (f"✅ Yêu cầu mượn phòng {record.phong_id.name} đã được duyệt thành công!\n"
                       f"⏰ Thời gian: {record.thoi_gian_muon_du_kien.strftime('%H:%M %d/%m')} - {record.thoi_gian_tra_du_kien.strftime('%H:%M %d/%m')}\n"
                       f"📦 Đồ dùng kèm theo: {assets_str}\n"
                       f"🛠 Dịch vụ đi kèm: {dich_vu_str}")
                
                # Gửi thông báo Email
                _logger.info("DEBUG: Chuẩn bị gửi thông báo Duyệt cấp 1")
                self._gui_thong_bao_email(record.email, f"Thông báo duyệt phòng: {record.phong_id.name}", msg)
                ghi_chu_log = f"Đã gửi Email thông báo duyệt phòng tới {record.email}"
                
                # Gửi thông báo Telegram
                tele_msg = f"✅ <b>ĐẶT PHÒNG THÀNH CÔNG</b>\nPhòng: {record.phong_id.name}\nNgười mượn: {record.nguoi_muon_id.display_name}\nThời gian: {record.thoi_gian_muon_du_kien.strftime('%H:%M %d/%m')} - {record.thoi_gian_tra_du_kien.strftime('%H:%M %d/%m')}"
                gui_tin_nhan_telegram(tele_msg)
            
            self.lich_su(record, ghi_chu=ghi_chu_log)

    def xac_nhan_duyet_cap_2(self):
        for record in self:
            _logger.info("DEBUG: Chạy xac_nhan_duyet_cap_2 cho bản ghi ID: %s", record.id)
            if record.trang_thai != "cho_duyet_cap_2":
                raise exceptions.UserError("Chỉ có thể duyệt yêu cầu đang chờ cấp 2 duyệt.")
            
            record.write({"trang_thai": "đã_duyệt"})

            # Thu thập thông tin đồ đã mượn
            assets_str = ", ".join(record.tai_san_ids.mapped('ten_tai_san')) if record.tai_san_ids else "Không có đồ mượn kèm"
            dich_vu_str = ", ".join(record.dich_vu_ids.mapped('name')) if record.dich_vu_ids else "Không có dịch vụ đi kèm"
            
            # Xây dựng nội dung thông báo chi tiết
            msg = (f"✅ Yêu cầu mượn hội trường {record.phong_id.name} của bạn đã được Lãnh đạo duyệt thành công!\n"
                   f"⏰ Thời gian: {record.thoi_gian_muon_du_kien.strftime('%H:%M %d/%m')} - {record.thoi_gian_tra_du_kien.strftime('%H:%M %d/%m')}\n"
                   f"📦 Đồ dùng kèm theo: {assets_str}\n"
                   f"🛠 Dịch vụ đi kèm: {dich_vu_str}")
            
            # Gửi thông báo Email
            _logger.info("DEBUG: Chuẩn bị gửi thông báo Duyệt cấp 2")
            self._gui_thong_bao_email(record.email, f"Thông báo duyệt hội trường: {record.phong_id.name}", msg)
            
            # Gửi thông báo Telegram
            tele_msg = f"✅ <b>DUYỆT HỘI TRƯỜNG CẤP 2 THÀNH CÔNG</b>\nPhòng: {record.phong_id.name}\nNgười mượn: {record.nguoi_muon_id.display_name}\nThời gian: {record.thoi_gian_muon_du_kien.strftime('%H:%M %d/%m')} - {record.thoi_gian_tra_du_kien.strftime('%H:%M %d/%m')}"
            gui_tin_nhan_telegram(tele_msg)

            self.lich_su(record, ghi_chu=f"Đã gửi Email thông báo Lãnh đạo duyệt tới {record.email}")

            # Logic hủy các yêu cầu trùng (đã copy từ trên xuống để đảm bảo chạy khi duyệt chính thức)
            # Hủy các yêu cầu cùng phòng có thời gian trùng lặp
            cung_phong_trung_thoi_gian = [
                ('phong_id', '=', record.phong_id.id),
                ('id', '!=', record.id),
                ('trang_thai', 'in', ['chờ_duyệt', 'cho_duyet_cap_2']),
                ('thoi_gian_muon_du_kien', '<', record.thoi_gian_tra_du_kien),
                ('thoi_gian_tra_du_kien', '>', record.thoi_gian_muon_du_kien)
            ]
            xu_li_cung_phong_trung_thoi_gian = self.search(cung_phong_trung_thoi_gian)
            for other in xu_li_cung_phong_trung_thoi_gian:
                other.write({"trang_thai": "đã_hủy"})
                # Gửi thông báo hủy cho người bị trùng
                msg_cancel = f"⚠️ Yêu cầu mượn phòng {other.phong_id.name} của bạn đã tự động bị hủy do trùng lịch với người khác."
                self._gui_thong_bao_email(other.email, f"Thông báo hủy đặt phòng: {other.phong_id.name}", msg_cancel)
                self.lich_su(other, ghi_chu=f"Tự động hủy và gửi Email thông báo tới {other.email}")


            # Hủy các yêu cầu cùng phòng có thời gian trùng lặp
            cung_phong_trung_thoi_gian = [
                ('phong_id', '=', record.phong_id.id),
                ('id', '!=', record.id),
                ('trang_thai', '=', 'chờ_duyệt'),
                ('thoi_gian_muon_du_kien', '<', record.thoi_gian_tra_du_kien),
                ('thoi_gian_tra_du_kien', '>', record.thoi_gian_muon_du_kien)
            ]
            xu_li_cung_phong_trung_thoi_gian = self.search(cung_phong_trung_thoi_gian)
            for other in xu_li_cung_phong_trung_thoi_gian:
                other.write({"trang_thai": "đã_hủy"})
                msg_cancel = f"⚠️ Yêu cầu mượn phòng {other.phong_id.name} của bạn đã tự động bị hủy do trùng lịch với người khác."
                self._gui_thong_bao_email(other.email, f"Thông báo hủy đặt phòng: {other.phong_id.name}", msg_cancel)
                self.lich_su(other, ghi_chu=f"Tự động hủy và gửi Email thông báo tới {other.email}")

            # Hủy các yêu cầu khác phòng nhưng của cùng một người mượn nếu bị trùng thời gian
            khac_phong_trung_thoi_gian = [
                ('nguoi_muon_id', '=', record.nguoi_muon_id.id),
                ('id', '!=', record.id),
                ('trang_thai', '=', 'chờ_duyệt'),
                ('thoi_gian_muon_du_kien', '<', record.thoi_gian_tra_du_kien),
                ('thoi_gian_tra_du_kien', '>', record.thoi_gian_muon_du_kien)
            ]
            xu_li_khac_phong_trung_thoi_gian = self.search(khac_phong_trung_thoi_gian)
            for other in xu_li_khac_phong_trung_thoi_gian:
                other.write({"trang_thai": "đã_hủy"})
                msg_cancel = f"⚠️ Yêu cầu mượn phòng {other.phong_id.name} của bạn đã tự động bị hủy do thời gian yêu cầu trùng với lịch của bạn đã được duyệt ở phòng khác."
                self._gui_thong_bao_email(other.email, f"Thông báo hủy đặt phòng: {other.phong_id.name}", msg_cancel)
                self.lich_su(other, ghi_chu=f"Tự động hủy và gửi Email thông báo tới {other.email}")

    def huy_muon_phong(self):
        """ Hủy đăng ký mượn phòng """
        for record in self:
            if record.trang_thai != "chờ_duyệt":
                raise exceptions.UserError("Chỉ có thể hủy yêu cầu có trạng thái 'Chờ duyệt'.")
            record.write({"trang_thai": "đã_hủy"})
            self.lich_su(record)
            
            # Telegram
            tele_msg = f"❌ <b>HỦY ĐẶT PHÒNG</b>\nPhòng: {record.phong_id.name}\nNgười mượn: {record.nguoi_muon_id.display_name}"
            gui_tin_nhan_telegram(tele_msg)

    def huy_da_duyet(self):
        """ Hủy yêu cầu đã duyệt """
        for record in self:
            if record.trang_thai != "đã_duyệt":
                raise exceptions.UserError("Chỉ có thể hủy yêu cầu có trạng thái 'Đã duyệt'.")
            
            record.write({"trang_thai": "đã_hủy"})
            msg_cancel = f"⚠️ Yêu cầu mượn phòng {record.phong_id.name} (đã duyệt) của bạn vừa bị quản trị viên hủy."
            self._gui_thong_bao_email(record.email, f"Thông báo hủy đặt phòng đã duyệt: {record.phong_id.name}", msg_cancel)
            self.lich_su(record, ghi_chu=f"Quản trị viên hủy và gửi Email thông báo tới {record.email}")

    def bat_dau_su_dung(self):
        """ Bắt đầu sử dụng phòng - Cập nhật thời gian mượn thực tế """
        for record in self:
            if record.trang_thai != "đã_duyệt":
                raise exceptions.UserError("Chỉ có thể bắt đầu sử dụng phòng có trạng thái 'Đã duyệt'.")

            # Kiểm tra nếu đã có người đang sử dụng phòng này
            kiem_tra_phong = self.env["dat_phong"].search([
                ("phong_id", "=", record.phong_id.id),
                ("trang_thai", "=", "đang_sử_dụng"),
                ("id", "!=", record.id)
            ])

            if kiem_tra_phong:
                raise exceptions.UserError(f"Phòng {record.phong_id.name} hiện đang được sử dụng. Vui lòng chờ đến khi phòng trống.")

            # Nếu không có ai đang sử dụng, cho phép bắt đầu
            record.write({
                "trang_thai": "đang_sử_dụng",
                "thoi_gian_muon_thuc_te": datetime.now()
            })
            self.lich_su(record)


    def tra_phong(self):
        """ Trả phòng - Cập nhật thời gian trả thực tế và đảm bảo thời gian mượn thực tế có giá trị """
        for record in self:
            if record.trang_thai != "đang_sử_dụng":
                raise exceptions.UserError("Chỉ có thể trả phòng đang ở trạng thái 'Đang sử dụng'.")
            current_time = datetime.now()
            thoi_gian_muon = record.thoi_gian_muon_thuc_te or current_time
            record.write({
                "trang_thai": "đã_trả",
                "thoi_gian_tra_thuc_te": current_time,
                "thoi_gian_muon_thuc_te": thoi_gian_muon
            })
            self.lich_su(record)
            
            # Gửi thông báo Telegram khi trả phòng
            tele_msg = f"🏁 <b>ĐÃ TRẢ PHÒNG</b>\nPhòng: {record.phong_id.name}\nNgười mượn: {record.nguoi_muon_id.display_name}\nLúc: {current_time.strftime('%H:%M %d/%m')}"
            gui_tin_nhan_telegram(tele_msg)
            
            # PHASE 3: Tính số giờ mượn và cộng dồn cho tài sản đi kèm
            delta = current_time - thoi_gian_muon
            hours = delta.total_seconds() / 3600.0
            if hours > 0 and record.tai_san_ids:
                for asset in record.tai_san_ids:
                    asset.sudo().write({'so_gio_su_dung': asset.so_gio_su_dung + hours})
                    gio_gioi_han = asset.loai_tai_san_id.gio_gioi_han_bao_tri
                    if gio_gioi_han > 0 and asset.so_gio_su_dung >= gio_gioi_han:
                        import datetime as dt # Dùng alias để tránh đụng độ
                        self.env['phieu_bao_tri'].sudo().create({
                            'tai_san_id': asset.id,
                            'ngay_bao_tri': fields.Datetime.now(),
                            'ngay_tra': fields.Datetime.now() + dt.timedelta(days=1),
                            'chi_phi': 0,
                            'ghi_chu': f"Hệ thống tự động phát hiện vượt mức hoạt động: {asset.so_gio_su_dung:.1f}/{gio_gioi_han} giờ (Sau khi dùng phòng {record.phong_id.name}).",
                            'state': 'draft'
                        })
        
        self.env["lich_su_muon_tra"].update_lich_su_muon_tra()

    @api.model
    def lich_su(self, record, ghi_chu=''):
        """ Ghi vào lịch sử mượn trả """
        self.env["lich_su_thay_doi"].create({
            "dat_phong_id": record.id,
            "nguoi_muon_id": record.nguoi_muon_id.id,
            "thoi_gian_muon_du_kien": record.thoi_gian_muon_du_kien,
            "thoi_gian_muon_thuc_te": record.thoi_gian_muon_thuc_te,
            "thoi_gian_tra_du_kien": record.thoi_gian_tra_du_kien,
            "thoi_gian_tra_thuc_te": record.thoi_gian_tra_thuc_te,
            "trang_thai": record.trang_thai,
            "ghi_chu": ghi_chu
        })

    @api.model
    def cron_nhac_nho_hop(self):
        """ Gửi thông báo nhắc nhở 15 phút trước giờ cuộc họp bắt đầu """
        now = datetime.now()
        warning_time = now + datetime.timedelta(minutes=15)
        # Tìm các cuộc họp sẽ bắt đầu trong vòng 15-20 phút tới và đã được duyệt
        upcoming_meetings = self.search([
            ('trang_thai', '=', 'đã_duyệt'),
            ('thoi_gian_muon_du_kien', '>=', now),
            ('thoi_gian_muon_du_kien', '<=', warning_time + datetime.timedelta(minutes=5))
        ])

        for meeting in upcoming_meetings:
            msg = f"⏰ Nhắc nhở: Cuộc họp của bạn tại {meeting.phong_id.name} sẽ bắt đầu lúc {meeting.thoi_gian_muon_du_kien.strftime('%H:%M %d/%m')}. Xin vui lòng chuẩn bị."
            self._gui_thong_bao_email(meeting.email, f"Nhắc nhở cuộc họp: {meeting.phong_id.name}", msg)
            self.lich_su(meeting, ghi_chu=f"Gửi Email nhắc nhở tham gia họp tới {meeting.email}")

    @api.model
    def cron_nhac_tra_phong(self):
        """ Gửi thông báo nhắc người dùng trả phòng nếu đã quá giờ dự kiến mà vẫn 'Đang sử dụng' """
        now = datetime.now()
        overdue_meetings = self.search([
            ('trang_thai', '=', 'đang_sử_dụng'),
            ('thoi_gian_tra_du_kien', '<', now)
        ])

        for meeting in overdue_meetings:
            msg = f"⏰ Nhắc nhở: Thời gian mượn phòng {meeting.phong_id.name} của bạn đã kết thúc lúc {meeting.thoi_gian_tra_du_kien.strftime('%H:%M %d/%m')}. Hãy hoàn tất cuộc họp và nhấn nút 'Trả phòng'."
            self._gui_thong_bao_email(meeting.email, f"Nhắc nhở trả phòng: {meeting.phong_id.name}", msg)
            self.lich_su(meeting, ghi_chu=f"Gửi Email nhắc nhở trả phòng tới {meeting.email}")
