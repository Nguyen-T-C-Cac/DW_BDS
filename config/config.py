import os
import mysql.connector
from dotenv import load_dotenv

# Khi lên GitHub Actions/Render, nó sẽ tự lấy từ Secrets/Environment Variables của hệ thống
load_dotenv()

# Cấu hình SSL (Bắt buộc cho TiDB)
# Trên GitHub Actions/Render (Linux), file CA thường nằm ở đây
ssl_ca_path = "/etc/ssl/certs/ca-certificates.crt"

# Nếu chạy trên Windows (Local), có thể không có file này, ta có thể bỏ qua check SSL tạm thời
# hoặc bạn phải tải file CA về máy và trỏ đường dẫn vào.

ssl_args = {}
if os.path.exists(ssl_ca_path):
    ssl_args = {"ssl_ca": ssl_ca_path, "ssl_verify_identity": True}
else:
    # Fallback cho Windows Local (nếu không cài certificate)
    ssl_args = {"ssl_disabled": False} 

# Tạo lại dictionary cfg từ biến môi trường
common_config = {
    "host": os.getenv("TIDB_HOST"),
    "port": int(os.getenv("TIDB_PORT", 4000)),
    "user": os.getenv("TIDB_USER"),
    "password": os.getenv("TIDB_PASSWORD"),
    **ssl_args # Tự động thêm cấu hình SSL vào
}

cfg = {
    "staging": {
        **common_config,
        "database": os.getenv("DB_NAME_STAGING", "estate_stagging")
    },
    "datawarehouse": {
        **common_config,
        "database": os.getenv("DB_NAME_DW", "estate_dw")
    },
    "datamart": {
        **common_config,
        "database": os.getenv("DB_NAME_MART", "estate_mart")
    },
    "control": {
        **common_config,
        "database": os.getenv("DB_NAME_CONTROL", "estate_control")
    }
}