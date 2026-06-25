import random
import os
import pymupdf
from datetime import date, timedelta

SOURCE_PDF = os.path.join(os.path.dirname(__file__), 'SMSFAR 2024-smart form.pdf')

# ── data pools ──────────────────────────────────────────────────────────────
TITLES      = ['Mr', 'Mrs', 'Ms', 'Dr', 'Miss']
FIRST_NAMES = ['James','Sarah','Michael','Emma','David','Lisa','Robert','Karen',
               'William','Jennifer','John','Patricia','Thomas','Susan','Mark',
               'Jessica','Andrew','Helen','Peter','Catherine','Paul','Margaret',
               'Steven','Elizabeth','Brian','Christine','Kevin','Rebecca']
LAST_NAMES  = ['Smith','Johnson','Williams','Brown','Jones','Miller','Davis',
               'Wilson','Taylor','Anderson','Thomas','Jackson','White','Harris',
               'Martin','Thompson','Garcia','Martinez','Robinson','Clark',
               'Rodriguez','Lewis','Lee','Walker','Hall','Allen','Young','King']
PRACTICES   = ['ABC Accounting', 'Smith & Associates', 'Premier Tax Solutions',
               'Wealth Advisory Group', 'Total SMSF Services', 'Henderson Partners',
               'Blue Sky Accounting', 'Pinnacle Tax & Super', 'Accord Financial']
BANKS       = ['Commonwealth Bank', 'ANZ Bank', 'Westpac', 'NAB', 'Macquarie Bank',
               'Bendigo Bank', 'Suncorp Bank', 'Bank of Queensland']
ESA_ALIASES = ['SMSFAUSTRALIA', 'BGLSMSF', 'CLASSSMSF', 'SUPERFUND', 'HEFFRON',
               'MCLOWD', 'SIMPLE FUND', 'SELFMANAGEDSUPER']

# ── helpers ─────────────────────────────────────────────────────────────────
def rand_tfn():
    """Generate a valid-format 9-digit TFN: XXX XXX XXX"""
    digits = [random.randint(0, 9) for _ in range(9)]
    return f"{digits[0]}{digits[1]}{digits[2]} {digits[3]}{digits[4]}{digits[5]} {digits[6]}{digits[7]}{digits[8]}"

def rand_abn():
    """Generate a valid-format 11-digit ABN: XX XXX XXX XXX"""
    digits = [random.randint(0, 9) for _ in range(11)]
    digits[0] = random.randint(1, 9)
    return f"{digits[0]}{digits[1]} {digits[2]}{digits[3]}{digits[4]} {digits[5]}{digits[6]}{digits[7]} {digits[8]}{digits[9]}{digits[10]}"

def rand_bsb():
    """Generate a 6-digit BSB number with no hyphen."""
    return f"{random.randint(100,999)}{random.randint(100,999)}"

def rand_account():
    return str(random.randint(10000000, 999999999))

def whole_amount(min_val=0, max_val=500000):
    """Whole dollar amounts – no cents, no commas."""
    val = random.randint(min_val, max_val)
    return f"{val:.0f}"

def cents_amount(min_val=0, max_val=500000):
    """Dollar + cents amounts for member fields – with commas."""
    val = random.uniform(min_val, max_val)
    return f"{val:,.2f}"

def rand_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)

def rand_dob():
    start = date(1945, 1, 1)
    end   = date(1985, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def rand_phone():
    return f"0{random.randint(2,4)}{random.randint(10000000,99999999)}"

def rand_email(first, last):
    domains = ['gmail.com','outlook.com','bigpond.com','hotmail.com','icloud.com']
    return f"{first.lower()}.{last.lower()}@{random.choice(domains)}"

def rand_fund_name(last1, last2=None):
    suffixes = ['Superannuation Fund', 'Super Fund', 'Retirement Fund', 'SMSF']
    if last2 and random.random() > 0.5:
        return f"{last1} & {last2} {random.choice(suffixes)}"
    return f"{last1} Family {random.choice(suffixes)}"

# ── PDF field helpers ────────────────────────────────────────────────────────
def set_text(page, field_name, value):
    """Set a text field value on the given page."""
    for widget in page.widgets():
        if widget.field_name == field_name:
            widget.field_value = str(value)
            widget.update()
            return

def set_amount(page, field_name, value):
    """Set a numeric/dollar field value, right-aligned."""
    for widget in page.widgets():
        if widget.field_name == field_name:
            widget.field_value = str(value)
            widget.text_align = 2  # 0=left, 1=center, 2=right
            widget.update()
            return

def set_radio(page, field_name, option_index):
    """Select a radio button by option index (0 = first widget, 1 = second widget)."""
    matches = [w for w in page.widgets() if w.field_name == field_name]
    for i, widget in enumerate(matches):
        widget.field_value = (i == option_index)
        widget.update()

# ── member field filler ──────────────────────────────────────────────────────
def fill_member(page, n):
    """Fill fields for member N (1-based) on the given page."""
    ncdbis_field = 'mem1-ncsbis' if n == 1 else f'mem{n}-ncdbis'

    set_amount(page, f'mem{n}-ls',     cents_amount(0, 100000))
    set_amount(page, f'mem{n}-is',     cents_amount(0, 80000))
    set_amount(page, f'mem{n}-acc',    cents_amount(0, 800000))
    set_amount(page, ncdbis_field,     cents_amount(0, 600000))
    set_amount(page, f'mem{n}-cdbis',  cents_amount(0, 200000))
    set_amount(page, f'mem{n}-tris',   str(random.randint(0, 2)))
    set_amount(page, f'mem{n}-bal',    cents_amount(100000, 1500000))
    set_amount(page, f'mem{n}-accbal', cents_amount(0, 800000))
    set_amount(page, f'mem{n}-retbal', cents_amount(0, 600000))
    set_amount(page, f'mem{n}-lrba',   cents_amount(0, 300000))

# ── main form generator ──────────────────────────────────────────────────────
def generate_form(output_path, num_members=None):
    if num_members is None:
        num_members = random.randint(1, 6)

    first1, last1 = rand_name()
    first2, last2 = rand_name()
    fund_name = rand_fund_name(last1, last2)

    doc = pymupdf.open(SOURCE_PDF)

    # ── Page 1: Fund identification ──────────────────────────────────────────
    p1 = doc[0]
    set_text(p1, 'tfn',       rand_tfn())
    set_text(p1, 'smsf-name', fund_name)
    set_text(p1, 'abn',       rand_abn())

    # ── Page 2: Electronic funds / audit ────────────────────────────────────
    p2 = doc[1]
    set_text(p2, 'ss-bsb',      rand_bsb())
    set_text(p2, 'ss-acc',      rand_account())
    set_text(p2, 'ss-acc-name', fund_name)
    set_text(p2, 'ref-bsb',     rand_bsb())
    set_text(p2, 'ref-acc',     rand_account())
    set_text(p2, 'ref-acc-name', fund_name)
    set_text(p2, 'esa',         random.choice(ESA_ALIASES))

    # Audit: 0=No, 1=Yes  (first radio option is No)
    audit_a_qual = random.randint(0, 1)
    audit_b_qual = random.randint(0, 1)
    set_radio(p2, 'aud-parta-qual',    audit_a_qual)
    set_radio(p2, 'aud-partb-qual',    audit_b_qual)
    # Part B rectified only relevant when Part B is qualified (index 1 = Yes)
    set_radio(p2, 'aud-partb-qual-yes', random.randint(0, 1))

    # ── Page 3: ECPI ────────────────────────────────────────────────────────
    p3 = doc[2]
    ecpi_choice = random.choice(['no', 'segregated', 'unsegregated'])
    if ecpi_choice != 'no':
        set_amount(p3, 'ECPI', whole_amount(5000, 80000))

    # ecpi-yes/no: 0=No, 1=Yes
    set_radio(p3, 'ecpi-yes/no',       0 if ecpi_choice == 'no' else 1)
    # ecpi-other-asses: 0=No, 1=Yes
    set_radio(p3, 'ecpi-other-asses',  random.randint(0, 1))
    # pension-method: 0=Segregated, 1=Unsegregated
    if ecpi_choice != 'no':
        set_radio(p3, 'pension-method', 0 if ecpi_choice == 'segregated' else 1)
    # act-cert: 0=No, 1=Yes
    set_radio(p3, 'act-cert', 1 if ecpi_choice == 'unsegregated' and random.random() > 0.4 else 0)

    # ── Page 5: Management expenses ─────────────────────────────────────────
    p5 = doc[4]
    set_amount(p5, 'j1-admin-exp', whole_amount(1000, 20000))
    set_amount(p5, 'j2-admin-exp', whole_amount(0, 5000))

    # ── Page 7: Losses carried forward ──────────────────────────────────────
    p7 = doc[6]
    set_amount(p7, 'cfl-tax', whole_amount(0, 50000))
    set_amount(p7, 'cfl-cg',  whole_amount(0, 50000))

    # ── Pages 8–13: Members (pages index 7–12) ──────────────────────────────
    for n in range(1, 7):
        page = doc[7 + n - 1]   # page index 7 = page 8 (member 1)
        if n <= num_members:
            fill_member(page, n)

    # ── Page 20: Assets ─────────────────────────────────────────────────────
    p20 = doc[19]
    def wa(mn=0, mx=500000): return whole_amount(mn, mx)

    set_amount(p20, '15a-a',   wa(0, 300000))
    set_amount(p20, '15a-b',   wa(0, 100000))
    set_amount(p20, '15a-c',   wa(0, 200000))
    set_amount(p20, '15a-d',   wa(0, 300000))
    set_amount(p20, '15b-e',   wa(0, 500000))
    set_amount(p20, '15b-f',   wa(0, 800000))
    set_amount(p20, '15b-g',   wa(0, 800000))
    set_amount(p20, '15b-h',   wa(0, 500000))
    set_amount(p20, '15b-i',   wa(0, 50000))
    set_amount(p20, '15b-j1',  wa(0, 500000))
    set_amount(p20, '15b-j2',  wa(0, 300000))
    set_amount(p20, '15b-js',  wa(0, 200000))
    set_amount(p20, '15b-j4',  wa(0, 800000))
    set_amount(p20, '15b-j5',  wa(0, 200000))
    set_amount(p20, '15b-j6',  wa(0, 100000))
    set_amount(p20, '15b-j7',  wa(0, 100000))
    set_amount(p20, '15b-j',   wa(0, 800000))
    set_amount(p20, '15b-k',   wa(0, 100000))
    set_amount(p20, '15b-l',   wa(0, 300000))
    set_amount(p20, '15b-m',   wa(0, 500000))
    set_amount(p20, '15b-0',   wa(0, 800000))
    set_amount(p20, '15c-n',   wa(0, 50000))
    set_amount(p20, 'Text34',  wa(0, 100000))
    set_amount(p20, 'Text35',  wa(0, 100000))
    set_amount(p20, 'Text36',  wa(0, 100000))
    set_amount(p20, 'Text37',  wa(0, 100000))
    set_amount(p20, 'Text38',  wa(0, 100000))
    set_amount(p20, 'Text39',  wa(0, 100000))
    set_amount(p20, '15e',     wa(0, 50000))

    # ── Page 21: Liabilities ─────────────────────────────────────────────────
    p21 = doc[20]
    set_amount(p21, '16-v1', wa(0, 100000))
    set_amount(p21, '16-v2', wa(0, 100000))
    set_amount(p21, '16-v3', wa(0, 100000))
    set_amount(p21, '16v',   wa(0, 200000))
    set_amount(p21, '16w',   wa(100000, 2000000))
    set_amount(p21, '16x',   wa(0, 50000))
    set_amount(p21, '16y',   wa(0, 50000))
    set_amount(p21, '16z',   wa(0, 50000))

    # ── Page 22: Declarations ────────────────────────────────────────────────
    p22 = doc[21]
    trustee_first, trustee_last = rand_name()
    agent_first, agent_last     = rand_name()
    has_corp_trustee = random.random() > 0.5

    set_text(p22, 'trustee-family-name', trustee_last)
    set_text(p22, 'trustee-first-name',  trustee_first)
    set_text(p22, 'trustee-other-name',  random.choice(FIRST_NAMES))
    set_text(p22, 'trustee-phone',       rand_phone())
    set_text(p22, 'trustee-email',       rand_email(trustee_first, trustee_last))
    if has_corp_trustee:
        set_text(p22, 'trustee-corporate', f"{trustee_last} Pty Ltd")
        set_text(p22, 'trustee-corp-abn',  rand_abn())

    set_text(p22, 'tax-agent-family-name', agent_last)
    set_text(p22, 'tax-agent-first-name',  agent_first)
    set_text(p22, 'tax-agent-other-name',  random.choice(FIRST_NAMES))
    set_text(p22, 'Tax agents practice',   random.choice(PRACTICES))
    set_text(p22, 'tan-phone',             rand_phone())
    set_amount(p22, 'tan-ref',             str(random.randint(10000000, 99999999)))
    set_amount(p22, 'tan',                 str(random.randint(10000000, 99999999)))

    doc.save(output_path)
    doc.close()
    print(f"Generated: {output_path}  ({num_members} members)")

# ── run ──────────────────────────────────────────────────────────────────────
os.makedirs('output', exist_ok=True)

for members in range(1, 7):
    for i in range(1, 3):
        generate_form(f'output/smsf_return_{members}members_{i}.pdf', num_members=members)

print("\nAll PDFs generated in the 'output' folder.")