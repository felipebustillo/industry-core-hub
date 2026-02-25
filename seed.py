#!/usr/bin/env python3
"""
Seed script for Industry Core Hub backend.
Creates business partners, catalog parts, serialized parts, and twins.

Usage:
    python seed.py [--url http://localhost:9000]
"""

import argparse
import sys
import time
import requests

BASE_URL = "http://localhost:9000"

# ─── Business Partners ───────────────────────────────────────────────────────

BUSINESS_PARTNERS = [
    {"bpnl": "BPNL00000003CRHK", "name": "Catena-X Automotive OEM A"},
    {"bpnl": "BPNL00000003CPIY", "name": "Catena-X Tier-1 Supplier B"},
    {"bpnl": "BPNL4565423555AS", "name": "Volkswagen AG"},
    {"bpnl": "BPNL0000001023XX", "name": "BMW Racing GmbH"},
    {"bpnl": "BPNL5004654513YZ", "name": "BASF SE"},
    {"bpnl": "BPNL856ASD9656AA", "name": "Mercedes-Benz AG"},
    {"bpnl": "BPNL5470544322BB", "name": "Robert Bosch GmbH"},
    {"bpnl": "BPNL00000007RXLP", "name": "ZF Friedrichshafen AG"},
    {"bpnl": "BPNL00000008BFQY", "name": "Continental AG"},
    {"bpnl": "BPNL501TG00870AS", "name": "Brembo S.p.A."},
]

# ─── Catalog Parts ────────────────────────────────────────────────────────────

CATALOG_PARTS = [
    {
        "manufacturerId": "BPNL00000003CRHK",
        "manufacturerPartId": "ENG-V8-4400-001",
        "name": "Engine Block V8 4.4L",
        "category": "Engine",
        "description": "High-performance V8 engine block, 4.4L displacement, aluminum alloy construction. Designed for optimal efficiency and longevity.",
        "materials": [{"name": "Aluminum Alloy 6061", "share": 65.0}, {"name": "Cast Iron", "share": 30.0}, {"name": "Steel Fasteners", "share": 5.0}],
        "weight": {"value": 185.0, "unit": "kg"},
        "width": {"value": 680.0, "unit": "mm"},
        "height": {"value": 720.0, "unit": "mm"},
        "length": {"value": 850.0, "unit": "mm"},
    },
    {
        "manufacturerId": "BPNL5470544322BB",
        "manufacturerPartId": "ALT-T78-14V-002",
        "name": "Alternator Type78 14V 180A",
        "category": "Electrical",
        "description": "High-output alternator engineered for maximum performance. 14V, 180A output with integrated voltage regulator.",
        "materials": [{"name": "Copper Windings", "share": 40.0}, {"name": "Steel Housing", "share": 45.0}, {"name": "Electronic Components", "share": 15.0}],
        "weight": {"value": 7.8, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL856ASD9656AA",
        "manufacturerPartId": "ENG-I6T-3000-003",
        "name": "Turbocharged Inline-6 Motor 3.0L",
        "category": "Engine",
        "description": "High-performance turbocharged inline-six for optimal power and efficiency. Twin-scroll turbocharger, 382 HP output.",
        "materials": [{"name": "Aluminum Alloy", "share": 60.0}, {"name": "Titanium Valves", "share": 5.0}, {"name": "Steel Crankshaft", "share": 35.0}],
        "weight": {"value": 165.0, "unit": "kg"},
        "width": {"value": 520.0, "unit": "mm"},
        "height": {"value": 680.0, "unit": "mm"},
        "length": {"value": 780.0, "unit": "mm"},
    },
    {
        "manufacturerId": "BPNL00000003CRHK",
        "manufacturerPartId": "ENG-V6S-3000-004",
        "name": "Supercharged V6 Motor 3.0L",
        "category": "Engine",
        "description": "Supercharged V6 engine delivering dynamic performance and smooth acceleration. 340 HP, direct fuel injection.",
        "weight": {"value": 152.0, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL00000007RXLP",
        "manufacturerPartId": "TRN-8HP75-005",
        "name": "8HP75 Automatic Transmission",
        "category": "Drivetrain",
        "description": "8-speed automatic transmission tested for high-quality standards. Torque capacity up to 750 Nm.",
        "materials": [{"name": "Steel Gears", "share": 55.0}, {"name": "Aluminum Housing", "share": 30.0}, {"name": "Synthetic Lubricant", "share": 10.0}, {"name": "Electronic Controls", "share": 5.0}],
        "weight": {"value": 87.0, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL501TG00870AS",
        "manufacturerPartId": "BRK-GT6-380-006",
        "name": "GT6 Brake Disc 380mm",
        "category": "Brakes",
        "description": "High-performance ventilated brake disc. Built with precision to ensure maximum durability and reliability. Cross-drilled design.",
        "materials": [{"name": "Carbon Ceramic", "share": 70.0}, {"name": "Steel Hub", "share": 30.0}],
        "weight": {"value": 8.2, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL00000008BFQY",
        "manufacturerPartId": "SUS-ADS-450-007",
        "name": "Adaptive Damping Suspension Module",
        "category": "Suspension",
        "description": "Electronically controlled adaptive damping system. Lightweight yet incredibly strong for enhanced ride comfort and handling.",
        "weight": {"value": 12.5, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL00000003CPIY",
        "manufacturerPartId": "CLG-DS950-008",
        "name": "DS-950 High-Efficiency Radiator",
        "category": "Cooling",
        "description": "Tested to meet the highest industry standards for thermal management. Dual-pass design with aluminum core.",
        "materials": [{"name": "Aluminum Core", "share": 75.0}, {"name": "Plastic End Tanks", "share": 20.0}, {"name": "Rubber Gaskets", "share": 5.0}],
        "weight": {"value": 5.4, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL5470544322BB",
        "manufacturerPartId": "FUL-FP450-009",
        "name": "FP450 High-Pressure Fuel Pump",
        "category": "Fuel System",
        "description": "Direct injection fuel pump. Crafted using high-quality materials for 350 bar operating pressure.",
        "weight": {"value": 1.8, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL5470544322BB",
        "manufacturerPartId": "STR-EPS-350-010",
        "name": "Electric Power Steering Column",
        "category": "Steering",
        "description": "A cutting-edge component designed to optimize steering response and driver feedback. Variable-ratio rack.",
        "weight": {"value": 9.3, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL00000008BFQY",
        "manufacturerPartId": "ELC-BAT-AGM-011",
        "name": "AGM Start-Stop Battery 95Ah",
        "category": "Electrical",
        "description": "Designed for seamless integration with advanced start-stop systems. 95Ah capacity, 850A CCA.",
        "materials": [{"name": "Lead-Acid AGM", "share": 80.0}, {"name": "Polypropylene Case", "share": 15.0}, {"name": "Copper Terminals", "share": 5.0}],
        "weight": {"value": 26.5, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL00000003CPIY",
        "manufacturerPartId": "EXH-SS-DPFE-012",
        "name": "Stainless Steel DPF-Back Exhaust",
        "category": "Exhaust",
        "description": "Manufactured with a focus on sustainability and performance. T304 stainless steel, mandrel-bent construction.",
        "materials": [{"name": "Stainless Steel T304", "share": 85.0}, {"name": "Ceramic Catalyst", "share": 10.0}, {"name": "Titanium Tips", "share": 5.0}],
        "weight": {"value": 14.7, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL856ASD9656AA",
        "manufacturerPartId": "ECU-MDEG3-013",
        "name": "MDEG3 Engine Control Unit",
        "category": "Electronics",
        "description": "Advanced engine management ECU with multi-core processor. OTA update capable, ISO 26262 ASIL-D certified.",
        "weight": {"value": 0.65, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL4565423555AS",
        "manufacturerPartId": "SEN-LIDAR-V2-014",
        "name": "LiDAR Sensor Module V2",
        "category": "ADAS",
        "description": "Long-range LiDAR sensor for autonomous driving applications. 300m range, 0.1 degree angular resolution, 905nm wavelength.",
        "weight": {"value": 1.2, "unit": "kg"},
    },
    {
        "manufacturerId": "BPNL0000001023XX",
        "manufacturerPartId": "BAT-HV-800V-015",
        "name": "800V High-Voltage Battery Pack",
        "category": "EV Powertrain",
        "description": "Next-generation 800V battery pack for electric vehicles. 100 kWh capacity, NMC 811 chemistry, liquid-cooled thermal management.",
        "materials": [{"name": "NMC 811 Cells", "share": 60.0}, {"name": "Aluminum Housing", "share": 25.0}, {"name": "Copper Busbars", "share": 10.0}, {"name": "Thermal Paste", "share": 5.0}],
        "weight": {"value": 450.0, "unit": "kg"},
        "width": {"value": 1500.0, "unit": "mm"},
        "height": {"value": 150.0, "unit": "mm"},
        "length": {"value": 2200.0, "unit": "mm"},
    },
]

# ─── Serialized Parts ─────────────────────────────────────────────────────────

SERIALIZED_PARTS = [
    {"businessPartnerNumber": "BPNL00000003CRHK", "manufacturerId": "BPNL00000003CRHK", "manufacturerPartId": "ENG-V8-4400-001", "partInstanceId": "SN-V8-2025-000001", "van": "WBA3A5C5XFKJ12345", "name": "Engine Block V8 4.4L #1", "category": "Engine"},
    {"businessPartnerNumber": "BPNL00000003CRHK", "manufacturerId": "BPNL00000003CRHK", "manufacturerPartId": "ENG-V8-4400-001", "partInstanceId": "SN-V8-2025-000002", "van": "WBA3A5C5XFKJ12346", "name": "Engine Block V8 4.4L #2", "category": "Engine"},
    {"businessPartnerNumber": "BPNL00000003CRHK", "manufacturerId": "BPNL00000003CRHK", "manufacturerPartId": "ENG-V8-4400-001", "partInstanceId": "SN-V8-2025-000003", "van": "WBA3A5C5XFKJ12347", "name": "Engine Block V8 4.4L #3", "category": "Engine"},
    {"businessPartnerNumber": "BPNL5470544322BB", "manufacturerId": "BPNL5470544322BB", "manufacturerPartId": "ALT-T78-14V-002", "partInstanceId": "SN-ALT78-2025-000001", "name": "Alternator Type78 #1", "category": "Electrical"},
    {"businessPartnerNumber": "BPNL5470544322BB", "manufacturerId": "BPNL5470544322BB", "manufacturerPartId": "ALT-T78-14V-002", "partInstanceId": "SN-ALT78-2025-000002", "name": "Alternator Type78 #2", "category": "Electrical"},
    {"businessPartnerNumber": "BPNL856ASD9656AA", "manufacturerId": "BPNL856ASD9656AA", "manufacturerPartId": "ENG-I6T-3000-003", "partInstanceId": "SN-I6T-2025-000001", "van": "WDB9634031L234567", "name": "Inline-6 Turbo Motor #1", "category": "Engine"},
    {"businessPartnerNumber": "BPNL856ASD9656AA", "manufacturerId": "BPNL856ASD9656AA", "manufacturerPartId": "ENG-I6T-3000-003", "partInstanceId": "SN-I6T-2025-000002", "van": "WDB9634031L234568", "name": "Inline-6 Turbo Motor #2", "category": "Engine"},
    {"businessPartnerNumber": "BPNL00000007RXLP", "manufacturerId": "BPNL00000007RXLP", "manufacturerPartId": "TRN-8HP75-005", "partInstanceId": "SN-8HP75-2025-000001", "name": "8HP75 Transmission #1", "category": "Drivetrain"},
    {"businessPartnerNumber": "BPNL00000007RXLP", "manufacturerId": "BPNL00000007RXLP", "manufacturerPartId": "TRN-8HP75-005", "partInstanceId": "SN-8HP75-2025-000002", "name": "8HP75 Transmission #2", "category": "Drivetrain"},
    {"businessPartnerNumber": "BPNL501TG00870AS", "manufacturerId": "BPNL501TG00870AS", "manufacturerPartId": "BRK-GT6-380-006", "partInstanceId": "SN-GT6-2025-000001", "name": "GT6 Brake Disc #1", "category": "Brakes"},
    {"businessPartnerNumber": "BPNL501TG00870AS", "manufacturerId": "BPNL501TG00870AS", "manufacturerPartId": "BRK-GT6-380-006", "partInstanceId": "SN-GT6-2025-000002", "name": "GT6 Brake Disc #2", "category": "Brakes"},
    {"businessPartnerNumber": "BPNL501TG00870AS", "manufacturerId": "BPNL501TG00870AS", "manufacturerPartId": "BRK-GT6-380-006", "partInstanceId": "SN-GT6-2025-000003", "name": "GT6 Brake Disc #3", "category": "Brakes"},
    {"businessPartnerNumber": "BPNL501TG00870AS", "manufacturerId": "BPNL501TG00870AS", "manufacturerPartId": "BRK-GT6-380-006", "partInstanceId": "SN-GT6-2025-000004", "name": "GT6 Brake Disc #4", "category": "Brakes"},
    {"businessPartnerNumber": "BPNL00000008BFQY", "manufacturerId": "BPNL00000008BFQY", "manufacturerPartId": "SUS-ADS-450-007", "partInstanceId": "SN-ADS450-2025-000001", "name": "Adaptive Damper FL #1", "category": "Suspension"},
    {"businessPartnerNumber": "BPNL00000008BFQY", "manufacturerId": "BPNL00000008BFQY", "manufacturerPartId": "SUS-ADS-450-007", "partInstanceId": "SN-ADS450-2025-000002", "name": "Adaptive Damper FR #2", "category": "Suspension"},
    {"businessPartnerNumber": "BPNL00000003CPIY", "manufacturerId": "BPNL00000003CPIY", "manufacturerPartId": "CLG-DS950-008", "partInstanceId": "SN-DS950-2025-000001", "name": "Radiator DS-950 #1", "category": "Cooling"},
    {"businessPartnerNumber": "BPNL5470544322BB", "manufacturerId": "BPNL5470544322BB", "manufacturerPartId": "FUL-FP450-009", "partInstanceId": "SN-FP450-2025-000001", "name": "Fuel Pump FP450 #1", "category": "Fuel System"},
    {"businessPartnerNumber": "BPNL5470544322BB", "manufacturerId": "BPNL5470544322BB", "manufacturerPartId": "FUL-FP450-009", "partInstanceId": "SN-FP450-2025-000002", "name": "Fuel Pump FP450 #2", "category": "Fuel System"},
    {"businessPartnerNumber": "BPNL4565423555AS", "manufacturerId": "BPNL4565423555AS", "manufacturerPartId": "SEN-LIDAR-V2-014", "partInstanceId": "SN-LIDAR-2025-000001", "name": "LiDAR Sensor V2 #1", "category": "ADAS"},
    {"businessPartnerNumber": "BPNL4565423555AS", "manufacturerId": "BPNL4565423555AS", "manufacturerPartId": "SEN-LIDAR-V2-014", "partInstanceId": "SN-LIDAR-2025-000002", "name": "LiDAR Sensor V2 #2", "category": "ADAS"},
    {"businessPartnerNumber": "BPNL0000001023XX", "manufacturerId": "BPNL0000001023XX", "manufacturerPartId": "BAT-HV-800V-015", "partInstanceId": "SN-HV800-2025-000001", "van": "WBY1Z4C58FVR98765", "name": "800V Battery Pack #1", "category": "EV Powertrain"},
    {"businessPartnerNumber": "BPNL0000001023XX", "manufacturerId": "BPNL0000001023XX", "manufacturerPartId": "BAT-HV-800V-015", "partInstanceId": "SN-HV800-2025-000002", "van": "WBY1Z4C58FVR98766", "name": "800V Battery Pack #2", "category": "EV Powertrain"},
]


def seed_business_partners(session: requests.Session):
    """Create business partners."""
    print("\n=== Seeding Business Partners ===")
    url = f"{BASE_URL}/v1/partner-management/business-partner"
    created = 0
    skipped = 0
    for bp in BUSINESS_PARTNERS:
        try:
            resp = session.post(url, json=bp)
            if resp.status_code in (200, 201):
                print(f"  + {bp['name']} ({bp['bpnl']})")
                created += 1
            elif resp.status_code == 409 or "already exists" in resp.text.lower():
                print(f"  ~ {bp['name']} (already exists)")
                skipped += 1
            else:
                print(f"  ! {bp['name']}: {resp.status_code} {resp.text[:120]}")
                skipped += 1
        except Exception as e:
            print(f"  ! {bp['name']}: {e}")
            skipped += 1
    print(f"  Partners: {created} created, {skipped} skipped")
    return created


def seed_catalog_parts(session: requests.Session):
    """Create catalog parts."""
    print("\n=== Seeding Catalog Parts ===")
    url = f"{BASE_URL}/v1/part-management/catalog-part"
    created = 0
    skipped = 0
    for part in CATALOG_PARTS:
        try:
            resp = session.post(url, json=part)
            if resp.status_code in (200, 201):
                print(f"  + {part['name']} ({part['manufacturerPartId']})")
                created += 1
            elif resp.status_code == 409 or "already exists" in resp.text.lower():
                print(f"  ~ {part['name']} (already exists)")
                skipped += 1
            else:
                print(f"  ! {part['name']}: {resp.status_code} {resp.text[:120]}")
                skipped += 1
        except Exception as e:
            print(f"  ! {part['name']}: {e}")
            skipped += 1
    print(f"  Catalog parts: {created} created, {skipped} skipped")
    return created


def seed_serialized_parts(session: requests.Session):
    """Create serialized (instance) parts."""
    print("\n=== Seeding Serialized Parts ===")
    url = f"{BASE_URL}/v1/part-management/serialized-part"
    created = 0
    skipped = 0
    for part in SERIALIZED_PARTS:
        try:
            resp = session.post(url, json=part)
            if resp.status_code in (200, 201):
                print(f"  + {part.get('name', part['partInstanceId'])}")
                created += 1
            elif resp.status_code == 409 or "already exists" in resp.text.lower():
                print(f"  ~ {part.get('name', part['partInstanceId'])} (already exists)")
                skipped += 1
            else:
                print(f"  ! {part.get('name', part['partInstanceId'])}: {resp.status_code} {resp.text[:120]}")
                skipped += 1
        except Exception as e:
            print(f"  ! {part.get('name', part['partInstanceId'])}: {e}")
            skipped += 1
    print(f"  Serialized parts: {created} created, {skipped} skipped")
    return created


def seed_catalog_part_twins(session: requests.Session):
    """Create digital twins for catalog parts."""
    print("\n=== Seeding Catalog Part Twins ===")
    url = f"{BASE_URL}/v1/twin-management/catalog-part-twin"
    created = 0
    skipped = 0
    for part in CATALOG_PARTS:
        twin = {
            "manufacturerId": part["manufacturerId"],
            "manufacturerPartId": part["manufacturerPartId"],
        }
        try:
            resp = session.post(url, json=twin)
            if resp.status_code in (200, 201):
                print(f"  + Twin for {part['name']}")
                created += 1
            elif resp.status_code == 409 or "already exists" in resp.text.lower():
                print(f"  ~ Twin for {part['name']} (already exists)")
                skipped += 1
            else:
                print(f"  ! Twin for {part['name']}: {resp.status_code} {resp.text[:120]}")
                skipped += 1
        except Exception as e:
            print(f"  ! Twin for {part['name']}: {e}")
            skipped += 1
    print(f"  Twins: {created} created, {skipped} skipped")
    return created


def seed_serialized_part_twins(session: requests.Session):
    """Create digital twins for serialized parts."""
    print("\n=== Seeding Serialized Part Twins ===")
    url = f"{BASE_URL}/v1/twin-management/serialized-part-twin"
    created = 0
    skipped = 0
    for part in SERIALIZED_PARTS:
        twin = {
            "manufacturerId": part["manufacturerId"],
            "manufacturerPartId": part["manufacturerPartId"],
            "partInstanceId": part["partInstanceId"],
        }
        try:
            resp = session.post(url, json=twin)
            if resp.status_code in (200, 201):
                print(f"  + Twin for {part.get('name', part['partInstanceId'])}")
                created += 1
            elif resp.status_code == 409 or "already exists" in resp.text.lower():
                print(f"  ~ Twin for {part.get('name', part['partInstanceId'])} (already exists)")
                skipped += 1
            else:
                print(f"  ! Twin for {part.get('name', part['partInstanceId'])}: {resp.status_code} {resp.text[:120]}")
                skipped += 1
        except Exception as e:
            print(f"  ! Twin for {part.get('name', part['partInstanceId'])}: {e}")
            skipped += 1
    print(f"  Twins: {created} created, {skipped} skipped")
    return created


def verify_data(session: requests.Session):
    """Verify seeded data by reading back counts."""
    print("\n=== Verification ===")
    checks = [
        ("Business Partners", "/v1/partner-management/business-partner"),
        ("Catalog Parts", "/v1/part-management/catalog-part"),
        ("Serialized Parts", "/v1/part-management/serialized-part"),
        ("Catalog Part Twins", "/v1/twin-management/catalog-part-twin"),
        ("Serialized Part Twins", "/v1/twin-management/serialized-part-twin"),
    ]
    for label, path in checks:
        try:
            resp = session.get(f"{BASE_URL}{path}")
            if resp.status_code == 200:
                data = resp.json()
                count = len(data) if isinstance(data, list) else "?"
                print(f"  {label}: {count} records")
            else:
                print(f"  {label}: HTTP {resp.status_code}")
        except Exception as e:
            print(f"  {label}: {e}")


def main():
    global BASE_URL

    parser = argparse.ArgumentParser(description="Seed ICHub backend with sample data")
    parser.add_argument("--url", default=BASE_URL, help=f"Backend URL (default: {BASE_URL})")
    args = parser.parse_args()

    BASE_URL = args.url.rstrip("/")

    print(f"Seeding ICHub backend at {BASE_URL}")
    print("=" * 60)

    # Check health
    session = requests.Session()
    session.headers["Content-Type"] = "application/json"

    try:
        resp = session.get(f"{BASE_URL}/health")
        if resp.status_code != 200:
            print(f"Backend not healthy: {resp.status_code}")
            sys.exit(1)
        print(f"Backend health: OK")
    except requests.ConnectionError:
        print(f"Cannot connect to {BASE_URL}")
        sys.exit(1)

    start = time.time()

    seed_business_partners(session)
    seed_catalog_parts(session)
    seed_serialized_parts(session)
    seed_catalog_part_twins(session)
    seed_serialized_part_twins(session)

    elapsed = time.time() - start
    print(f"\n{'=' * 60}")
    print(f"Seeding completed in {elapsed:.1f}s")

    verify_data(session)
    print()


if __name__ == "__main__":
    main()
