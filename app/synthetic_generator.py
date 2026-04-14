import random
import time
from datetime import datetime, timedelta
from .database import create_db
from .processor import process_event

ROUTES = {
    "E2": ["Harristown", "DCU", "Drumcondra", "OConnell_Street", "St_Stephens_Green", "Donnybrook", "Blackrock", "Dun_Laoghaire"],
    "E1": ["Northwood", "DCU", "Drumcondra", "OConnell_Street", "St_Stephens_Green", "Donnybrook", "Bray"],
    "46A": ["Phoenix_Park", "Heuston", "College_Green", "Donnybrook", "Blackrock"],
    "39A": ["Blanchardstown", "Phibsborough", "OConnell_Street", "UCD"],
}

PASSENGER_BASE = {
    "Harristown": 15,
    "DCU": 35,
    "Drumcondra": 25,
    "OConnell_Street": 55,
    "St_Stephens_Green": 45,
    "Donnybrook": 30,
    "Blackrock": 35,
    "Dun_Laoghaire": 25,
    "Northwood": 15,
    "Bray": 20,
    "Phoenix_Park": 10,
    "Heuston": 30,
    "College_Green": 40,
    "Blanchardstown": 20,
    "Phibsborough": 25,
    "UCD": 30,
}


def generate_event(prev_headway=None):
    from datetime import datetime, timezone 
    now = datetime.now(timezone.utc)

    route_id = random.choice(list(ROUTES.keys()))
    stops = ROUTES[route_id]

    stop_sequence = random.randint(1, len(stops))
    stop_name = stops[stop_sequence - 1]

    # Headway behavior
    if prev_headway is None:
        headway_min = random.uniform(5, 15)
    else:
        drift = random.uniform(-3, 3)
        headway_min = max(1.0, prev_headway + drift)

    # Delay behavior
    delay_sec = random.uniform(-30, 300)

    # Passengers depend partly on stop + delay
    base_passengers = PASSENGER_BASE.get(stop_name, 20)
    waiting_passengers = max(0, int(random.gauss(base_passengers + delay_sec / 20, 10)))

    # Dwell time depends on passengers
    dwell_time_sec = max(10, int(waiting_passengers * random.uniform(1.5, 3.0)))

    actual_arrival = now + timedelta(seconds=delay_sec)
    actual_departure = actual_arrival + timedelta(seconds=dwell_time_sec)

    # Simple schedule assumption
    scheduled_arrival = now

    event = {
        "route_id": route_id,
        "bus_id": f"BUS_{random.randint(100, 999)}",
        "bus_name": f"{route_id}_Bus",
        "stop_sequence": stop_sequence,
        "stop_name": stop_name,
        "scheduled_arrival": scheduled_arrival,
        "actual_arrival": actual_arrival,
        "delay_sec": delay_sec,
        "waiting_passengers": waiting_passengers,
        "dwell_time_sec": dwell_time_sec,
        "actual_departure": actual_departure,
        "headway_min": headway_min,
        "hour": actual_arrival.hour,
    }

    return event, headway_min


def stream_live(generator_delay=1.0):
    create_db()
    print("Starting LIVE synthetic stream...")

    prev_headway = None

    while True:
        event, prev_headway = generate_event(prev_headway)
        processed = process_event(event)

        print(
            f"[{processed['route_id']}] {processed['stop_name']} | "
            f"headway={processed['headway_min']:.2f} | "
            f"status={processed['status']} | "
            f"prob={processed['bunching_probability']:.2f} | "
            f"action={processed['recommended_action']}"
            f"AI: {processed.get('ai_explanation','NOT AVAILABLE' )}\n"
        )

        time.sleep(generator_delay)


if __name__ == "__main__":
    stream_live()