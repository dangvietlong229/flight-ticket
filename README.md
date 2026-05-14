# TARA BOT 🤖✈️🛒

**AI agent cá nhân trên Telegram — săn vé máy bay, so sánh giá, cào deal.**

[![Deploy on Render](https://img.shields.io/badge/deploy-Render-46E3B7?style=flat-square)](https://render.com)
[![License: MIT](https://img.shields.io/badge/license-MIT-4ade80?style=flat-square)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-60a5fa?style=flat-square)](https://python.org)

> Build bởi [Tara Le](https://github.com/thaolst) — AI × Growth Marketing

---

## ✨ Tính năng

| Tính năng | Mô tả | Trạng thái |
|-----------|-------|------------|
| 💬 **Chat tự nhiên** | Hỏi "tìm vé SG Đà Nẵng cuối tuần" — Gemini hiểu, SerpAPI search | ✅ |
| ✈️ **Tra cứu chuyến bay** | Giá, hãng, giờ bay real-time từ Google Flights | ✅ |
| 🛒 **So sánh giá đồ** | Search sản phẩm, so sánh từ nhiều nguồn | ✅ |
| 🔔 **Daily monitor** | Mỗi sáng check giá các tuyến quen thuộc, gửi alert | ✅ |
| 🧠 **Context-aware** | Gemini nhớ lịch sử chat trong session | ✅ |
| 🔗 **Affiliate inject** | Tự động thêm affiliate link vào kết quả | ✅ |
| 🆕 **Shopee cào giá** | *(coming soon)* |

## 🎬 Demo

*Screenshot / GIF sẽ update sau khi deploy*

```
👤: tìm vé SG ra Hà Nội thứ 7 tuần này
🤖: ✈️ SGN → HAN
    📅 2026-05-16 → 2026-05-21

    1. Vietjet Air — 1,450,000 VND (2h05m)
       SGN 06:00 → HAN 08:05

    2. Vietnam Airlines — 2,100,000 VND (2h)
       SGN 08:30 → HAN 10:30
```

## 🧱 Tech stack

```
┌──────────┐     ┌───────────┐     ┌──────────┐
│ Telegram │ ←→ │  Gemini   │ ←→ │ SerpAPI  │
│   Bot    │     │ 1.5 Flash │     │(Flights+ │
│          │     │(Tool-call)│     │ Shopping)│
└──────────┘     └───────────┘     └──────────┘
                       ↕
                 ┌──────────┐
                 │ GitHub   │
                 │ Actions  │
                 │(scheduler)│
                 └──────────┘
```

- **Telegram Bot** — python-telegram-bot v20+
- **Gemini 1.5 Flash** — NLU + tool-calling (Google AI Studio - Free)
- **SerpAPI** — Google Flights + Google Shopping (Free tier)
- **Render** — host 24/7 qua Webhooks (Free tier)
- **GitHub Actions** — daily cron monitor (Free)

## 🚀 Deploy (Miễn phí 100%)

Bạn có thể chạy bot này trực tiếp trên máy hoặc host hoàn toàn miễn phí trên nền tảng Render.

1. **Fork repo** → `git clone https://github.com/thaolst/tara-bot`
2. **Get API keys**:
   - [@BotFather](https://t.me/botfather) → tạo bot → copy token
   - [SerpAPI](https://serpapi.com) → sign up → copy key
   - [Google AI Studio](https://aistudio.google.com/app/apikey) → copy Gemini key
3. **Deploy lên Render**:
   - Tạo Web Service trên Render kết nối với GitHub Repo của bạn.
   - Thêm các biến môi trường: `TELEGRAM_TOKEN`, `GEMINI_API_KEY`, `SERPAPI_KEY`, `ALLOWED_USER_ID`, `WEBHOOK_URL` (ví dụ: `https://your-render-app.onrender.com`).
4. **Bật monitor**:
   - Settings → Secrets → thêm vào GitHub repo
   - Actions → enable workflow

*Chi tiết cách deploy (kể cả test trên local): [DEPLOY.md](./DEPLOY.md)*

## 📁 Cấu trúc

```
src/
├── bot.py              # Telegram bot entry point (Polling & Webhook)
├── agents.py           # Gemini agent + automatic tool-calling
├── config.py           # Env config loader
└── tools/
    └── serpapi.py      # Flight + shopping search
.github/workflows/
└── monitor.yml         # Daily price check
```

## 🗺️ Roadmap

- [x] Flight search (SerpAPI)
- [x] Shopping price compare
- [x] Daily price monitor (GitHub Actions)
- [x] 24/7 Telegram bot qua Render Webhooks
- [ ] Shopee price scraper
- [ ] Affiliate link injection vào kết quả
- [ ] Auto-deal: notify khi deal tốt xuất hiện
- [ ] Multi-user support

## 📝 License

MIT — free to use, fork, modify.

---

*Tara Bot — AI agent cá nhân, build public để chia sẻ, không phải product thương mại.*
