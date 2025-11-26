import os
import sys
import csv
import argparse

from delivery import Delivery
from route_optimizer import optimize_route
from transport import TRANSPORT_MODES
from haversine import get_haversine_distance
from logger import log_time, logging
from datetime import datetime

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
REJECTED_PATH = os.path.join(PACKAGE_ROOT, "rejected.csv")


@log_time
def main(args):
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    deliveries = []
    rejected_rows = []

    fields = ["customer", "latitude", "longitude", "priority", "weight_kg"]
    with open(args.input, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if any(field not in row or row[field] == "" for field in fields):
                rejected_rows.append(row)
                continue

            if Delivery.validate(row):
                deliveries.append(Delivery(**row))
            else:
                rejected_rows.append(row)

    if rejected_rows:
        with open(REJECTED_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rejected_rows)

        print(f"{len(rejected_rows)} invalid rows written to {REJECTED_PATH}")

    if not deliveries:
        print("No valid deliveries to process. Exiting.")
        sys.exit(1)

    mode = args.mode.title()
    if mode not in TRANSPORT_MODES:
        print(f"Invalid mode '{args.mode}'. Defaulting to 'Car'.")
        mode = "Car"

    criterion = args.criterion.lower()
    if criterion not in ["time", "cost", "co2"]:
        print(f"Invalid criterion '{args.criterion}'. Defaulting to 'time'.")
        criterion = "time"

    print(f"Loaded {len(deliveries)} deliveries.")
    print(f"Transport mode: {mode}, Optimization criterion: {criterion}")

    route = optimize_route(deliveries, mode, criterion)

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Customer", "Distance_km", "Cumulative_km", "ETA_h", "Cost_NOK", "CO2_g"]
        )
        cumulative = 0
        for i, stop in enumerate(route):
            if i == 0:
                distance = 0
            else:
                distance = get_haversine_distance(
                    float(route[i - 1].latitude),
                    float(route[i - 1].longitude),
                    float(stop.latitude),
                    float(stop.longitude),
                )
            cumulative += distance
            speed = TRANSPORT_MODES[mode]["speed"]
            cost = TRANSPORT_MODES[mode]["cost"] * distance
            co2 = TRANSPORT_MODES[mode]["co2"] * distance
            eta = distance / speed
            writer.writerow(
                [
                    stop.customer,
                    round(distance, 2),
                    round(cumulative, 2),
                    round(eta, 2),
                    round(cost, 2),
                    round(co2, 2),
                ]
            )
    print(f"Route saved to {args.output}")

    # Print summary
    total_distance = sum(
        get_haversine_distance(
            float(route[i - 1].latitude),
            float(route[i - 1].longitude),
            float(route[i].latitude),
            float(route[i].longitude),
        )
        for i in range(1, len(route))
    )
    total_eta = total_distance / TRANSPORT_MODES[mode]["speed"]
    total_cost = total_distance * TRANSPORT_MODES[mode]["cost"]
    total_co2 = total_distance * TRANSPORT_MODES[mode]["co2"]

    print("Route Summary")
    print(f"Total distance: {total_distance:.2f} km")
    print(f"Total ETA: {total_eta:.2f} hours")
    print(f"Total cost: {total_cost:.2f} NOK")
    print(f"Total CO2: {total_co2:.2f} g")

    logging.info(
        f"Optimization run completed. Mode={mode}, Criterion={criterion}, "
        f"Deliveries={len(deliveries)}, Time={datetime.now()}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool to optimize delivery routes for NordicExpress."
    )
    parser.add_argument("--input", required=True, help="Input CSV file with deliveries")
    parser.add_argument(
        "--output", required=True, help="Output CSV file for the optimized route"
    )
    parser.add_argument(
        "--mode", default="Car", help="Transport mode: Car, Bicycle, Walk"
    )
    parser.add_argument(
        "--criterion", default="time", help="Optimization criterion: time, cost, co2"
    )

    args = parser.parse_args()
    main(args)
