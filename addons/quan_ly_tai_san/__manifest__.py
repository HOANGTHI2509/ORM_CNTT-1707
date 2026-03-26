{
    'name': "Quản lý tài sản",

    'summary': "Quản lý tài sản và lịch sử sử dụng",

    'description': """
        Module quản lý tài sản trong doanh nghiệp, bao gồm:
        - Thông tin tài sản (tai_san, loai_tai_san, vi_tri, nha_cung_cap)
        - Lịch sử sử dụng (lich_su_su_dung)
        - Lịch sử bảo trì (lich_su_bao_tri)
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Human Resources/Assets',
    'version': '0.2',
    'license': 'LGPL-3',

    'depends': ['base', 'nhan_su', 'hr', 'board'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/tai_san_ai_view.xml',
        'sequences.xml',
        'reports/report_ban_giao.xml',
        'views/dashboard.xml',
        'views/tai_san.xml',
        'views/phieu_muon.xml',
        'views/phieu_bao_tri.xml',
        'views/vi_tri.xml',
        'views/loai_tai_san.xml',
        'views/nha_cung_cap.xml',
        'views/lich_su_su_dung.xml',
        'views/lich_su_bao_tri.xml',
        'views/lich_su_di_chuyen.xml',
        'views/phieu_dieu_chuyen.xml',
        'views/phieu_kiem_ke.xml',
        'views/lich_su_kiem_ke.xml',
        'views/bien_ban_den_bu.xml',

        'views/thanh_ly.xml',
        'views/thong_ke.xml',
        'views/nhan_vien_view.xml',
        'views/phieu_ban_giao_view.xml',
        'views/dot_bao_duong_view.xml',
        'views/menu.xml',

    ],

    'demo': [
    ],

    'assets': {
        'web.assets_backend': [
            'quan_ly_tai_san/static/src/css/tai_san.css',
        ],
    },
    'installable': True,
    'application': True,
}
