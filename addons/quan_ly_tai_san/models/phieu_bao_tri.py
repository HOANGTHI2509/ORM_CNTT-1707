import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import requests
import logging

_logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "8674994673:AAGry6psZQjjR1EMXcXprIEevecQ6Ur4Ei0"
TELEGRAM_CHAT_ID = "8262831605"

def gui_tin_nhan_telegram_ts(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}, timeout=5)
    except Exception as e:
        _logger.error("Lỗi gửi Telegram: %s", str(e))


class PhieuBaoTri(models.Model):
    _name = 'phieu_bao_tri'
    _description = 'Phiếu bảo trì tài sản'
    _order = 'ma_phieu_bao_tri'
    _states = {
        'draft': 'Nháp',
        'approved': 'Đã duyệt',
        'done': 'Hoàn thành',
        'cancelled': 'Hủy',
    }

    ma_phieu_bao_tri = fields.Char("Mã phiếu bảo trì", copy=False, readonly=True, default="New",
                                   states={'draft': [('readonly', False)]})
    ngay_bao_tri = fields.Datetime("Thời gian bảo trì dự kiến", required=True,
                                   states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                           'cancelled': [('readonly', True)]})
    ngay_bao_tri_thuc_te = fields.Datetime("Thời gian bảo trì thực tế", required=False,
                                           states={'draft': [('readonly', True)], 'approved': [('readonly', False)],
                                                   'done': [('readonly', True)], 'cancelled': [('readonly', True)]})
    ngay_tra = fields.Datetime("Thời gian trả dự kiến", required=True,
                               states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                       'cancelled': [('readonly', True)]})
    ngay_tra_thuc_te = fields.Datetime("Thời gian trả thực tế", required=False,
                                       states={'draft': [('readonly', True)], 'approved': [('readonly', False)],
                                               'done': [('readonly', True)], 'cancelled': [('readonly', True)]})
    chi_phi = fields.Integer("Chi phí", required=True,
                             states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                     'cancelled': [('readonly', True)]})
    ghi_chu = fields.Char("Ghi chú", states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                             'cancelled': [('readonly', True)]})
    tai_san_id = fields.Many2one(comodel_name="tai_san", string="Tài sản", required=True, store=True,
                                 states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                         'cancelled': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Nháp'), ('approved', 'Đã duyệt'), ('done', 'Hoàn thành'), ('cancelled', 'Hủy')],
        default='draft', string="Trạng thái")

    @api.constrains('ma_phieu_bao_tri')
    def _check_ma_phieu_bao_tri_format(self):
        for record in self:
            if not re.fullmatch(r'PB-\d{5}', record.ma_phieu_bao_tri):
                raise ValidationError("Mã phải có định dạng PB-XXXXX (ví dụ: PB-12345)")

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu_bao_tri', 'New') == 'New':
            last_record = self.search([], order='ma_phieu_bao_tri desc', limit=1)
            if last_record and last_record.ma_phieu_bao_tri.startswith('PB-'):
                last_number = int(last_record.ma_phieu_bao_tri.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ma_phieu_bao_tri'] = f'PB-{new_number:05d}'
            
        record = super(PhieuBaoTri, self).create(vals)
        
        # Telegram New
        if record.tai_san_id:
            tele_msg = f"🔧 <b>BÁO CÁO HỎNG / BẢO TRÌ MỚI ({record.ma_phieu_bao_tri})</b>\nTài sản: {record.tai_san_id.ten_tai_san}\nChi phí dự kiến: {record.chi_phi:,.0f} VNĐ\nTrạng thái: Nháp"
            gui_tin_nhan_telegram_ts(tele_msg)
            
        return record

    def action_approve(self):
        for record in self:
            if record.state == 'draft':
                self.env['lich_su_bao_tri'].create({
                    'ma_lich_su_bao_tri': self.env['ir.sequence'].next_by_code('lich_su_bao_tri') or 'New',
                    'ngay_bao_tri': record.ngay_bao_tri,
                    'ngay_tra': record.ngay_tra,
                    'chi_phi': record.chi_phi,
                    'ghi_chu': record.ghi_chu,
                    'tai_san_id': record.tai_san_id.id,
                })
                record.state = 'approved'
                
                # Telegram Approve
                tele_msg = f"✅ <b>ĐÃ DUYỆT BẢO TRÌ TÀI SẢN ({record.ma_phieu_bao_tri})</b>\nTài sản: {record.tai_san_id.ten_tai_san}\nNgày dự kiến xong: {record.ngay_tra.strftime('%d/%m/%Y') if record.ngay_tra else ''}"
                gui_tin_nhan_telegram_ts(tele_msg)

    def action_done(self):
        for record in self:
            if record.state == 'approved':
                if not all([record.ngay_bao_tri_thuc_te, record.ngay_tra_thuc_te, record.chi_phi]):
                    raise UserError((
                                        'Vui lòng nhập đầy đủ Ngày bảo trì thực tế, Ngày trả thực tế và Chi phí trước khi hoàn thành.'))
                record.state = 'done'
                lich_su = self.env['lich_su_bao_tri'].search([
                    ('tai_san_id', '=', record.tai_san_id.id),
                    ('ngay_bao_tri', '=', record.ngay_bao_tri),
                    ('ngay_tra', '=', record.ngay_tra),
                    ('chi_phi', '=', record.chi_phi),
                    ('ghi_chu', '=', record.ghi_chu)
                ], limit=1)
                if lich_su:
                    lich_su.write({
                        'ngay_bao_tri': record.ngay_bao_tri_thuc_te,
                        'ngay_tra': record.ngay_tra_thuc_te
                    })

    def action_cancel(self):
        for record in self:
            if record.state in ['draft', 'approved']:
                lich_su_bao_tri = self.env['lich_su_bao_tri'].search([
                    ('tai_san_id', '=', record.tai_san_id.id),
                    ('ngay_bao_tri', '=', record.ngay_bao_tri),
                    ('ngay_tra', '=', record.ngay_tra),
                    ('chi_phi', '=', record.chi_phi),
                    ('ghi_chu', '=', record.ghi_chu)
                ])
                if lich_su_bao_tri:
                    lich_su_bao_tri.unlink()
                record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            if record.state in ['approved', 'cancelled']:
                record.state = 'draft'
