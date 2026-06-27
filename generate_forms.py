from __future__ import annotations

import os
import random
from datetime import date, timedelta
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 2 * cm
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN)
BODY_FONT = "Helvetica"
BOLD_FONT = "Helvetica-Bold"
BODY_SIZE = 9
LABEL_SIZE = 7
HEADER_SIZE = 11
TITLE_SIZE = 16
BOX_HEIGHT = 15
FIELD_GAP = 18
TOTAL_PAGES = 13

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
    "SIMPLEFUND",
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
        return "", 0.0
    if whole:
        value = random.randint(min_value, max_value)
        return f"{value:,}", float(value)
    value = round(random.uniform(min_value, max_value), 2)
    return f"{value:,.2f}", value


def measure(text):
    return str(text) if text is not None else ""


def t(value):
    return PAGE_HEIGHT - MARGIN - value


def draw_footer(pdf, page_number):
    pdf.setFont(BODY_FONT, 8)
    pdf.drawCentredString(PAGE_WIDTH / 2, 0.85 * cm, "OFFICIAL: Sensitive (when completed)")
    pdf.drawRightString(PAGE_WIDTH - MARGIN, 0.85 * cm, f"Page {page_number}")


def draw_tfn_header(pdf, value):
    width = 6.2 * cm
    height = 0.9 * cm
    x = PAGE_WIDTH - MARGIN - width
    y = PAGE_HEIGHT - MARGIN + 0.15 * cm - height
    pdf.setFont(LABEL_SIZE and BODY_FONT, LABEL_SIZE)
    pdf.drawString(x, y + height + 1, "Tax File Number")
    pdf.rect(x + 2.4 * cm, y, width - 2.4 * cm, height, stroke=1, fill=0)
    pdf.setFont(BODY_FONT, BODY_SIZE)
    pdf.drawCentredString(x + 2.4 * cm + (width - 2.4 * cm) / 2, y + 0.28 * cm, measure(value))


def draw_section_header(pdf, title, y):
    pdf.setFont(BOLD_FONT, HEADER_SIZE)
    pdf.drawString(MARGIN, y, title)
    pdf.setLineWidth(0.7)
    pdf.line(MARGIN, y - 3, PAGE_WIDTH - MARGIN, y - 3)


def draw_field(pdf, x, y, width, height, label, value="", *, align="left", fontsize=BODY_SIZE, bold=False):
    pdf.setFont(BODY_FONT, LABEL_SIZE)
    pdf.setFillColor(colors.black)
    pdf.drawString(x, y + height + 2, label)
    pdf.rect(x, y, width, height, stroke=1, fill=0)
    if value == "":
        return
    pdf.setFont(BOLD_FONT if bold else BODY_FONT, fontsize)
    padding = 3
    text_y = y + (height - fontsize) / 2 + 2
    if align == "right":
        pdf.drawRightString(x + width - padding, text_y, measure(value))
    elif align == "center":
        pdf.drawCentredString(x + width / 2, text_y, measure(value))
    else:
        pdf.drawString(x + padding, text_y, measure(value))


def draw_currency_field(pdf, x, y, width, label, value="", *, large=False):
    pdf.setFont(BODY_FONT, LABEL_SIZE)
    pdf.drawString(x, y + BOX_HEIGHT + 2, label)
    pdf.setFont(BOLD_FONT if large else BODY_FONT, BODY_SIZE if not large else 10)
    pdf.drawString(x, y + 4, "$")
    pdf.rect(x + 8, y, width - 8, BOX_HEIGHT if not large else BOX_HEIGHT + 4, stroke=1, fill=0)
    if value != "":
        text_y = y + 4 if not large else y + 6
        pdf.drawRightString(x + width - 3, text_y, measure(value))


def draw_checkbox(pdf, x, y, label, checked=False):
    size = 10
    pdf.rect(x, y, size, size, stroke=1, fill=0)
    if checked:
        pdf.setFont(BOLD_FONT, 10)
        pdf.drawCentredString(x + size / 2, y + 1, "X")
    pdf.setFont(BODY_FONT, BODY_SIZE)
    pdf.drawString(x + size + 4, y + 1, label)


def draw_code_and_currency(pdf, x, y, width, label, value="", code_label="", code_value=""):
    amount_width = width - 2.2 * cm
    draw_currency_field(pdf, x, y, amount_width, label, value)
    draw_field(pdf, x + amount_width + 0.25 * cm, y, 1.95 * cm, BOX_HEIGHT, code_label, code_value, align="center")


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
    closing = max(50000.0, opening + total_contributions + allocated + inward - outward - lump_sum - income_stream)

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
        shown, numeric = maybe_numeric(minimum, maximum, whole=True, blank_probability=0.25 if code in {"B", "C", "I"} else 0.45)
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
        deduction_total += int(left_numeric)
        nondeductible_total += int(right_numeric)
    m1, m1_numeric = maybe_numeric(0, 12000, whole=True, blank_probability=0.45)
    deduction_pairs["M1"] = m1
    deduction_total += int(m1_numeric)

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
    levy = random.choice([259, 518])
    levy_adjustment_m = random.randint(0, 500)
    levy_adjustment_n = random.randint(0, 500)
    amount_due = tax_payable + interest_charge + levy + levy_adjustment_m - eligible_credit_total - tax_offset_refunds - payg_instalments - levy_adjustment_n

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
    }


def page_one(pdf, data):
    pdf.setFont(BOLD_FONT, TITLE_SIZE)
    pdf.drawRightString(PAGE_WIDTH - MARGIN, t(0.3 * cm), "Self-managed superannuation fund annual return 2024")

    draw_section_header(pdf, "Section A — Fund information", t(1.6 * cm))

    draw_field(pdf, MARGIN, t(2.8 * cm), 4.4 * cm, BOX_HEIGHT, "Tax file number (TFN)", data["tfn"])
    draw_field(pdf, MARGIN + 4.9 * cm, t(2.8 * cm), CONTENT_WIDTH - 4.9 * cm, BOX_HEIGHT, "Name of self-managed superannuation fund (SMSF)", data["fund_name"])
    draw_field(pdf, MARGIN, t(4.1 * cm), 4.4 * cm, BOX_HEIGHT, "Australian business number (ABN)", data["abn"])

    draw_field(pdf, MARGIN, t(5.5 * cm), CONTENT_WIDTH, BOX_HEIGHT, "Current postal address", data["address"]["street"])
    draw_field(pdf, MARGIN, t(6.8 * cm), 8.6 * cm, BOX_HEIGHT, "Suburb/town", data["address"]["suburb"])
    draw_field(pdf, MARGIN + 9 * cm, t(6.8 * cm), 2.5 * cm, BOX_HEIGHT, "State", data["address"]["state"], align="center")
    draw_field(pdf, MARGIN + 11.9 * cm, t(6.8 * cm), 3.0 * cm, BOX_HEIGHT, "Postcode", data["address"]["postcode"], align="center")

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN, t(8.5 * cm), "Annual return status")
    draw_checkbox(pdf, MARGIN, t(9.2 * cm), "A Amendment", data["annual_return_amendment"])
    draw_checkbox(pdf, MARGIN + 6.2 * cm, t(9.2 * cm), "B First return for new SMSF", data["annual_return_first"])


def page_two(pdf, data):
    draw_tfn_header(pdf, data["tfn"])
    draw_section_header(pdf, "Section 6 — SMSF auditor", t(0.7 * cm))

    auditor = data["auditor"]
    draw_field(pdf, MARGIN, t(1.9 * cm), 6 * cm, BOX_HEIGHT, "Family name", auditor["family_name"])
    draw_field(pdf, MARGIN + 6.4 * cm, t(1.9 * cm), 5.5 * cm, BOX_HEIGHT, "First given name", auditor["first_name"])
    draw_field(pdf, MARGIN + 12.2 * cm, t(1.9 * cm), 3.1 * cm, BOX_HEIGHT, "SMSF Auditor Number", auditor["san"], align="center")
    draw_field(pdf, MARGIN, t(3.2 * cm), 4.4 * cm, BOX_HEIGHT, "Phone", auditor["phone"])
    draw_field(pdf, MARGIN + 4.8 * cm, t(3.2 * cm), CONTENT_WIDTH - 4.8 * cm, BOX_HEIGHT, "Postal address", auditor["postal_address"])

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN, t(4.7 * cm), "Audit qualified")
    draw_checkbox(pdf, MARGIN, t(5.4 * cm), "B Part A qualified — Yes", auditor["part_a_qualified"])
    draw_checkbox(pdf, MARGIN + 6.1 * cm, t(5.4 * cm), "No", not auditor["part_a_qualified"])
    draw_checkbox(pdf, MARGIN, t(6.2 * cm), "C Part B qualified — Yes", auditor["part_b_qualified"])
    draw_checkbox(pdf, MARGIN + 6.1 * cm, t(6.2 * cm), "No", not auditor["part_b_qualified"])
    draw_checkbox(pdf, MARGIN, t(7.0 * cm), "D Issues rectified — Yes", auditor["part_b_rectified"])
    draw_checkbox(pdf, MARGIN + 6.1 * cm, t(7.0 * cm), "No", not auditor["part_b_rectified"])

    draw_section_header(pdf, "Section 7 — EFT details", t(8.5 * cm))
    eft = data["eft"]
    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN, t(9.4 * cm), "A Fund's financial institution")
    draw_field(pdf, MARGIN, t(10.3 * cm), 3.2 * cm, BOX_HEIGHT, "BSB", eft["fund_bsb"], align="center")
    draw_field(pdf, MARGIN + 3.6 * cm, t(10.3 * cm), 4.8 * cm, BOX_HEIGHT, "Account number", eft["fund_account"], align="center")
    draw_field(pdf, MARGIN + 8.8 * cm, t(10.3 * cm), 6.5 * cm, BOX_HEIGHT, "Account name", eft["fund_account_name"])
    draw_checkbox(pdf, MARGIN, t(11.2 * cm), "Tax refunds to this account", eft["fund_refund_check"])

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN, t(12.3 * cm), "B Financial institution for tax refunds")
    draw_field(pdf, MARGIN, t(13.2 * cm), 3.2 * cm, BOX_HEIGHT, "BSB", eft["refund_bsb"], align="center")
    draw_field(pdf, MARGIN + 3.6 * cm, t(13.2 * cm), 4.8 * cm, BOX_HEIGHT, "Account number", eft["refund_account"], align="center")
    draw_field(pdf, MARGIN + 8.8 * cm, t(13.2 * cm), 6.5 * cm, BOX_HEIGHT, "Account name", eft["refund_account_name"])
    draw_field(pdf, MARGIN, t(14.5 * cm), CONTENT_WIDTH, BOX_HEIGHT, "C Electronic service address alias (ESA)", eft["esa"])


def page_three(pdf, data):
    status = data["status"]
    draw_tfn_header(pdf, data["tfn"])
    draw_section_header(pdf, "Sections 8, 9 and 10 — Status and exempt current pension income", t(0.7 * cm))

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN, t(1.8 * cm), "Section 8 — Status of SMSF")
    draw_checkbox(pdf, MARGIN, t(2.6 * cm), "A Type — Regulated", status["type"] == "regulated")
    draw_checkbox(pdf, MARGIN + 6.2 * cm, t(2.6 * cm), "Other", status["type"] != "regulated")
    draw_checkbox(pdf, MARGIN, t(3.4 * cm), "B Benefit structure — Accumulation", status["benefit_structure"] == "accumulation")
    draw_checkbox(pdf, MARGIN + 8.2 * cm, t(3.4 * cm), "Mixture", status["benefit_structure"] != "accumulation")
    draw_checkbox(pdf, MARGIN, t(4.2 * cm), "C Super co-contribution received", status["co_contribution"])

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN, t(5.3 * cm), "Section 9 — Was the fund wound up")
    draw_checkbox(pdf, MARGIN, t(6.1 * cm), "No", not status["wound_up"])
    draw_checkbox(pdf, MARGIN + 3 * cm, t(6.1 * cm), "Yes", status["wound_up"])
    draw_field(pdf, MARGIN + 5.2 * cm, t(6.0 * cm), 3.3 * cm, BOX_HEIGHT, "Date", status["wound_up_date"], align="center")
    draw_checkbox(pdf, MARGIN + 9.1 * cm, t(6.1 * cm), "Tax obligations met — Yes", status["tax_obligations_met"])
    draw_checkbox(pdf, MARGIN + 14.0 * cm, t(6.1 * cm), "No", not status["tax_obligations_met"])

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN, t(7.5 * cm), "Section 10 — Exempt current pension income")
    draw_checkbox(pdf, MARGIN, t(8.3 * cm), "No", not status["ecpi_yes"])
    draw_checkbox(pdf, MARGIN + 3 * cm, t(8.3 * cm), "Yes", status["ecpi_yes"])
    draw_currency_field(pdf, MARGIN, t(9.4 * cm), 5.4 * cm, "A Amount", status["ecpi_amount"])
    draw_checkbox(pdf, MARGIN + 6.2 * cm, t(9.7 * cm), "B Segregated", status["ecpi_method"] == "segregated")
    draw_checkbox(pdf, MARGIN + 10.1 * cm, t(9.7 * cm), "C Unsegregated", status["ecpi_method"] == "unsegregated")
    draw_checkbox(pdf, MARGIN, t(10.8 * cm), "D Actuarial certificate obtained", status["actuarial_certificate"])


def draw_grid_page(pdf, data, title, rows, *, y_start=1.8 * cm, row_gap=0.98 * cm, columns=3):
    draw_tfn_header(pdf, data["tfn"])
    draw_section_header(pdf, title, t(0.7 * cm))
    col_width = CONTENT_WIDTH / columns
    field_width = col_width - 0.25 * cm
    for index, row in enumerate(rows):
        col = index % columns
        line = index // columns
        x = MARGIN + col * col_width
        y = t(y_start + line * row_gap)
        code = row["code"]
        label = row["label"]
        value = row["value"]
        if row.get("currency", True):
            draw_currency_field(pdf, x, y, field_width, f"{code} {label}", value)
        else:
            draw_field(pdf, x, y, field_width, BOX_HEIGHT, f"{code} {label}", value, align="right")


def page_four(pdf, data):
    rows = [
        {"code": "A", "label": "Net capital gain", "value": data["income"]["A"]["text"]},
        {"code": "B", "label": "Gross rent", "value": data["income"]["B"]["text"]},
        {"code": "C", "label": "Gross interest", "value": data["income"]["C"]["text"]},
        {"code": "X", "label": "Forestry managed investment scheme income", "value": data["income"]["X"]["text"]},
        {"code": "D1", "label": "Foreign source income", "value": data["income"]["D1"]["text"]},
        {"code": "D", "label": "Other net foreign income", "value": data["income"]["D"]["text"]},
        {"code": "E", "label": "Franking credits NZ", "value": data["income"]["E"]["text"]},
        {"code": "F", "label": "Transfers from foreign funds", "value": data["income"]["F"]["text"]},
        {"code": "H", "label": "Gross payments where ABN not quoted", "value": data["income"]["H"]["text"]},
        {"code": "R1", "label": "Contributions included in assessable income", "value": data["income"]["R1"]["text"]},
        {"code": "R2", "label": "Low tax contributions", "value": data["income"]["R2"]["text"]},
        {"code": "R3", "label": "Capital gains tax cap amounts", "value": data["income"]["R3"]["text"]},
        {"code": "R6", "label": "Other concessional contributions", "value": data["income"]["R6"]["text"]},
        {"code": "U1", "label": "Non-arm's length income component 1", "value": data["income"]["U1"]["text"]},
        {"code": "U2", "label": "Non-arm's length income component 2", "value": data["income"]["U2"]["text"]},
        {"code": "U3", "label": "Non-arm's length income component 3", "value": data["income"]["U3"]["text"]},
        {"code": "I", "label": "Trust distributions", "value": data["income"]["I"]["text"]},
        {"code": "J", "label": "Partnership distributions", "value": data["income"]["J"]["text"]},
        {"code": "K", "label": "Other Australian income", "value": data["income"]["K"]["text"]},
        {"code": "L", "label": "Listed trust distributions", "value": data["income"]["L"]["text"]},
        {"code": "M", "label": "Unlisted trust distributions", "value": data["income"]["M"]["text"]},
        {"code": "S", "label": "Other income", "value": data["income"]["S"]["text"]},
        {"code": "T", "label": "Assessable income changed tax status", "value": data["income"]["T"]["text"]},
        {"code": "W", "label": "Gross income", "value": data["gross_income"]},
        {"code": "Y", "label": "Exempt current pension income", "value": data["ecpi_total"]},
        {"code": "V", "label": "Total assessable income", "value": data["assessable_income"]},
    ]
    draw_grid_page(pdf, data, "Section B — Income (Section 11)", rows)


def page_five(pdf, data):
    draw_tfn_header(pdf, data["tfn"])
    draw_section_header(pdf, "Section C — Deductions (Section 12)", t(0.7 * cm))
    pdf.setFont(BOLD_FONT, BODY_SIZE)
    left_x = MARGIN
    right_x = MARGIN + CONTENT_WIDTH / 2 + 0.2 * cm
    column_width = CONTENT_WIDTH / 2 - 0.4 * cm
    pdf.drawString(left_x, t(1.6 * cm), "DEDUCTIONS")
    pdf.drawString(right_x, t(1.6 * cm), "NON-DEDUCTIBLE EXPENSES")

    row_specs = [
        ("A1", "Management and administration"),
        ("B1", "Investment expenses"),
        ("D1", "Audit fees"),
        ("E1", "Actuarial fees"),
        ("F1", "ASIC fees"),
        ("H1", "Trustee liability insurance"),
        ("I1", "Supervisory levy"),
        ("J1", "Management and custodial"),
        ("U1", "Non-arm's length expense"),
        ("L1", "Interest expenses"),
        ("M1", "Other allowable deductions"),
    ]
    y = t(2.5 * cm)
    for code, label in row_specs:
        draw_currency_field(pdf, left_x, y, column_width, f"{code} {label}", data["deductions"].get(code, ""))
        partner_code = code.replace("1", "2") if code != "M1" else ""
        if partner_code:
            draw_currency_field(pdf, right_x, y, column_width, f"{partner_code} {label}", data["deductions"].get(partner_code, ""))
        y -= FIELD_GAP

    y -= 6
    draw_currency_field(pdf, left_x, y, column_width, "N Total deductions", data["deduction_total"])
    draw_currency_field(pdf, right_x, y, column_width, "Y Total non-deductible", data["nondeductible_total"])
    y -= FIELD_GAP
    draw_currency_field(pdf, left_x, y, column_width, "O Taxable income or loss", data["taxable_income"])
    draw_currency_field(pdf, right_x, y, column_width, "Z Total SMSF expenses", data["expense_total"])


def page_six(pdf, data):
    rows = [
        {"code": "A", "label": "Taxable income", "value": data["tax"]["A"]},
        {"code": "T1", "label": "Tax on taxable income", "value": data["tax"]["T1"]},
        {"code": "J", "label": "Tax on no-TFN contributions", "value": data["tax"]["J"]},
        {"code": "B", "label": "Gross tax", "value": data["tax"]["B"]},
        {"code": "C1", "label": "Tax offset 1", "value": data["tax"]["C1"]},
        {"code": "C2", "label": "Tax offset 2", "value": data["tax"]["C2"]},
        {"code": "C", "label": "Total tax offsets", "value": data["tax"]["C"]},
        {"code": "T2", "label": "Subtotal 1", "value": data["tax"]["T2"]},
        {"code": "D1", "label": "Carry forward tax offset 1", "value": data["tax"]["D1"]},
        {"code": "D2", "label": "Carry forward tax offset 2", "value": data["tax"]["D2"]},
        {"code": "D3", "label": "Carry forward tax offset 3", "value": data["tax"]["D3"]},
        {"code": "D4", "label": "Carry forward tax offset 4", "value": data["tax"]["D4"]},
        {"code": "D", "label": "Total carry forward tax offsets", "value": data["tax"]["D"]},
        {"code": "T3", "label": "Subtotal 2", "value": data["tax"]["T3"]},
        {"code": "E1", "label": "Refundable tax offset 1", "value": data["tax"]["E1"]},
        {"code": "E2", "label": "Refundable tax offset 2", "value": data["tax"]["E2"]},
        {"code": "E3", "label": "Refundable tax offset 3", "value": data["tax"]["E3"]},
        {"code": "E4", "label": "Refundable tax offset 4", "value": data["tax"]["E4"]},
        {"code": "E", "label": "Total refundable tax offsets", "value": data["tax"]["E"]},
        {"code": "T5", "label": "Tax payable", "value": data["tax"]["T5"]},
        {"code": "G", "label": "Section 102AAM interest charge", "value": data["tax"]["G"]},
    ]
    draw_grid_page(pdf, data, "Section D — Income tax calculation (Section 13)", rows, columns=3, row_gap=1.0 * cm)


def page_seven(pdf, data):
    draw_tfn_header(pdf, data["tfn"])
    draw_section_header(pdf, "Section D continued and Section E — Losses", t(0.7 * cm))
    continued = data["continued_tax"]
    left_rows = [
        ("H2", "Eligible credits 2"),
        ("H3", "Eligible credits 3"),
        ("H5", "Eligible credits 5"),
        ("H6", "Eligible credits 6"),
        ("H8", "Eligible credits 8"),
        ("H", "Total eligible credits"),
        ("I", "Tax offset refunds"),
        ("K", "PAYG instalments"),
        ("L", "Supervisory levy"),
        ("M", "Supervisory levy adjustment"),
        ("N", "Supervisory levy credit"),
        ("S", "Amount due or refundable"),
    ]
    y = t(1.8 * cm)
    for code, label in left_rows:
        draw_currency_field(pdf, MARGIN, y, 7.3 * cm, f"{code} {label}", continued[code])
        y -= FIELD_GAP

    draw_checkbox(pdf, MARGIN + 8.1 * cm, t(2.3 * cm), "Refund amount", continued["refund"])
    draw_checkbox(pdf, MARGIN + 8.1 * cm, t(3.1 * cm), "Amount due", not continued["refund"])

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN + 8.1 * cm, t(4.5 * cm), "Section 14 — Losses")
    draw_currency_field(pdf, MARGIN + 8.1 * cm, t(5.5 * cm), 7.2 * cm, "U Tax losses carried forward", data["losses"]["U"])
    draw_currency_field(pdf, MARGIN + 8.1 * cm, t(6.8 * cm), 7.2 * cm, "V Net capital losses carried forward", data["losses"]["V"])


def page_member(pdf, data, member_number):
    draw_tfn_header(pdf, data["tfn"])
    draw_section_header(pdf, f"Section F — MEMBER {member_number}", t(0.7 * cm))
    member = data["members"][member_number - 1] if member_number <= len(data["members"]) else None

    titles = TITLES
    x = MARGIN
    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(x, t(1.7 * cm), "Title")
    for i, title in enumerate(titles):
        checked = bool(member and member["title"] == title)
        draw_checkbox(pdf, x + i * 2.25 * cm, t(2.5 * cm), title, checked)

    draw_field(pdf, MARGIN, t(3.6 * cm), 5.2 * cm, BOX_HEIGHT, "Family name", member["family_name"] if member else "")
    draw_field(pdf, MARGIN + 5.6 * cm, t(3.6 * cm), 4.7 * cm, BOX_HEIGHT, "First given name", member["first_name"] if member else "")
    draw_field(pdf, MARGIN + 10.7 * cm, t(3.6 * cm), 4.6 * cm, BOX_HEIGHT, "Other given names", member["other_names"] if member else "")
    draw_field(pdf, MARGIN, t(4.9 * cm), 4.4 * cm, BOX_HEIGHT, "Member's TFN", member["tfn"] if member else "")
    draw_field(pdf, MARGIN + 4.8 * cm, t(4.9 * cm), 4.0 * cm, BOX_HEIGHT, "Date of birth", member["dob"] if member else "")
    draw_currency_field(pdf, MARGIN + 9.2 * cm, t(4.9 * cm), 6.1 * cm, "Opening account balance", member["opening_balance"] if member else "")

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN, t(6.1 * cm), "Contributions")
    contrib_y = t(7.0 * cm)
    contribution_rows = [
        ("A", "Employer", member["contributions"]["A"] if member else "", member["employer_abn"] if member else "", "A1 Employer ABN"),
        ("B", "Personal", member["contributions"]["B"] if member else "", "", ""),
        ("C", "CGT small business retirement", member["contributions"]["C"] if member else "", "", ""),
        ("D", "CGT small business 15-year", member["contributions"]["D"] if member else "", "", ""),
        ("E", "Personal injury", member["contributions"]["E"] if member else "", "", ""),
        ("F", "Spouse or child", member["contributions"]["F"] if member else "", "", ""),
        ("G", "Other third party", member["contributions"]["G"] if member else "", "", ""),
        ("H", "Primary residence disposal proceeds", member["contributions"]["H"] if member else "", member["residence_date"] if member else "", "H1 Date"),
        ("I", "Assessable foreign super", member["contributions"]["I"] if member else "", "", ""),
        ("J", "Non-assessable foreign super", member["contributions"]["J"] if member else "", "", ""),
        ("K", "Transfer from reserve assessable", member["contributions"]["K"] if member else "", "", ""),
        ("L", "Transfer from reserve non-assessable", member["contributions"]["L"] if member else "", "", ""),
        ("T", "Contributions from non-complying funds", member["contributions"]["T"] if member else "", "", ""),
        ("M", "Any other contributions", member["contributions"]["M"] if member else "", "", ""),
    ]
    left_x = MARGIN
    right_x = MARGIN + 8.0 * cm
    for index, (code, label, value, side_value, side_label) in enumerate(contribution_rows):
        current_x = left_x if index % 2 == 0 else right_x
        current_y = contrib_y - (index // 2) * FIELD_GAP
        draw_currency_field(pdf, current_x, current_y, 7.4 * cm, f"{code} {label}", value)
        if side_label:
            draw_field(pdf, current_x + 5.45 * cm, current_y, 1.95 * cm, BOX_HEIGHT, side_label, side_value, align="center", fontsize=7)

    totals_y = contrib_y - 7 * FIELD_GAP - 4
    draw_currency_field(pdf, MARGIN, totals_y, 7.4 * cm, "N Total contributions", member["total_contributions"] if member else "")

    pdf.setFont(BOLD_FONT, BODY_SIZE)
    pdf.drawString(MARGIN + 8.0 * cm, t(15.8 * cm), "Other transactions")
    other_y = t(16.6 * cm)
    draw_currency_field(pdf, MARGIN + 8.0 * cm, other_y, 7.3 * cm, "O Allocated earnings/losses", member["allocated_earnings"] if member else "")
    draw_checkbox(pdf, MARGIN + 13.0 * cm, other_y + 3, "Loss", bool(member and member["allocated_loss"]))
    other_y -= FIELD_GAP
    draw_currency_field(pdf, MARGIN + 8.0 * cm, other_y, 7.3 * cm, "P Inward rollovers", member["inward_rollovers"] if member else "")
    other_y -= FIELD_GAP
    draw_currency_field(pdf, MARGIN + 8.0 * cm, other_y, 7.3 * cm, "Q Outward rollovers", member["outward_rollovers"] if member else "")
    other_y -= FIELD_GAP
    draw_code_and_currency(pdf, MARGIN + 8.0 * cm, other_y, 7.3 * cm, "R1 Lump sum payments", member["lump_sum"] if member else "", "Code", member["lump_sum_code"] if member else "")
    other_y -= FIELD_GAP
    draw_code_and_currency(pdf, MARGIN + 8.0 * cm, other_y, 7.3 * cm, "R2 Income stream payments", member["income_stream"] if member else "", "Code", member["income_stream_code"] if member else "")

    balances_y = t(19.7 * cm)
    draw_currency_field(pdf, MARGIN, balances_y, 4.7 * cm, "S1 Accumulation phase account balance", member["accumulation_balance"] if member else "")
    draw_currency_field(pdf, MARGIN + 5.1 * cm, balances_y, 4.9 * cm, "S2 Retirement phase non-CDBIS", member["retirement_non_cdbis"] if member else "")
    draw_currency_field(pdf, MARGIN + 10.4 * cm, balances_y, 3.4 * cm, "S3 Retirement phase CDBIS", member["retirement_cdbis"] if member else "")
    draw_field(pdf, MARGIN + 14.2 * cm, balances_y, 1.1 * cm, BOX_HEIGHT, "TRIS", member["tris_count"] if member else "", align="center")

    draw_currency_field(pdf, MARGIN, t(21.2 * cm), CONTENT_WIDTH, "CLOSING ACCOUNT BALANCE S$", member["closing_balance"] if member else "", large=True)
    draw_currency_field(pdf, MARGIN, t(22.6 * cm), 5.0 * cm, "X1 Accumulation phase value", member["x1"] if member else "")
    draw_currency_field(pdf, MARGIN + 5.4 * cm, t(22.6 * cm), 5.0 * cm, "X2 Retirement phase value", member["x2"] if member else "")
    draw_currency_field(pdf, MARGIN + 10.8 * cm, t(22.6 * cm), 4.5 * cm, "Y Outstanding LRBA amount", member["lrba"] if member else "")


def build_pdf(output_path, num_members):
    data = build_form_data(num_members)
    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    pdf.setTitle("Self-managed superannuation fund annual return 2024")
    pdf.setStrokeColor(colors.black)
    pdf.setFillColor(colors.black)
    pdf.setLineWidth(0.5)

    page_one(pdf, data)
    draw_footer(pdf, 1)
    pdf.showPage()

    page_two(pdf, data)
    draw_footer(pdf, 2)
    pdf.showPage()

    page_three(pdf, data)
    draw_footer(pdf, 3)
    pdf.showPage()

    page_four(pdf, data)
    draw_footer(pdf, 4)
    pdf.showPage()

    page_five(pdf, data)
    draw_footer(pdf, 5)
    pdf.showPage()

    page_six(pdf, data)
    draw_footer(pdf, 6)
    pdf.showPage()

    page_seven(pdf, data)
    draw_footer(pdf, 7)
    pdf.showPage()

    for member_number in range(1, 7):
        page_member(pdf, data, member_number)
        draw_footer(pdf, 7 + member_number)
        if member_number != 6:
            pdf.showPage()

    pdf.save()
    return data["tfn"]


def main():
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    generated = []
    for members in range(1, 7):
        for index in range(1, 3):
            output_path = output_dir / f"smsf_return_{members}members_{index}.pdf"
            tfn_value = build_pdf(output_path, members)
            relative_path = os.path.relpath(output_path, Path(__file__).resolve().parent)
            print(f"Generated: {relative_path}  ({members} members, TFN: {tfn_value})")
            generated.append(output_path)

    print("\nAll 12 PDFs generated in the 'output' folder.")
    return generated


if __name__ == "__main__":
    main()
