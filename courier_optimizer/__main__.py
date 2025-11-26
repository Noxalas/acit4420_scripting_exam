import os
import sys
import csv
import argparse

from delivery import Delivery
from route_optimizer import optimize_route
from transport import TRANSPORT_MODES
from haversine import get_haversine_distance
from logger import log_time, logging

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
REJECTED_PATH = os.path.join(PACKAGE_ROOT, "rejected.csv")
ROUTE_OUTPUT_PATH = os.path.join(PACKAGE_ROOT, "route.csv")


def calculate_metrics(distance: float, mode: str) -> tuple[float, float, float]:
    """Calculates ETA, Cost, and CO2 for a given distance and transport mode."""
    mode_data = TRANSPORT_MODES[mode]
    speed = mode_data["speed"]
    cost_per_km = mode_data["cost"]
    co2_per_km = mode_data["co2"]

    eta = distance / speed
    cost = distance * cost_per_km
    co2 = distance * co2_per_km
    return eta, cost, co2


@log_time
def main(args):
    # 1. Initial Setup and Validation
    if not os.path.exists(args.input):
        logging.error(f"Input file '{args.input}' not found.")
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    try:
        depot_lat, depot_lon = map(float, args.depot.split(","))
        depot_location = (depot_lat, depot_lon)
    except ValueError:
        logging.error(f"Invalid depot format: '{args.depot}'. Expected lat,lon.")
        print(f"Error: Invalid depot format: '{args.depot}'. Expected lat,lon.")
        sys.exit(1)

    mode = args.mode.title()
    if mode not in TRANSPORT_MODES:
        logging.warning(f"Invalid mode '{args.mode}'. Defaulting to 'Car'.")
        mode = "Car"

    criterion = args.criterion.lower()
    if criterion not in ["time", "cost", "co2"]:
        logging.warning(f"Invalid criterion '{args.criterion}'. Defaulting to 'time'.")
        criterion = "time"

    # 2. Load and Validate Deliveries
    deliveries = []
    rejected_rows = []
    fields = ["customer", "latitude", "longitude", "priority", "weight_kg"]

    try:
        with open(args.input, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if Delivery.validate(row):
                    deliveries.append(Delivery(**row))
                else:
                    rejected_rows.append(row)
    except Exception as e:
        logging.error(f"Error reading input CSV: {e}")
        print(f"Error reading input CSV: {e}")
        sys.exit(1)

    if rejected_rows:
        with open(REJECTED_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rejected_rows)

        logging.warning(f"{len(rejected_rows)} invalid rows written to {REJECTED_PATH}")
        print(f"{len(rejected_rows)} invalid rows written to {REJECTED_PATH}")

    if not deliveries:
        logging.info("No valid deliveries to process. Exiting.")
        print("No valid deliveries to process. Exiting.")
        sys.exit(0)

    print(f"Loaded {len(deliveries)} deliveries.")
    print(f"Transport mode: {mode}, Optimization criterion: {criterion}")

    route = optimize_route(deliveries, depot_location)

    full_route_stops = (
        [
            type(
                "Depot",
                (object,),
                {
                    "latitude": depot_location[0],
                    "longitude": depot_location[1],
                    "customer": "DEPOT_START",
                },
            )
        ]
        + route
        + [
            type(
                "Depot",
                (object,),
                {
                    "latitude": depot_location[0],
                    "longitude": depot_location[1],
                    "customer": "DEPOT_END",
                },
            )
        ]
    )

    total_distance = 0
    total_eta = 0
    total_cost = 0
    total_co2 = 0
    cumulative = 0

    output_rows = []

    for i in range(1, len(full_route_stops)):
        prev_stop = full_route_stops[i - 1]
        current_stop = full_route_stops[i]

        distance = get_haversine_distance(
            float(prev_stop.latitude),
            float(prev_stop.longitude),
            float(current_stop.latitude),
            float(current_stop.longitude),
        )

        eta, cost, co2 = calculate_metrics(distance, mode)

        if i <= len(route) + 1:
            total_distance += distance
            total_eta += eta
            total_cost += cost
            total_co2 += co2

        cumulative += distance

        output_rows.append(
            (
                current_stop.customer,
                round(distance, 2),
                round(cumulative, 2),
                round(eta, 2),
                round(cost, 2),
                round(co2, 2),
            )
        )

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Customer", "Distance_km", "Cumulative_km", "ETA_h", "Cost_NOK", "CO2_g"]
        )
        writer.writerows(output_rows)

    print(f"Route saved to {args.output}")

    print("\n--- Route Summary ---")
    print(f"Transport Mode: {mode}")
    print(f"Optimization Criterion: {criterion.title()}")
    print(f"Total Deliveries: {len(route)}")
    print(f"Total distance (Round trip): {total_distance:.2f} km")
    print(f"Total ETA: {total_eta:.2f} hours")
    print(f"Total cost: {total_cost:.2f} NOK")
    print(f"Total CO2 emissions: {total_co2:.2f} g")
    print("---------------------\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool to optimize delivery routes for NordicExpress."
    )
    parser.add_argument("--input", required=True, help="Input CSV file with deliveries")
    parser.add_argument(
        "--output",
        default=ROUTE_OUTPUT_PATH,
        help="Output CSV file for the optimized route",
    )
    parser.add_argument(
        "--mode", default="Car", help="Transport mode: Car, Bicycle, Walk"
    )
    parser.add_argument(
        "--criterion", default="time", help="Optimization criterion: time, cost, co2"
    )
    parser.add_argument(
        "--depot",
        required=True,
        help="Depot location (Latitude,Longitude, e.g., 59.91,10.75)",
    )

    args = parser.parse_args()

    main(args=args)
