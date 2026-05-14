"""Flight search tool using SerpAPI."""

from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Any

import httpx

from ..config import Config


def _get_next_friday() -> str:
    """Return next Friday as YYYY-MM-DD."""
    today = date.today()
    days_ahead = (4 - today.weekday()) % 7  # Friday = 4
    if days_ahead == 0:
        days_ahead = 7
    return (today + timedelta(days=days_ahead)).isoformat()


SERPAPI_BASE = "https://serpapi.com/search.json"


def _search_oneway(departure_id: str, arrival_id: str, date_str: str, adults: int, currency: str) -> list:
    """Helper: call SerpAPI for a one-way flight, return list of flights."""
    key = Config.serpapi_key
    params: dict[str, Any] = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": date_str,
        "adults": adults,
        "currency": currency,
        "type": "2",  # One-way
        "api_key": key,
    }
    try:
        resp = httpx.get(SERPAPI_BASE, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("best_flights", []) + data.get("other_flights", [])
    except Exception as e:
        return []


def search_flights(
    departure_id: str = "SGN",
    arrival_id: str = "HAN",
    outbound_date: str | None = None,
    return_date: str | None = None,
    adults: int = 1,
    currency: str = "VND",
) -> str:
    """Search flights via SerpAPI Google Flights engine.

    Args:
        departure_id: IATA code (e.g. SGN, HAN, DAD)
        arrival_id: IATA code of destination
        outbound_date: YYYY-MM-DD, defaults to next Friday
        return_date: YYYY-MM-DD. ONLY provide if user explicitly asks for round-trip or mentions a return date. Leave empty for one-way.
        adults: number of passengers
        currency: VND, USD, etc.

    Returns:
        Formatted string with best options
    """
    outbound = outbound_date or _get_next_friday()

    if return_date:
        # Round-trip: 2 independent one-way searches
        outbound_flights = _search_oneway(departure_id, arrival_id, outbound, adults, currency)
        return_flights = _search_oneway(arrival_id, departure_id, return_date, adults, currency)
        return _format_roundtrip(outbound_flights, return_flights, departure_id, arrival_id, outbound, return_date)
    else:
        # One-way search
        flights = _search_oneway(departure_id, arrival_id, outbound, adults, currency)
        return _format_oneway(flights, departure_id, arrival_id, outbound)


CITY_MAP = {
    "SGN": "Sài Gòn", "HAN": "Hà Nội", "DAD": "Đà Nẵng",
    "PQC": "Phú Quốc", "CXR": "Nha Trang", "HUI": "Huế",
    "DIN": "Điện Biên", "VII": "Vinh", "UIH": "Quy Nhơn",
    "TBB": "Tuy Hòa", "VCA": "Cần Thơ", "DLI": "Đà Lạt",
    "VDO": "Vân Đồn", "VKG": "Rạch Giá", "VCS": "Côn Đảo",
}


def _format_flight_block(flights: list, max_results: int = 5) -> list[str]:
    """Format a list of flights into lines."""
    lines = []
    rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, flight in enumerate(flights[:max_results], 1):
        price = flight.get("price", 0)
        price_fmt = f"{price:,} VND"
        legs = flight.get("flights", [])
        total_min = flight.get("total_duration", 0)
        h, m = divmod(total_min, 60)
        duration = f"{h}h{m}m" if h else f"{m}m"

        stops, segments = [], []
        for leg in legs:
            airline = leg.get("airline", "?")
            dep_t = leg.get("departure_airport", {}).get("time", "").split()[-1][:5]
            arr_t = leg.get("arrival_airport", {}).get("time", "").split()[-1][:5]
            dep_code = leg.get("departure_airport", {}).get("id", "")
            arr_code = leg.get("arrival_airport", {}).get("id", "")
            flight_no = leg.get("flight_number", "")
            segments.append(f"{dep_t} ({dep_code}) → {arr_t} ({arr_code})")
            stops.append(f"{airline} {flight_no}")

        layovers = flight.get("layovers", [])
        if not layovers:
            transit_info = "Bay thẳng ✅"
        else:
            layover_texts = []
            for lv in layovers:
                if isinstance(lv, dict):
                    name = lv.get("name", "?")
                    dur = lv.get("duration", 0)
                    lh, lm = divmod(dur, 60)
                    dur_str = f"{lh}h{lm}m" if lh else f"{lm}m"
                    layover_texts.append(f"{dur_str} tại {name}")
                else:
                    layover_texts.append(str(lv))
            transit_info = f"{len(layovers)} điểm dừng: {', '.join(layover_texts)}"

        rank_emoji = rank_emojis[min(i - 1, 4)]
        lines.append(f"{rank_emoji} *[{i}] {price_fmt}*")
        lines.append(f"🕒 {' | '.join(segments)}")
        lines.append(f"⏳ {duration} — {transit_info}")
        lines.append(f"🏢 {' → '.join(stops)}")
        lines.append("-" * 40)
    return lines


def _format_oneway(flights: list, dep: str, arr: str, out: str) -> str:
    """Format one-way flight results."""
    dep_name = CITY_MAP.get(dep, dep)
    arr_name = CITY_MAP.get(arr, arr)
    gf_link = f"https://www.google.com/travel/flights?q=Flights+to+{arr}+from+{dep}+on+{out}"

    if not flights:
        return "😕 Không tìm thấy chuyến bay nào cho tuyến này."

    lines = [
        f"✈️ *{dep_name} ({dep}) → {arr_name} ({arr})*",
        f"🛫 Loại vé: Một chiều | 📅 {out}",
        "=" * 40,
    ]
    lines += _format_flight_block(flights)
    lines.append(f"[🔍 Xem thêm trên Google Flights]({gf_link})")
    return "\n".join(lines)


def _format_roundtrip(
    outbound: list, returns: list, dep: str, arr: str, out: str, ret: str
) -> str:
    """Format round-trip flight results (2 one-way blocks)."""
    dep_name = CITY_MAP.get(dep, dep)
    arr_name = CITY_MAP.get(arr, arr)
    gf_out = f"https://www.google.com/travel/flights?q=Flights+to+{arr}+from+{dep}+on+{out}"
    gf_ret = f"https://www.google.com/travel/flights?q=Flights+to+{dep}+from+{arr}+on+{ret}"

    lines = [
        f"✈️ *{dep_name} ({dep}) ⇄ {arr_name} ({arr})*",
        f"📅 Đi: {out} | Về: {ret}",
        "",
    ]

    # Outbound section
    lines.append(f"🛫 *CHIỀU ĐI — {dep_name} → {arr_name}*")
    lines.append("=" * 40)
    if outbound:
        lines += _format_flight_block(outbound)
    else:
        lines.append("😕 Không tìm thấy chuyến đi.")
    lines.append(f"[🔍 Tìm chuyến đi trên Google Flights]({gf_out})")

    lines.append("")

    # Return section
    lines.append(f"🛬 *CHIỀU VỀ — {arr_name} → {dep_name}*")
    lines.append("=" * 40)
    if returns:
        lines += _format_flight_block(returns)
    else:
        lines.append("😕 Không tìm thấy chuyến về.")
    lines.append(f"[🔍 Tìm chuyến về trên Google Flights]({gf_ret})")

    return "\n".join(lines)


def search_shopping(query: str, currency: str = "VND") -> str:
    """Search products via SerpAPI Google Shopping engine.

    Args:
        query: product name to search
        currency: currency for prices

    Returns:
        Formatted product listing with prices, ratings, links
    """
    key = Config.serpapi_key
    params: dict[str, Any] = {
        "engine": "google_shopping",
        "q": query,
        "currency": currency,
        "api_key": key,
    }

    try:
        resp = httpx.get(SERPAPI_BASE, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return f"⚠️ Lỗi search: {e}"

    results = data.get("shopping_results", [])
    if not results:
        return f"😕 Không tìm thấy \"{query}\"."

    lines = [f"🛒 *{query}* ({len(results)} kết quả)", ""]

    # Currency symbol mapping
    currency_symbols = {"VND": "₫", "USD": "$", "SGD": "S$", "JPY": "¥"}

    for i, item in enumerate(results[:6], 1):
        title = item.get("title", "?")
        price = item.get("price", "?")
        source = item.get("source", "?")
        rating = item.get("rating")
        reviews = item.get("reviews", 0)
        delivery = item.get("delivery", "")
        link = item.get("product_link") or item.get("link", "")

        # Rank emoji
        rank = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣"][min(i - 1, 5)]

        # Price highlight
        is_cheapest = i == 1
        price_fmt = f"*{price}* 🔥" if is_cheapest and i <= 3 else f"*{price}*"

        # Rating stars
        stars = ""
        if rating:
            full = int(rating)
            stars = "⭐" * full + f" {rating}" if full > 0 else f"⭐ {rating}"
            if reviews:
                stars += f" ({reviews:,} đánh giá)"

        # Delivery info
        delivery_tag = f" · 🚚 {delivery}" if delivery else ""

        lines.append(f"{rank} {title}")
        lines.append(f"   💰 {price_fmt} — {source}{delivery_tag}")
        if stars:
            lines.append(f"   {stars}")
        if link:
            lines.append(f"   🔗 {link}")
        lines.append("")

    return "\n".join(lines)
