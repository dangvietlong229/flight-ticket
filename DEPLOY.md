# DEPLOY.md — Hướng dẫn setup tara-bot (Miễn phí 100%)

## 1. Tạo API keys

### 1.1 Telegram Bot Token
- Mở Telegram, tìm `@BotFather`
- Send `/newbot` → đặt tên → nhận token
- Lưu token dạng: `123456:ABC-DEF1234`

### 1.2 Lấy Telegram User ID của bạn
- Mở Telegram, tìm `@userinfobot`
- Send `/start` → copy số ID (VD: `123456789`)

### 1.3 SerpAPI Key
- Vào https://serpapi.com
- Sign up → Dashboard copy key
- Free: 100 searches/tháng

### 1.4 Gemini API Key
- Vào [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create API key (Hoàn toàn miễn phí)

---

## 2. Cách 1: Chạy trực tiếp trên máy (Local Polling)

Phù hợp để test nhanh hoặc khi bạn chỉ cần bật bot lúc đang mở máy.

### 2.1 Cấu hình môi trường
Tạo file `.env` trong thư mục `tara-bot` và điền các key:
```env
TELEGRAM_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_key
SERPAPI_KEY=your_serpapi_key
ALLOWED_USER_ID=your_telegram_id
```

### 2.2 Chạy bot
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run_bot.sh
```

---

## 3. Cách 2: Deploy lên Render (Miễn phí 24/7 qua Webhook)

Phù hợp nếu bạn muốn bot luôn chạy trên mạng để có thể nhắn tin hỏi bất cứ lúc nào mà không cần bật máy tính.

### 3.1 Push code lên GitHub
Tạo 1 repo riêng tư (private repo) trên GitHub của bạn và push thư mục `tara-bot` lên.

### 3.2 Setup Render
- Đăng nhập [Render.com](https://render.com) (dùng tài khoản GitHub).
- Chọn **New** -> **Web Service**.
- Kết nối với repo GitHub chứa `tara-bot`.
- Render sẽ tự động nhận diện cấu hình từ file `render.yaml`.
- Tuy nhiên, bạn cần thiết lập biến môi trường ở bước tiếp theo.

### 3.3 Thiết lập Environment Variables trên Render
Trong trang cài đặt của Web Service trên Render, mục **Environment**, thêm các biến sau:
- `TELEGRAM_TOKEN`
- `GEMINI_API_KEY`
- `SERPAPI_KEY`
- `ALLOWED_USER_ID`
- `WEBHOOK_URL`: Đây là đường dẫn Web Service của bạn trên Render (Ví dụ: `https://tara-bot-xyz.onrender.com`). Chú ý không để dấu gạch chéo `/` ở cuối.

### 3.4 Deploy và Test
- Bấm **Deploy**. Sau khi Render báo thành công (Build Successful).
- Lần gọi đầu tiên (webhook cold start) có thể mất khoảng 50 giây do Render Free Tier sẽ "ngủ" nếu không hoạt động. Các lần sau sẽ phản hồi tức thì.

---

## 4. Setup Daily Monitor (GitHub Actions)

Bot chat chạy trên Render. Tính năng theo dõi giá (Monitor) sẽ chạy trên GitHub Actions (miễn phí).

### 4.1 Thêm secrets vào GitHub repo
- Settings → Secrets and variables → Actions
- Add:
  - `SERPAPI_KEY`
  - `TELEGRAM_TOKEN`
  - `TELEGRAM_CHAT_ID` (user ID của bạn)
  - `GEMINI_API_KEY`

### 4.2 Enable workflow
- Actions tab → "Flight Monitor" → Enable
- Workflow chạy mỗi ngày 9:00 AM Vietnam time

---

## 5. Budget

| Service | Cost | Ghi chú |
|---------|------|---------|
| Render | $0 | Free tier Web Service (ngủ sau 15p, Webhook đánh thức tự động) |
| SerpAPI | $0 | Free tier |
| Gemini API | $0 | Free tier rất dư dả cho bot cá nhân |
| GitHub Actions | $0 | Public repo / Private repo free quota |
| **Total** | **$0/tháng** | Hoàn toàn không cần thẻ tín dụng |
