from odoo import models, fields, api, exceptions
import logging
import requests
import json
import re
import datetime

_logger = logging.getLogger(__name__)

class NhanVienAIWizard(models.TransientModel):
    _name = 'nhan_vien.ai.wizard'
    ai_request = fields.Text(string="Thông tin Ứng viên/Câu hỏi", help="VD: Tạo hồ sơ cho bạn Nguyễn Thanh Tùng sinh 20/10/1998... HOẶC: Chức vụ Sale thuộc phòng nào?")
    ai_response = fields.Html(string="AI Trả Lời", readonly=True)

    def action_generate(self):
        self.ensure_one()
        if not self.ai_request or not self.ai_request.strip():
            raise exceptions.UserError("Sếp chưa nhập lệnh kìa! Hãy gõ nội dung vào ô hỏi nhé.")
        api_key = self.env['ir.config_parameter'].sudo().get_param('gemini_api_key')
        if not api_key:
            raise exceptions.UserError("Chưa cấu hình Google Gemini API Key. Vui lòng vào Cài đặt -> Kỹ thuật -> Tham số hệ thống nhập 'gemini_api_key'.")

        # Chuẩn bị Context
        phong_bans = self.env['phong_ban'].search([])
        phong_info = ", ".join([f"ID {p.id}: {p.ten_phong_ban}" for p in phong_bans])

        jobs = self.env['hr.job'].search([])
        job_info = ", ".join([f"ID {j.id}: {j.name}" for j in jobs])
        
        total_employees = self.env['hr.employee'].search_count([])

        now = datetime.datetime.now()
        
        prompt = f"""
Bạn là Trợ lý Ảo AI xử lý dữ liệu cho hệ thống Nhân sự ERP Odoo.
Giám đốc Nhân sự yêu cầu: "{self.ai_request}"

THÔNG TIN HỆ THỐNG HIỆN TẠI:
- Tổng số nhân sự toàn công ty: {total_employees} người
- Danh sách Phòng ban: {phong_info}
- Chức vụ (Vị trí công việc): {job_info}

Nhiệm vụ: Phân loại câu lệnh để TẠO HỒ SƠ hoặc TRẢ LỜI CÂU HỎI.
1. Nếu Giám đốc ĐẶT CÂU HỎI (VD: Có những phòng ban nào? Chức vụ Kế toán thì thuộc phòng nào hợp lý?): Trả về JSON chứa "action": "answer".
2. Nếu Giám đốc RA LỆNH TẠO HỒ SƠ (Đọc thông tin ứng viên): Trả về JSON chứa "action": "create".
- Ngày sinh (birthday), Ngày cấp CCCD (ngay_cap) FORMAT: YYYY-MM-DD. Năm nay {now.year}. 
- Giới tính (gender): "male", "female", "other".
- Nếu không nhắc tới, trả về null.

Cấu trúc trả lời BẮT BUỘC (TUYỆT ĐỐI không dùng markdown):
Trường hợp Hỏi Đáp:
{{
    "action": "answer",
    "message": "<Câu trả lời thân thiện của bạn>"
}}

Trường hợp Tạo Hồ Sơ:
{{
    "action": "create",
    "ho_ten_dem": "<Họ và tên đệm>",
    "ten": "<Tên chính>",
    "gender": "<male/female/other>",
    "birthday": "<YYYY-MM-DD>",
    "work_phone": "<SĐT>",
    "que_quan": "<Quê quán>",
    "so_cccd": "<CCCD số>",
    "ngay_cap": "<YYYY-MM-DD>",
    "phong_ban_id": <ID phòng>,
    "job_id": <ID chức vụ>
}}
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
                self.ai_response = f"<div style='margin-bottom: 10px; border-bottom: 1px dashed #ccc; padding-bottom: 5px;'><i><b style='color:#555;'>Giám đốc HR hỏi:</b> {self.ai_request}</i></div>{answer_text}"
                self.ai_request = False
                return {
                    'type': 'ir.actions.act_window',
                    'name': '✨ Trợ lý Tuyển Dụng',
                    'res_model': 'nhan_vien.ai.wizard',
                    'res_id': self.id,
                    'view_mode': 'form',
                    'target': 'new',
                }

            create_vals = {}
            if ai_data.get('ho_ten_dem'): create_vals['ho_ten_dem'] = ai_data['ho_ten_dem']
            if ai_data.get('ten'): create_vals['ten'] = ai_data['ten']
            if ai_data.get('gender'): create_vals['gender'] = ai_data['gender']
            if ai_data.get('birthday'): create_vals['birthday'] = ai_data['birthday']
            if ai_data.get('work_phone'): create_vals['work_phone'] = ai_data['work_phone']
            if ai_data.get('que_quan'): create_vals['que_quan'] = ai_data['que_quan']
            if ai_data.get('so_cccd'): create_vals['so_cccd'] = ai_data['so_cccd']
            if ai_data.get('ngay_cap'): create_vals['ngay_cap'] = ai_data['ngay_cap']
            if ai_data.get('phong_ban_id'): create_vals['phong_ban_id'] = ai_data['phong_ban_id']
            if ai_data.get('job_id'): create_vals['job_id'] = ai_data['job_id']

            if not create_vals.get('ten'):
                raise exceptions.UserError("AI không tìm thấy tên nhân viên trong lệnh của sếp! Bạn không thể tạo nhân viên trống rỗng.")

            # Fix lỗi DB Not-Null: Tự ghép tay trường name để Odoo vượt qua bước kiểm tra Constraint trước khi chạy hàm Compute
            ho_ten_dem = create_vals.get('ho_ten_dem', '')
            ten = create_vals.get('ten', '')
            create_vals['name'] = f"{ho_ten_dem} {ten}".strip()

            new_emp = self.env['hr.employee'].create(create_vals)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Hồ sơ Nhân viên Mới (AI Sinh)',
                'res_model': 'hr.employee',
                'res_id': new_emp.id,
                'view_mode': 'form',
                'target': 'current',
            }

        except Exception as e:
            _logger.error("Lỗi gọi Gemini AI HR: %s", str(e))
            raise exceptions.UserError("AI Gemini không thể phân tích nội dung. Chi tiết lỗi từ Server:\n" + str(e))
