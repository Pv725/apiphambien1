# File: app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # cần cài flask-cors
import re

app = Flask(__name__)
CORS(app)  # cho phép Tampermonkey gọi từ mọi nguồn

# ============================================================
# DATABASE 600 CÂU HỎI (thay thế bằng dữ liệu thật của bạn)
# Định dạng: key là một phần chuỗi câu hỏi (đã chuẩn hóa),
# value là đáp án đúng.
# Dưới đây là dữ liệu mẫu 600 câu rút gọn, bạn phải thay thế toàn bộ.
# ============================================================
DATA = {
    # Format: "chuỗi con câu hỏi": "đáp án",
    "đường đôi": "Biển 3",
    "cấm xe ô tô rẽ trái": "Cả hai biển",
    "biển số 1 có ý nghĩa": "Đi thẳng hoặc rẽ trái trên cầu vượt",
    # Thêm 597 câu nữa vào đây...
    "tốc độ tối đa trong khu dân cư": "50 km/h",
    "nồng độ cồn cho phép": "0 mg/100 ml máu",
    # ...
}

# Chuẩn hóa chuỗi: bỏ dấu câu, khoảng trắng thừa, chữ thường
def normalize(s):
    if not s:
        return ""
    s = s.lower().strip()
    s = re.sub(r'[^\w\s]', '', s)  # xóa dấu câu
    s = re.sub(r'\s+', ' ', s)
    return s

# Tìm kiếm đáp án: duyệt từng key, nếu key nằm trong câu hỏi hoặc ngược lại
def find_answer(question_text):
    norm_q = normalize(question_text)
    # Tìm khớp chính xác nhất
    for key, answer in DATA.items():
        norm_k = normalize(key)
        if norm_k in norm_q or norm_q in norm_k:
            return answer
    # Nếu không tìm thấy, thử tìm từng từ khóa
    words = norm_q.split()
    for key, answer in DATA.items():
        norm_k = normalize(key)
        if any(w in norm_k for w in words if len(w) > 3):
            return answer
    return None

# Endpoint chính
@app.route('/api/tra-cuu', methods=['POST'])
def tra_cuu():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Thiếu trường 'question'"}), 400
    question = data['question']
    answer = find_answer(question)
    if answer:
        return jsonify({"answer": answer})
    else:
        return jsonify({"answer": "Không tìm thấy đáp án"}), 404

# Health check
@app.route('/')
def home():
    return "API Bot Hoàng Gia 600 câu đang chạy"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
