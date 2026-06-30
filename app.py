# ============================================================
# File: app.py - GEMINI AI ĐÃ TÍCH HỢP API KEY CỦA BẠN
# ============================================================
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# API Key của bạn (đã nhập trực tiếp)
GEMINI_API_KEY = "AIzaSyCq5AfWX-LA_bzeSU2ykP8cHysj9pXvZWc"
genai.configure(api_key=GEMINI_API_KEY)

# Model Gemini
MODEL_NAME = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

# Prompt hệ thống
SYSTEM_PROMPT = """
Bạn là trợ lý tra cứu đáp án câu hỏi lý thuyết lái xe.
Nhiệm vụ: Đọc câu hỏi và chỉ trả về chính xác nội dung đáp án đúng, không giải thích gì thêm.
Trả lời ngắn gọn, đúng đáp án, không thêm từ "Đáp án:", không xuống dòng.
Ví dụ câu hỏi: "Biển nào báo hiệu Đường đôi?" -> trả lời: "Biển 3".
Nếu không tìm thấy đáp án, trả về: "Không xác định".
"""

def get_answer_from_gemini(question_text):
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nCâu hỏi: {question_text}\nTrả lời:"
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
                max_output_tokens=60,
                candidate_count=1,
            ),
            safety_settings={
                'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
            }
        )
        answer = response.text.strip()
        answer = re.sub(r'^(Đáp án:|đáp án:|Answer:|answer:)\s*', '', answer)
        return answer
    except Exception as e:
        print(f"Lỗi Gemini API: {e}")
        return None

# Endpoint
@app.route('/api/tra-cuu', methods=['POST'])
def tra_cuu():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Thiếu trường 'question'"}), 400
    
    question = data['question']
    answer = get_answer_from_gemini(question)
    if answer and answer != "Không xác định":
        return jsonify({"answer": answer})
    
    return jsonify({"answer": "Không tìm thấy đáp án"}), 404

@app.route('/')
def home():
    return "API Bot Hoàng Gia - Gemini AI đang chạy"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
