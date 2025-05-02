import time


#  Kitchen fridge – average RH% over the last three hours
def avg_moisture_past_3h(conn):
    with conn.cursor() as cur:
        three_hours_ago_epoch = int(time.time()) - 3 * 3600
        cur.execute(
            """
            SELECT AVG((payload ->> 'Moisture Meter - Moisture Meter') ::NUMERIC)
            FROM "IOT table_virtual"
            WHERE payload->> 'parent_asset_uid' = '005-c3y-7mv-144'
              AND (payload ->> 'timestamp')::BIGINT >= %s
            """,
            (three_hours_ago_epoch,),
        )
        value = cur.fetchone()[0]

    if value is None:
        return "No moisture data available in the past three hours"

    return (
        f"Average Moisture in the kitchen fridge for the past three hours is: "
        f"{value:.2f}% RH (PST)"
    )


#  Dishwasher – average water consumption per cycle
def avg_water_per_cycle(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT AVG((payload ->> 'Capacitive Liquid Level Sensor - water consumption') ::NUMERIC)
            FROM "IOT table_virtual"
            WHERE payload ->> 'parent_asset_uid' = %s
            """,
            ("8mc-1c2-lgd-6wn",),
        )
        ml = cur.fetchone()[0]

    if ml is None:
        return "No water consumption data available"

    gallons = float(ml) * 0.001 * 0.264172
    return f"Average water consumption per cycle: {gallons:.2f} gallons"


#  Compare cumulative electricity usage across three devices

def top_energy_consumer(conn):
    DEVICE_IDS = [
        "005-c3y-7mv-144", 
        "28fa6478-b03b-414f-b6d4-f07472643ad7",  
        "8mc-1c2-lgd-6wn",  
    ]
    placeholders = ",".join(["%s"] * len(DEVICE_IDS))

    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT
              payload->> 'parent_asset_uid' AS device_id,
              SUM(
                    COALESCE((payload->> 'ACS712 - ammeter')::NUMERIC, 0)
                  + COALESCE((payload->> 'ACS712 - ammeter dishwasher')::NUMERIC, 0)
                  + COALESCE((payload->> 'sensor 2 28fa6478-b03b-414f-b6d4-f07472643ad7')::NUMERIC, 0)
              ) AS total_amp_seconds
            FROM "IOT table_virtual"
            WHERE payload->> 'parent_asset_uid' IN ({placeholders})
            GROUP BY payload->> 'parent_asset_uid'
            """,
            DEVICE_IDS,
        )
        rows = cur.fetchall()

    if not rows:
        return "No electricity data available"

    amp_seconds = {dev: float(total) for dev, total in rows}
    kwh = {d: (amps / 3600) * 120.0 / 1000.0 for d, amps in amp_seconds.items()}
    device, usage = max(kwh.items(), key=lambda kv: kv[1])

    NICKNAMES = {
        "005-c3y-7mv-144": "Kitchen Fridge",
        "28fa6478-b03b-414f-b6d4-f07472643ad7": "Garage Fridge",
        "8mc-1c2-lgd-6wn": "Smart Dishwasher",
    }

    return (
        f"The device that consumed the most energy over all time is "
        f"'{NICKNAMES[device]}' with a total of {usage:.3f} kWh."
    )
