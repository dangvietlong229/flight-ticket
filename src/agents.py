"""Gemini agent with tool-calling for flight and shopping search."""

from __future__ import annotations

import logging
from datetime import date

import google.generativeai as genai

from .config import Config
from .tools.serpapi import search_flights, search_shopping

log = logging.getLogger("tara-bot.agent")

TODAY = date.today()

SYSTEM_PROMPT = f"""Bạn là Tara Bot — một agent thông minh chuyên tìm kiếm chuyến bay và săn giá đồ.

NGUYÊN TẮC:
- Trả lời bằng tiếng Việt tự nhiên, thân thiện.
- Khi user hỏi vé máy bay, gọi tool search_flights.
- Khi user hỏi giá sản phẩm, gọi tool search_shopping.
- Sau khi tool trả kết quả, chuyển tiếp NGUYÊN VĂN kết quả đó cho user, chỉ thêm 1-2 câu ngắn ở đầu hoặc cuối.
- KHÔNG reformat lại kết quả từ tool — giữ nguyên định dạng.
- Có thể nói chuyện thông thường (chào hỏi, tạm biệt) — không cần gọi tool.

Hôm nay là {TODAY.strftime("%A, %d/%m/%Y")} — ĐÂY LÀ MỐC THỜI GIAN HIỆN TẠI.
- KHÔNG TỰ ĐỘNG THÊM ngày về (return_date) nếu user không yêu cầu khứ hồi hoặc không nói rõ ngày về. Nếu không có ngày về, bot sẽ tự hiểu là tìm vé một chiều.
- Mặc định cho các câu hỏi mơ hồ về thời gian:
- "cuối tuần" → thứ Sáu tuần gần nhất (không quá khứ)
- "tuần sau" → tuần tiếp theo
- Nếu không rõ, lấy ngày đi và ngày về hợp lý."""

class Agent:
    def __init__(self):
        genai.configure(api_key=Config.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
            tools=[search_flights, search_shopping],
        )
        self.chat_session = self.model.start_chat(enable_automatic_function_calling=True)

    def chat(self, user_message: str) -> str:
        """Send user message, execute tool calls automatically via Gemini, return response."""
        try:
            response = self.chat_session.send_message(user_message)
            return response.text
        except Exception as e:
            log.exception("Error during Gemini API call")
            return f"Xin lỗi, em không thể xử lý yêu cầu này ngay bây giờ. Thử lại với câu hỏi đơn giản hơn nhé! ({e})"
