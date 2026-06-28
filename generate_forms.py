from __future__ import annotations

import os
import random
from datetime import date, timedelta
from pathlib import Path

import pymupdf

MAX_MEMBERS = 6
LEVY_AMOUNTS = (259, 518)

TITLES = ["Mr", "Mrs", "Ms", "Dr", "Miss"]
FIRST_NAMES = [
    "James",
    "Sarah",
    "Michael",
    "Emma",
    "David",
    "Lisa",
    "Robert",
    "Karen",
    "William",
    "Jennifer",
    "John",
    "Patricia",
    "Thomas",
    "Susan",
    "Mark",
    "Jessica",
    "Andrew",
    "Helen",
    "Peter",
    "Catherine",
    "Paul",
    "Margaret",
    "Steven",
    "Elizabeth",
    "Brian",
    "Christine",
    "Kevin",
    "Rebecca",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Miller",
    "Davis",
    "Wilson",
    "Taylor",
    "Anderson",
    "Thomas",
    "Jackson",
    "White",
    "Harris",
    "Martin",
    "Thompson",
    "Garcia",
    "Martinez",
    "Robinson",
    "Clark",
    "Rodriguez",
    "Lewis",
    "Lee",
    "Walker",
    "Hall",
    "Allen",
    "Young",
    "King",
]
PRACTICES = [
    "ABC Accounting",
    "Smith & Associates",
    "Premier Tax Solutions",
    "Wealth Advisory Group",
    "Total SMSF Services",
    "Henderson Partners",
    "Blue Sky Accounting",
    "Pinnacle Tax & Super",
    "Accord Financial",
]
BANKS = [
    "Commonwealth Bank",
    "ANZ Bank",
    "Westpac",
    "NAB",
    "Macquarie Bank",
    "Bendigo Bank",
    "Suncorp Bank",
    "Bank of Queensland",
]
ESA_ALIASES = [
    "SMSFAUSTRALIA",
    "BGLSMSF",
    "CLASSSMSF",
    "SUPERFUND",
    "HEFFRON",
    "MCLOWD",
    "SIMPLE FUND",
    "SELFMANAGEDSUPER",
]
STREETS = [
    "Main Street",
    "King Street",
    "High Street",
    "George Street",
    "Park Road",
    "Church Street",
    "Station Road",
    "Victoria Avenue",
]
SUBURBS = [
    "Sydney",
    "Melbourne",
    "Brisbane",
    "Perth",
    "Adelaide",
    "Canberra",
    "Hobart",
    "Newcastle",
]
STATES = ["NSW", "VIC", "QLD", "WA", "SA", "ACT", "TAS"]


def rand_tfn():
    """Generate an 8 or 9 digit TFN."""
    length = random.choice([8, 9])
    digits = [str(random.randint(0, 9)) for _ in range(length)]
    digits[0] = str(random.randint(1, 9))
    return "".join(digits)


def rand_abn():
    digits = [str(random.randint(0, 9)) for _ in range(11)]
    digits[0] = str(random.randint(1, 9))
    return "".join(digits)


def rand_bsb():
    return f"{random.randint(100, 999)}{random.randint(100, 999)}"


def rand_account():
    return str(random.randint(10000000, 999999999))


def rand_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def rand_phone():
    return f"0{random.randint(2, 4)}{random.randint(10000000, 99999999)}"


def rand_email(first, last):
    domains = ["gmail.com", "outlook.com", "bigpond.com", "hotmail.com", "icloud.com"]
    return f"{first.lower()}.{last.lower()}@{random.choice(domains)}"


def rand_fund_name(last1, last2=None):
    suffixes = ["Superannuation Fund", "Super Fund", "Retirement Fund", "SMSF"]
    if last2 and random.random() > 0.5:
        return f"{last1} & {last2} {random.choice(suffixes)}"
    return f"{last1} Family {random.choice(suffixes)}"


def rand_amount(min_value, max_value):
    return f"{random.uniform(min_value, max_value):,.2f}"


def rand_whole(min_value, max_value):
    return f"{random.randint(min_value, max_value):,}"


def rand_date(start_year=2023, end_year=2024):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    chosen = start + timedelta(days=random.randint(0, (end - start).days))
    return chosen.strftime("%d/%m/%Y")


def maybe_tfn():
    return rand_tfn() if random.random() < 0.3 else "Provided"


def maybe_numeric(min_value, max_value, *, whole=True, blank_probability=0.35):
    if random.random() < blank_probability:
        return "", 0 if whole else 0.0
    if whole:
        value = random.randint(min_value, max_value)
        return f"{value:,}", float(value)
    value = round(random.uniform(min_value, max_value), 2)
    return f"{value:,.2f}", value


def format_value(text):
    return str(text) if text is not None else ""


def generate_member(index):
    first, last = rand_name()
    other = random.choice([name for name in FIRST_NAMES if name != first])
    title = random.choice(TITLES)
    opening = round(random.uniform(75000, 750000), 2)

    contributions = {}
    total_contributions = 0.0
    for code, minimum, maximum, blank_probability in [
        ("A", 1000, 60000, 0.25),
        ("B", 1000, 30000, 0.45),
        ("C", 10000, 200000, 0.85),
        ("D", 10000, 300000, 0.9),
        ("E", 5000, 150000, 0.9),
        ("F", 1000, 30000, 0.7),
        ("G", 1000, 25000, 0.8),
        ("H", 10000, 250000, 0.88),
        ("I", 1000, 60000, 0.85),
        ("J", 1000, 60000, 0.85),
        ("K", 1000, 50000, 0.85),
        ("L", 1000, 50000, 0.88),
        ("T", 1000, 30000, 0.95),
        ("M", 1000, 25000, 0.55),
    ]:
        shown, numeric = maybe_numeric(minimum, maximum, whole=False, blank_probability=blank_probability)
        contributions[code] = shown
        total_contributions += numeric

    employer_abn = rand_abn() if contributions["A"] else ""
    residence_date = rand_date() if contributions["H"] else ""
    allocated = round(random.uniform(-25000, 65000), 2)
    inward = 0.0 if random.random() < 0.45 else round(random.uniform(5000, 200000), 2)
    outward = 0.0 if random.random() < 0.65 else round(random.uniform(5000, 100000), 2)
    lump_sum = 0.0 if random.random() < 0.75 else round(random.uniform(5000, 75000), 2)
    income_stream = 0.0 if random.random() < 0.72 else round(random.uniform(5000, 65000), 2)
    closing = max(0.0, opening + total_contributions + allocated + inward - outward - lump_sum - income_stream)

    retirement_total = 0.0 if random.random() < 0.55 else round(closing * random.uniform(0.15, 0.55), 2)
    cdbis = 0.0 if retirement_total == 0 else round(retirement_total * random.uniform(0.0, 0.35), 2)
    non_cdbis = round(retirement_total - cdbis, 2)
    accumulation = round(closing - retirement_total, 2)
    lrba = 0.0 if random.random() < 0.65 else round(closing * random.uniform(0.05, 0.35), 2)
    tris_count = 0 if retirement_total == 0 else random.randint(0, 2)

    def money(value):
        return f"{value:,.2f}" if value else ""

    return {
        "title": title,
        "family_name": last,
        "first_name": first,
        "other_names": other,
        "tfn": maybe_tfn(),
        "dob": "Provided",
        "opening_balance": f"{opening:,.2f}",
        "contributions": contributions,
        "employer_abn": employer_abn,
        "residence_date": residence_date,
        "total_contributions": f"{total_contributions:,.2f}",
        "allocated_earnings": money(abs(allocated)),
        "allocated_loss": allocated < 0,
        "inward_rollovers": money(inward),
        "outward_rollovers": money(outward),
        "lump_sum": money(lump_sum),
        "lump_sum_code": random.choice(["R", "S", "U"]) if lump_sum else "",
        "income_stream": money(income_stream),
        "income_stream_code": random.choice(["A", "B", "C"]) if income_stream else "",
        "accumulation_balance": f"{accumulation:,.2f}",
        "retirement_non_cdbis": f"{non_cdbis:,.2f}" if non_cdbis else "",
        "retirement_cdbis": f"{cdbis:,.2f}" if cdbis else "",
        "tris_count": str(tris_count) if tris_count else "",
        "closing_balance": f"{closing:,.2f}",
        "x1": f"{accumulation:,.2f}",
        "x2": f"{retirement_total:,.2f}" if retirement_total else "",
        "lrba": money(lrba),
    }


def build_form_data(num_members):
    first1, last1 = rand_name()
    first2, last2 = rand_name()
    fund_name = rand_fund_name(last1, last2)
    tfn_value = maybe_tfn()
    address = {
        "street": f"{random.randint(1, 250)} {random.choice(STREETS)}",
        "suburb": random.choice(SUBURBS),
        "state": random.choice(STATES),
        "postcode": f"{random.randint(2000, 7999)}",
    }
    auditor_first, auditor_last = rand_name()
    bank_name = random.choice(BANKS)
    second_bank_name = random.choice(BANKS)
    ecpi_yes = random.random() < 0.45
    ecpi_amount = random.randint(5000, 85000) if ecpi_yes else 0

    income_values = {}
    income_specs = [
        ("A", 500, 55000),
        ("B", 1000, 120000),
        ("C", 500, 85000),
        ("X", 0, 10000),
        ("D1", 500, 25000),
        ("D", 500, 30000),
        ("E", 0, 5000),
        ("F", 0, 40000),
        ("H", 0, 18000),
        ("R1", 0, 50000),
        ("R2", 0, 50000),
        ("R3", 0, 50000),
        ("R6", 0, 50000),
        ("U1", 0, 50000),
        ("U2", 0, 50000),
        ("U3", 0, 50000),
        ("I", 0, 90000),
        ("J", 0, 80000),
        ("K", 0, 70000),
        ("L", 0, 70000),
        ("M", 0, 70000),
        ("S", 0, 25000),
        ("T", 0, 25000),
    ]
    for code, minimum, maximum in income_specs:
        blank_probability = 0.25 if code in {"B", "C", "I"} else 0.45
        shown, numeric = maybe_numeric(minimum, maximum, whole=True, blank_probability=blank_probability)
        income_values[code] = {"text": shown, "value": numeric}

    gross_income = sum(income_values[code]["value"] for code in ["B", "C", "X", "D", "F", "H", "I", "J", "K", "L", "M", "S", "T"])
    ecpi_total = float(ecpi_amount)
    assessable_income = gross_income + income_values["A"]["value"] + income_values["D1"]["value"] + income_values["E"]["value"]
    assessable_income += income_values["R1"]["value"] + income_values["R2"]["value"] + income_values["R3"]["value"] + income_values["R6"]["value"]
    assessable_income += income_values["U1"]["value"] + income_values["U2"]["value"] + income_values["U3"]["value"] - ecpi_total
    assessable_income = max(0.0, assessable_income)

    deduction_pairs = {}
    deduction_total = 0
    nondeductible_total = 0
    for code in ["A", "B", "D", "E", "F", "H", "I", "J", "U", "L"]:
        left, left_numeric = maybe_numeric(0, 20000, whole=True, blank_probability=0.35)
        right, right_numeric = maybe_numeric(0, 15000, whole=True, blank_probability=0.5)
        deduction_pairs[f"{code}1"] = left
        deduction_pairs[f"{code}2"] = right
        deduction_total += int(round(left_numeric))
        nondeductible_total += int(round(right_numeric))
    m1, m1_numeric = maybe_numeric(0, 12000, whole=True, blank_probability=0.45)
    deduction_pairs["M1"] = m1
    deduction_total += int(round(m1_numeric))

    taxable_income = max(0, int(round(assessable_income)) - deduction_total)
    tax_on_income = int(round(taxable_income * 0.15))
    no_tfn_tax = 0 if random.random() < 0.75 else random.randint(500, 12000)
    gross_tax = tax_on_income + no_tfn_tax
    c1 = random.randint(0, 5000)
    c2 = random.randint(0, 3000)
    c_total = c1 + c2
    subtotal1 = max(0, gross_tax - c_total)
    carry_forwards = [random.randint(0, 2000) for _ in range(4)]
    carry_total = sum(carry_forwards)
    subtotal2 = max(0, subtotal1 - carry_total)
    refundable_offsets = [random.randint(0, 2500) for _ in range(4)]
    refundable_total = sum(refundable_offsets)
    tax_payable = max(0, subtotal2 - refundable_total)
    interest_charge = 0 if random.random() < 0.8 else random.randint(50, 1000)

    eligible_credits = [random.randint(0, 5000) for _ in range(5)]
    eligible_credit_total = sum(eligible_credits)
    tax_offset_refunds = random.randint(0, 3000)
    payg_instalments = random.randint(0, 4000)
    levy = random.choice(LEVY_AMOUNTS)
    levy_adjustment_m = random.randint(0, 500)
    levy_adjustment_n = random.randint(0, 500)
    total_charges = tax_payable + interest_charge + levy + levy_adjustment_m
    total_credits = eligible_credit_total + tax_offset_refunds + payg_instalments + levy_adjustment_n
    amount_due = total_charges - total_credits

    members = [generate_member(i) for i in range(num_members)]

    return {
        "tfn": tfn_value,
        "fund_name": fund_name,
        "abn": rand_abn(),
        "address": address,
        "annual_return_amendment": random.random() < 0.2,
        "annual_return_first": random.random() < 0.3,
        "auditor": {
            "family_name": auditor_last,
            "first_name": auditor_first,
            "san": rand_whole(10000000, 99999999),
            "phone": rand_phone(),
            "postal_address": f"{random.randint(1, 250)} {random.choice(STREETS)}, {random.choice(SUBURBS)} {random.choice(STATES)} {random.randint(2000, 7999)}",
            "part_a_qualified": random.random() < 0.25,
            "part_b_qualified": random.random() < 0.25,
            "part_b_rectified": random.random() < 0.7,
        },
        "eft": {
            "fund_bank": bank_name,
            "fund_bsb": rand_bsb(),
            "fund_account": rand_account(),
            "fund_account_name": fund_name,
            "fund_refund_check": random.random() < 0.75,
            "refund_bank": second_bank_name,
            "refund_bsb": rand_bsb(),
            "refund_account": rand_account(),
            "refund_account_name": fund_name,
            "esa": random.choice(ESA_ALIASES),
        },
        "status": {
            "type": random.choice(["regulated", "other"]),
            "benefit_structure": random.choice(["accumulation", "mixture"]),
            "co_contribution": random.choice([True, False]),
            "wound_up": random.random() < 0.1,
            "wound_up_date": rand_date() if random.random() < 0.1 else "",
            "tax_obligations_met": random.choice([True, False]),
            "ecpi_yes": ecpi_yes,
            "ecpi_amount": f"{ecpi_amount:,}" if ecpi_amount else "",
            "ecpi_method": random.choice(["segregated", "unsegregated"]) if ecpi_yes else "",
            "actuarial_certificate": ecpi_yes and random.random() < 0.55,
        },
        "income": income_values,
        "gross_income": f"{int(round(gross_income)):,}",
        "ecpi_total": f"{int(ecpi_total):,}" if ecpi_total else "",
        "assessable_income": f"{int(round(assessable_income)):,}",
        "deductions": deduction_pairs,
        "deduction_total": f"{deduction_total:,}",
        "nondeductible_total": f"{nondeductible_total:,}",
        "taxable_income": f"{taxable_income:,}",
        "expense_total": f"{deduction_total + nondeductible_total:,}",
        "tax": {
            "A": f"{taxable_income:,}",
            "T1": f"{tax_on_income:,}",
            "J": f"{no_tfn_tax:,}" if no_tfn_tax else "",
            "B": f"{gross_tax:,}",
            "C1": f"{c1:,}" if c1 else "",
            "C2": f"{c2:,}" if c2 else "",
            "C": f"{c_total:,}" if c_total else "",
            "T2": f"{subtotal1:,}",
            "D1": f"{carry_forwards[0]:,}" if carry_forwards[0] else "",
            "D2": f"{carry_forwards[1]:,}" if carry_forwards[1] else "",
            "D3": f"{carry_forwards[2]:,}" if carry_forwards[2] else "",
            "D4": f"{carry_forwards[3]:,}" if carry_forwards[3] else "",
            "D": f"{carry_total:,}" if carry_total else "",
            "T3": f"{subtotal2:,}",
            "E1": f"{refundable_offsets[0]:,}" if refundable_offsets[0] else "",
            "E2": f"{refundable_offsets[1]:,}" if refundable_offsets[1] else "",
            "E3": f"{refundable_offsets[2]:,}" if refundable_offsets[2] else "",
            "E4": f"{refundable_offsets[3]:,}" if refundable_offsets[3] else "",
            "E": f"{refundable_total:,}" if refundable_total else "",
            "T5": f"{tax_payable:,}",
            "G": f"{interest_charge:,}" if interest_charge else "",
        },
        "continued_tax": {
            "H2": f"{eligible_credits[0]:,}" if eligible_credits[0] else "",
            "H3": f"{eligible_credits[1]:,}" if eligible_credits[1] else "",
            "H5": f"{eligible_credits[2]:,}" if eligible_credits[2] else "",
            "H6": f"{eligible_credits[3]:,}" if eligible_credits[3] else "",
            "H8": f"{eligible_credits[4]:,}" if eligible_credits[4] else "",
            "H": f"{eligible_credit_total:,}" if eligible_credit_total else "",
            "I": f"{tax_offset_refunds:,}" if tax_offset_refunds else "",
            "K": f"{payg_instalments:,}" if payg_instalments else "",
            "L": f"{levy:,}",
            "M": f"{levy_adjustment_m:,}" if levy_adjustment_m else "",
            "N": f"{levy_adjustment_n:,}" if levy_adjustment_n else "",
            "S": f"{abs(amount_due):,}",
            "refund": amount_due < 0,
        },
        "losses": {
            "U": rand_whole(0, 50000),
            "V": rand_whole(0, 50000),
        },
        "members": members,
        "assets": _generate_assets(),
        "liabilities": _generate_liabilities(members),
        "declarations": _generate_declarations(),
    }


def _rand_asset_amount():
    return maybe_numeric(10000, 2000000, whole=True)[0]


def _generate_assets():
    a = _rand_asset_amount
    return {
        "15a-a": a(),
        "15a-b": a(),
        "15a-c": a(),
        "15a-d": a(),
        "15b-e": a(),
        "15b-f": a(),
        "15b-g": a(),
        "15b-h": a(),
        "15b-i": a(),
        "15b-j1": a(),
        "15b-j2": a(),
        "15b-js": a(),
        "15b-j4": a(),
        "15b-j5": a(),
        "15b-j6": a(),
        "15b-j7": a(),
        "15b-j": a(),
        "15b-k": a(),
        "15b-l": a(),
        "15b-m": a(),
        "15b-0": a(),
        "15c-n": a(),
        "Text34": a(),
        "Text35": a(),
        "Text36": a(),
        "Text37": a(),
        "Text38": a(),
        "Text39": a(),
        "15e": a(),
    }


def _generate_liabilities(members):
    v1, v1_num = maybe_numeric(0, 500000, whole=True)
    v2, v2_num = maybe_numeric(0, 200000, whole=True)
    v3, v3_num = maybe_numeric(0, 100000, whole=True)
    v_total = int(v1_num + v2_num + v3_num)
    members_total = int(sum(
        float(m["closing_balance"].replace(",", ""))
        for m in members
    ))
    return {
        "16-v1": v1,
        "16-v2": v2,
        "16-v3": v3,
        "16v": f"{v_total:,}" if v_total else "",
        "16w": f"{members_total:,}",
        "16x": maybe_numeric(0, 400000, whole=True)[0],
        "16y": maybe_numeric(0, 300000, whole=True)[0],
        "16z": maybe_numeric(0, 1000000, whole=True)[0],
    }


def _generate_declarations():
    trustee_first, trustee_last = rand_name()
    trustee_other = random.choice([n for n in FIRST_NAMES if n != trustee_first])
    is_corporate = random.random() < 0.4
    agent_first, agent_last = rand_name()
    agent_other = random.choice([n for n in FIRST_NAMES if n != agent_first])
    tan_number = str(random.randint(10000000, 99999999))
    return {
        "trustee-family-name": trustee_last,
        "trustee-first-name": trustee_first,
        "trustee-other-name": trustee_other,
        "trustee-phone": rand_phone(),
        "trustee-email": rand_email(trustee_first, trustee_last),
        "trustee-corporate": f"{trustee_last} Pty Ltd" if is_corporate else "",
        "trustee-corp-abn": rand_abn() if is_corporate else "",
        "tax-agent-family-name": agent_last,
        "tax-agent-first-name": agent_first,
        "tax-agent-other-name": agent_other,
        # NOTE: "Tax agents practice" is the exact field name defined in the PDF template.
        "Tax agents practice": random.choice(PRACTICES),
        "tan-phone": rand_phone(),
        "tan-ref": f"REF{random.randint(10000, 99999)}",
        "tan": tan_number,
    }


def _set_field(page, field_name, value):
    """Set a text field value on a PDF page."""
    for widget in page.widgets():
        if widget.field_name == field_name:
            widget.field_value = str(value) if value is not None else ""
            widget.update()
            return


def _set_radio(page, field_name, export_value):
    """Set a radio button group to the given export value."""
    for widget in page.widgets():
        if widget.field_name == field_name:
            widget.field_value = export_value
            widget.update()
            return


def build_pdf(output_path, num_members):
    template_path = Path(__file__).parent / "SMSFAR 2024-smart form.pdf"
    data = build_form_data(num_members)

    doc = pymupdf.open(str(template_path))

    # Page 1 — Fund information
    page = doc[0]
    _set_field(page, "tfn", data["tfn"])
    _set_field(page, "smsf-name", data["fund_name"])
    _set_field(page, "abn", data["abn"])

    # Page 2 — Auditor / EFT details
    page = doc[1]
    eft = data["eft"]
    _set_field(page, "ss-bsb", eft["fund_bsb"])
    _set_field(page, "ss-acc", eft["fund_account"])
    _set_field(page, "ss-acc-name", eft["fund_account_name"])
    _set_field(page, "ref-bsb", eft["refund_bsb"])
    _set_field(page, "ref-acc", eft["refund_account"])
    _set_field(page, "ref-acc-name", eft["refund_account_name"])
    _set_field(page, "esa", eft["esa"])
    aud = data["auditor"]
    _set_radio(page, "aud-parta-qual", "Yes" if aud["part_a_qualified"] else "No")
    _set_radio(page, "aud-partb-qual", "Yes" if aud["part_b_qualified"] else "No")
    _set_radio(page, "aud-partb-qual-yes", "Yes" if aud["part_b_rectified"] else "No")

    # Page 3 — Status / ECPI
    page = doc[2]
    status = data["status"]
    _set_field(page, "ECPI", status["ecpi_amount"])
    _set_radio(page, "ecpi-yes/no", "Yes" if status["ecpi_yes"] else "No")
    if status["ecpi_yes"]:
        # NOTE: "Seggregated"/"Unsegreggated" are the exact export values defined in the
        # PDF template (the form itself contains these typos); they must match exactly.
        pension_val = "Seggregated" if status["ecpi_method"] == "segregated" else "Unsegreggated"
        _set_radio(page, "pension-method", pension_val)
        _set_radio(page, "ecpi-other-asses", "Yes")
    if status["actuarial_certificate"]:
        _set_radio(page, "act-cert", "Yes")

    # Page 5 — Deductions (J1/J2 admin expenses)
    page = doc[4]
    _set_field(page, "j1-admin-exp", data["deductions"].get("J1", ""))
    _set_field(page, "j2-admin-exp", data["deductions"].get("J2", ""))

    # Page 7 — Losses (carry-forward)
    page = doc[6]
    _set_field(page, "cfl-tax", data["losses"]["U"])
    _set_field(page, "cfl-cg", data["losses"]["V"])

    # Pages 8–13 — Members 1–6
    for n in range(1, MAX_MEMBERS + 1):
        page = doc[7 + (n - 1)]
        member = data["members"][n - 1] if n <= num_members else None
        pfx = f"mem{n}"
        nc_field_suffix = "ncsbis" if n == 1 else "ncdbis"  # mem1 uses ncsbis; mem2-6 use ncdbis
        _set_field(page, f"{pfx}-ls", member["lump_sum"] if member else "")
        _set_field(page, f"{pfx}-is", member["income_stream"] if member else "")
        _set_field(page, f"{pfx}-acc", member["accumulation_balance"] if member else "")
        _set_field(page, f"{pfx}-{nc_field_suffix}", member["retirement_non_cdbis"] if member else "")
        _set_field(page, f"{pfx}-cdbis", member["retirement_cdbis"] if member else "")
        _set_field(page, f"{pfx}-tris", member["tris_count"] if member else "")
        _set_field(page, f"{pfx}-bal", member["closing_balance"] if member else "")
        _set_field(page, f"{pfx}-accbal", member["x1"] if member else "")
        _set_field(page, f"{pfx}-retbal", member["x2"] if member else "")
        _set_field(page, f"{pfx}-lrba", member["lrba"] if member else "")

    # Page 20 — Assets
    page = doc[19]
    for field_name, value in data["assets"].items():
        _set_field(page, field_name, value)

    # Page 21 — Liabilities
    page = doc[20]
    for field_name, value in data["liabilities"].items():
        _set_field(page, field_name, value)

    # Page 22 — Declarations
    page = doc[21]
    for field_name, value in data["declarations"].items():
        _set_field(page, field_name, value)

    doc.save(str(output_path), incremental=False, encryption=pymupdf.PDF_ENCRYPT_NONE)
    return data["tfn"]


def main():
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    for members in range(1, MAX_MEMBERS + 1):
        for index in range(1, 3):
            output_path = output_dir / f"smsf_return_{members}members_{index}.pdf"
            tfn_value = build_pdf(output_path, members)
            relative_path = os.path.relpath(output_path, Path(__file__).resolve().parent)
            summary_tfn = "Provided" if tfn_value == "Provided" else "Recorded"
            print(f"Generated: {relative_path}  ({members} members, TFN: {summary_tfn})")

    print("\nAll 12 PDFs generated in the 'output' folder.")


if __name__ == "__main__":
    main()

