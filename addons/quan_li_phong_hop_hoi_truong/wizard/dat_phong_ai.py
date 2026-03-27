from odoo import models, fields, api, exceptions
import logging
import requests
import json
import re
import datetime
import pytz

_logger = logging.getLogger(__name__)

class DatPhongAIWizard(models.TransientModel):
    _name = 'dat_phong.ai.wizard'
    _description = 'Trợ lý ảo AI Đặt phòng'

    ai_request = fields.Text(string="Nhập yêu cầu/câu hỏi tại đây", help="VD: Có phòng nào sức chứa 20 người không? Hoặc: Đặt cho tôi phòng Họp Lớn sáng mai.")
    ai_response = fields.Html(string="AI Trả Lời", readonly=True)

    def action_generate(self):
        self.ensure_one()
        if not self.ai_request or not self.ai_request.strip():
            raise exceptions.UserError("Sếp chưa nhập lệnh kìa! Hãy gõ nội dung vào ô hỏi nhé.")
        api_key = self.env['ir.config_parameter'].sudo().get_param('gemini_api_key')
        if not api_key:
            raise exceptions.UserError("Chưa được cấu hình Google Gemini API Key. Vui lòng vào Cài đặt -> Kỹ thuật -> Tham số hệ thống nhập 'gemini_api_key'.")

        # Chuẩn bị Context
        phong_hops = self.env['quan_ly_phong_hop'].search([('trang_thai', '=', 'su_dung')])
        phong_info = ", ".join([f"ID {p.id}: {p.name}" for p in phong_hops])

        tai_sans = self.env['tai_san'].search([('trang_thai', '=', 'LuuTru')])
        tai_san_info = ", ".join([f"ID {ts.id}: {ts.ten_tai_san}" for ts in tai_sans])

        dich_vus = self.env['dich_vu_di_kem'].search([])
        dich_vu_info = ", ".join([f"ID {dv.id}: {dv.name}" for dv in dich_vus])

        now = datetime.datetime.now()
        
        prompt = f"""
Bạn là Trợ lý Ảo phân tích dữ liệu Hệ thống Đặt Phòng vĩ đại nhất.
Người dùng giao tiếp: "{self.ai_request}"

DANH SÁCH DỮ LIỆU CÔNG TY (THÔNG TIN THỰC TẾ):
- Phòng họp: {phong_info}
- Tài sản mượn kèm: {tai_san_info}
- Dịch vụ đi kèm: {dich_vu_info}

Nhiệm vụ: Phân loại câu mở lời thành 1 trong 2 hành động cụ thể:
1. NẾU người dùng có ý định tò mò, XIN LỜI KHUYÊN, xem các phòng trống (VD: Có phòng nào sức chứa 10 người? Sáng mai lấy phòng nào phù hợp? Lịch trống là gì?): TRẢ LỜI NGAY, dạng "answer".
2. NẾU người dùng CHẮC CHẮN MUỐN ĐẶT PHÒNG/LẬP PHIẾU (VD: Đặt phòng VIP sáng mai nhé): TRẢ JSON dạng "create" để Odoo thực thi tạo phiếu.

Cấu trúc trả về BẮT BUỘC (Tuyệt đối chỉ xả chuỗi JSON, không dùng markdown):
Trường hợp Hỏi đáp, Tư vấn:
{{
    "action": "answer",
    "message": "<Câu trả lời của bạn, tư vấn phòng, báo phòng phù hợp>"
}}

Trường hợp Tạo Phiếu Đặt:
{{
    "action": "create",
    "phong_id": <ID phòng nguyên thủy, nếu không chắc thì để null>,
    "thoi_gian_muon_du_kien": "<YYYY-MM-DD HH:MM:SS>",
    "thoi_gian_tra_du_kien": "<YYYY-MM-DD HH:MM:SS>",
    "tai_san_ids": [<mảng các ID>],
    "dich_vu_ids": [<mảng các ID>],
    "so_luong": <số lượng>
}}
Lưu ý thời gian hiện tại là {now.strftime('%Y-%m-%d %H:%M:%S')}. Sáng là 08:00-11:30, Chiều là 13:30-17:00.
"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1}
        }

        try:
            response = requests.post(url, json=payload, timeout=20)
            response.raise_for_status()
            res_data = response.json()
            
            raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
            clean_json = re.sub(r'```json\n|\n```|```', '', raw_text).strip()
            
            ai_data = json.loads(clean_json)
            
            if ai_data.get('action') == 'answer':
                answer_text = ai_data.get('message', 'Không có câu trả lời cho yêu cầu này.')
                self.ai_response = f"<div style='margin-bottom: 10px; border-bottom: 1px dashed #ccc; padding-bottom: 5px;'><i><b style='color:#555;'>Bạn hỏi:</b> {self.ai_request}</i></div>{answer_text}"
                self.ai_request = False
                return {
                    'type': 'ir.actions.act_window',
                    'name': '✨ Trợ lý AI Đặt Phòng',
                    'res_model': 'dat_phong.ai.wizard',
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'new',
                }

            # Khởi tạo bản ghi mới
            employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
            if not employee:
                employee = self.env['hr.employee'].search([], limit=1)

            create_vals = {
                'nguoi_muon_id': employee.id if employee else False,
                'kieu_lap': 'khong_lap',
                'email': employee.work_email if employee else 'demo@gmail.com'
            }
            if ai_data.get('phong_id'): create_vals['phong_id'] = ai_data['phong_id']
            
            user_tz = pytz.timezone(self.env.user.tz or 'Asia/Ho_Chi_Minh')
            if ai_data.get('thoi_gian_muon_du_kien'):
                local_dt = datetime.datetime.strptime(ai_data['thoi_gian_muon_du_kien'], '%Y-%m-%d %H:%M:%S')
                utc_dt = user_tz.localize(local_dt).astimezone(pytz.utc)
                create_vals['thoi_gian_muon_du_kien'] = utc_dt.strftime('%Y-%m-%d %H:%M:%S')
            if ai_data.get('thoi_gian_tra_du_kien'):
                local_dt = datetime.datetime.strptime(ai_data['thoi_gian_tra_du_kien'], '%Y-%m-%d %H:%M:%S')
                utc_dt = user_tz.localize(local_dt).astimezone(pytz.utc)
                create_vals['thoi_gian_tra_du_kien'] = utc_dt.strftime('%Y-%m-%d %H:%M:%S')
            if ai_data.get('so_luong'): create_vals['so_luong'] = ai_data['so_luong']
            if ai_data.get('tai_san_ids'): create_vals['tai_san_ids'] = [(6, 0, ai_data['tai_san_ids'])]
            if ai_data.get('dich_vu_ids'): create_vals['dich_vu_ids'] = [(6, 0, ai_data['dich_vu_ids'])]
            
            # Tạo Phiếu Mượn
            new_record = self.env['dat_phong'].create(create_vals)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Phiếu Đặt Phòng (Sinh bởi AI)',
                'res_model': 'dat_phong',
                'res_id': new_record.id,
                'view_mode': 'form',
                'target': 'current',
            }

        except Exception as e:
            _logger.error("Lỗi gọi Gemini AI: %s", str(e))
            raise exceptions.UserError("AI Gemini không thể phân tích yêu cầu này do thiếu thông tin quá nhiều hoặc lỗi kết nối. Chi tiết lỗi từ Server: " + str(e))
