from .config import GEMINI_API_KEY


def template_explanation(record):
    action = record.get("recommended_action", "NO_ACTION")
    route = record.get("route_id", "unknown")
    stop = record.get("stop_name", "unknown")
    headway = float(record.get("headway_min", 0) or 0)
    prob = float(record.get("bunching_probability", 0) or 0)
    hold = int(record.get("hold_time_sec", 0) or 0)

    if action == "HOLD_BUS":
        return (
            f"Service compression detected on route {route} at {stop}. "
            f"Headway is {headway:.2f} minutes with bunching probability {prob:.2f}. "
            f"Holding the bus for {hold} seconds is recommended to restore spacing."
        )
    elif action == "MONITOR":
        return (
            f"Emerging instability detected on route {route} at {stop}. "
            f"Headway is {headway:.2f} minutes with bunching probability {prob:.2f}. "
            f"Monitoring is recommended."
        )
    else:
        return (
            f"Service is stable on route {route} at {stop}. "
            f"Headway is {headway:.2f} minutes and bunching probability is {prob:.2f}. "
            f"No immediate action is required."
        )


def explain(record):
    print("AI DEBUG: entered explain()")
    print("AI DEBUG: key present =", bool(GEMINI_API_KEY))

    if not GEMINI_API_KEY:
        print("AI DEBUG: no API key")
        return template_explanation(record)

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
You are an operations control assistant for a city bus network.

Analyze the situation and explain it like a professional transport controller.

Focus on:
1. What is happening
2. Why it is happening
3. What action should be taken and why

Keep it concise, specific, and operational.

DATA:
Route: {record.get('route_id')}
Stop: {record.get('stop_name')}
Delay (sec): {record.get('delay_sec')}
Headway (min): {record.get('headway_min')}
Passengers waiting: {record.get('waiting_passengers')}
Dwell time (sec): {record.get('dwell_time_sec')}
Status: {record.get('status')}
Bunching probability: {record.get('bunching_probability')}
Risk band: {record.get('risk_band')}
Recommended action: {record.get('recommended_action')}
Hold time (sec): {record.get('hold_time_sec')}
Priority: {record.get('priority_level')}
"""

        print("AI DEBUG: calling Gemini...")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = getattr(response, "text", None)
        print("AI DEBUG: raw response =", text)

        if text and text.strip():
            return text.strip()

        print("AI DEBUG: empty response -> fallback")
        return template_explanation(record)

    except Exception as e:
        print("AI DEBUG: error =", e)
        return template_explanation(record)

    