import os
import socket
import sys
from contextlib import closing

import psycopg2
from iot_queries import (
    avg_moisture_past_3h,
    avg_water_per_cycle,
    top_energy_consumer,
)

DEVICE_META = {
    "005-c3y-7mv-144": {"name": "Kitchen Fridge",  "location": "Kitchen"},
    "28fa6478-b03b-414f-b6d4-f07472643ad7": {"name": "Garage Fridge",   "location": "Garage"},
    "8mc-1c2-lgd-6wn": {"name": "Smart Dishwasher", "location": "Kitchen"},
}

QUERY_HANDLERS = {
    "what is the average moisture inside my kitchen fridge in the past three hours?": avg_moisture_past_3h,
    "what is the average water consumption per cycle in my smart dishwasher?": avg_water_per_cycle,
    "which device consumed more electricity among my three iot devices?": top_energy_consumer,
}
HELP_TEXT = "\n".join(f"• {q}" for q in QUERY_HANDLERS)


def open_db():
    """Open NeonDB using either an env var or the hard-coded URI."""
    uri = os.getenv(
        "NEON_DB_URI",
        "postgresql://neondb_owner:npg_DT7uBCk2cFQw@ep-tiny-fog-a59x42f5-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require",
    )
    return psycopg2.connect(uri)


def serve(port: int) -> None:
    with closing(open_db()) as db, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("", port))
        sock.listen(1)
        print(f"✅ Server ready on port {port}")

        conn, addr = sock.accept()
        with conn:
            print("🟢 Client connected from", addr)
            while True:
                raw = conn.recv(1024)
                if not raw:
                    print("🔴 Client disconnected")
                    break

                question = raw.decode().strip().lower()
                handler = QUERY_HANDLERS.get(question)

                if handler is None:
                    conn.sendall(
                        (
                            "Sorry, this query cannot be processed.\n"
                            "Please try one of the following:\n"
                            f"{HELP_TEXT}"
                        ).encode()
                    )
                    continue

                try:
                    answer = handler(db)
                except Exception as exc:       
                    answer = f"Internal error while processing your request: {exc}"

                conn.sendall(answer.encode())


if __name__ == "__main__":
    try:
        port_number = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    serve(port_number)
