# ============================================================
# File: app.py - GEMINI AI ĐÃ ĐƯỢC LẮP MẮT THẦN (VISION)
# ============================================================
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

# NHỚ THAY LẠI API KEY MỚI CỦA BẠN VÀO ĐÂY NHÉ (Key cũ tôi khuyên bạn nên xóa đi để bảo mật)
GEMINI_API_KEY = "AIzaSy_NHẬP_KEY_CỦA_BẠN_VÀO_ĐÂY"
genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

SYSTEM_PROMPT = """
Bạn là chuyên gia thi lý thuyết lái xe hạng B1/B2/C tại Việt Nam.
Nhiệm vụ: Đọc câu hỏi (và xem hình ảnh nếu có) để tìm ra đáp án đúng nhất.
Chỉ trả về phần chữ của đáp án đúng, tuyệt đối không giải thích, không thêm chữ "Đáp án:".
Ví dụ: "Biển 3", "Cả hai biển", "Đi thẳng hoặc rẽ trái".
"""

def get_answer_from_gemini(question_text, image_url=None):
    try:
        # Nhét chữ vào trước
        contents = [f"{SYSTEM_PROMPT}\n\nCâu hỏi: {question_text}\nTrả lời:"]
        
        # Nếu có link ảnh, tải ảnh về và nhét thêm vào cho Gemini nhìn
        if image_url:
            print(f"[*] Đang tải ảnh từ web: {image_url}")
            img_response = requests.get(image_url, timeout=5)
            if img_response.status_code == 200:
                img = Image.open(BytesIO(img_response.content))
                contents.append(img)
                print("[+] Đã tải ảnh và ghép vào Prompt thành công!")

        response = model.generate_content(
            contents,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
                max_output_tokens=60,
            )
        )
        
        answer = response.text.strip()
        answer = re.sub(r'^(Đáp án:|đáp án:|Answer:|answer:)\s*', '', answer)
        return answer
    except Exception as e:
        print(f"Lỗi Gemini API: {e}")
        return None

@app.route('/api/tra-cuu', methods=['POST'])
def tra_cuu():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Thiếu dữ liệu"}), 400
    
    question = data['question']
    image_url = data.get('image_url') # Nhận thêm link ảnh từ Tampermonkey
    
    print(f"\n[+] Đang hỏi Gemini: {question}")
    answer = get_answer_from_gemini(question, image_url)
    
    if answer and answer != "Không xác định":
        print(f"=> Gemini chốt đáp án: {answer}")
        return jsonify({"answer": answer})
    
    return jsonify({"answer": "Không tìm thấy đáp án"}), 404

if __name__ == '__main__':
    print("🚀 Máy chủ Gemini (Có Vision) đang chạy tại Port 10000")
    app.run(host='0.0.0.0', port=10000)
