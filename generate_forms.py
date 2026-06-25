import random
import pdfkit
import os
from datetime import date, timedelta

# ── wkhtmltopdf config ──────────────────────────────────────────────────────
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
PDF_OPTIONS = {
    'quiet': '',
    'page-size': 'A4',
    'margin-top': '10mm',
    'margin-bottom': '10mm',
    'margin-left': '12mm',
    'margin-right': '12mm',
    'encoding': 'UTF-8',
}

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
    return f"{random.randint(100,999)} {random.randint(100,999)} {random.randint(100,999)}"

def rand_abn():
    return f"{random.randint(10,99)} {random.randint(100,999)} {random.randint(100,999)} {random.randint(100,999)}"

def rand_bsb():
    return f"{random.randint(100,999)}-{random.randint(100,999)}"

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

def x(checked):
    """Return X if checked, empty otherwise."""
    return 'X' if checked else ''

def checkbox_title(selected_title, title_option):
    return x(selected_title == title_option)

def rand_code():
    return random.choice(['101', '102', '103', '104', '201', '202', '301', 'M', 'N', 'P', 'R'])

# ── member HTML ─────────────────────────────────────────────────────────────
def build_member_html(member_num):
    first, last = rand_name()
    title = random.choice(TITLES)
    tris  = random.randint(0, 2)
    r1_code = rand_code()
    r2_code = rand_code()

    s1 = cents_amount(0, 800000)
    s2 = cents_amount(0, 600000)
    s3 = cents_amount(0, 200000)
    # Closing balance = sum of S1+S2+S3 (approximate, for realism)
    closing = cents_amount(100000, 1500000)
    x1  = cents_amount(0, 800000)
    x2  = cents_amount(0, 600000)
    y   = cents_amount(0, 300000)
    r1_amt = cents_amount(0, 100000)
    r2_amt = cents_amount(0, 80000)

    return f"""
    <div class="member-block">
      <div class="member-heading">MEMBER {member_num}</div>

      <div class="title-row">
        Title: &nbsp;
        Mr <span class="checkbox">{checkbox_title(title,'Mr')}</span> &nbsp;
        Mrs <span class="checkbox">{checkbox_title(title,'Mrs')}</span> &nbsp;
        Miss <span class="checkbox">{checkbox_title(title,'Miss')}</span> &nbsp;
        Ms <span class="checkbox">{checkbox_title(title,'Ms')}</span> &nbsp;
        Other <span class="input-box input-box-narrow input-box-left"></span>
      </div>

      <div class="field-label-above">Family name</div>
      <div class="input-box input-box-left" style="width:100%; margin-bottom:5px;">{last}</div>

      <div class="two-col">
        <div class="col">
          <div class="field-label-above">First given name</div>
          <div class="input-box input-box-left input-box-full">{first}</div>
        </div>
        <div class="col">
          <div class="field-label-above">Other given names</div>
          <div class="input-box input-box-left input-box-full">{random.choice(FIRST_NAMES)}</div>
        </div>
      </div>

      <div class="two-col" style="margin-top:5px;">
        <div class="col">
          <div class="field-label-above"><strong>Member's TFN</strong><br><span style="font-size:7.5pt;">See the Privacy note in the Declaration.</span></div>
          <div class="input-box input-box-left input-box-full">Provided</div>
        </div>
        <div class="col">
          <div class="field-label-above">Date of birth &nbsp; <span style="font-size:7.5pt;">Day &nbsp;&nbsp; Month &nbsp;&nbsp; Year</span></div>
          <div class="input-box input-box-left input-box-full">Provided</div>
        </div>
      </div>

      <hr style="margin:8px 0;">

      <div class="two-col">
        <div class="col">
          <div class="inner-box">
            <div class="field-label-above">Accumulation phase account balance</div>
            <div class="dollar-field" style="margin-bottom:6px;"><span class="label-code">S1</span> <span class="dollar-sign">$</span> <div class="input-box" style="width:160px;">{s1}</div></div>

            <div class="field-label-above">Retirement phase account balance – Non CDBIS</div>
            <div class="dollar-field" style="margin-bottom:6px;"><span class="label-code">S2</span> <span class="dollar-sign">$</span> <div class="input-box" style="width:160px;">{s2}</div></div>

            <div class="field-label-above">Retirement phase account balance – CDBIS</div>
            <div class="dollar-field"><span class="label-code">S3</span> <span class="dollar-sign">$</span> <div class="input-box" style="width:160px;">{s3}</div></div>
          </div>
          <div style="margin-top:5px; display:flex; align-items:center; gap:8px;">
            <div class="input-box input-box-xnarrow" style="text-align:center;">{tris}</div>
            <span style="font-size:8.5pt;">TRIS Count</span>
            <span style="font-weight:bold; margin-left:10px;">CLOSING ACCOUNT BALANCE</span>
            <span class="label-code">S</span> <span class="dollar-sign">$</span>
            <div class="input-box" style="width:130px;">{closing}</div>
          </div>
          <div class="hint" style="margin-left:120px;">(S1 <em>plus</em> S2 <em>plus</em> S3)</div>
        </div>

        <div class="col">
          <div class="field-label-above">Lump sum payments &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Code</div>
          <div class="dollar-field" style="margin-bottom:6px;">
            <span class="label-code">R1</span> <span class="dollar-sign">$</span>
            <div class="input-box" style="width:130px;">{r1_amt}</div>
            <div class="input-box input-box-xnarrow" style="text-align:center;">{r1_code}</div>
          </div>

          <div class="field-label-above">Income stream payments &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Code</div>
          <div class="dollar-field" style="margin-bottom:6px;">
            <span class="label-code">R2</span> <span class="dollar-sign">$</span>
            <div class="input-box" style="width:130px;">{r2_amt}</div>
            <div class="input-box input-box-xnarrow" style="text-align:center;">{r2_code}</div>
          </div>
        </div>
      </div>

      <div style="margin-top:6px;">
        <div class="field-label-above">Accumulation phase value &nbsp;<span class="label-code">X1</span> $</div>
        <div class="input-box" style="width:220px; margin-bottom:4px;">{x1}</div>
        <div class="field-label-above">Retirement phase value &nbsp;<span class="label-code">X2</span> $</div>
        <div class="input-box" style="width:220px; margin-bottom:4px;">{x2}</div>
        <div class="field-label-above">Outstanding limited recourse borrowing arrangement amount &nbsp;<span class="label-code">Y</span> $</div>
        <div class="input-box" style="width:220px;">{y}</div>
      </div>
    </div>
    """

def build_members_html(num_members):
    return ''.join(build_member_html(i) for i in range(1, num_members + 1))

# ── main form generator ─────────────────────────────────────────────────────
def generate_form(output_path, num_members=None):
    if num_members is None:
        num_members = random.randint(1, 6)

    first1, last1 = rand_name()
    first2, last2 = rand_name()
    fund_name = rand_fund_name(last1, last2)
    tfn = rand_tfn()

    # ECPI
    ecpi_choice = random.choice(['no', 'segregated', 'unsegregated'])
    ecpi_no     = x(ecpi_choice == 'no')
    ecpi_yes    = x(ecpi_choice != 'no')
    ecpi_seg    = x(ecpi_choice == 'segregated')
    ecpi_unseg  = x(ecpi_choice == 'unsegregated')
    actuarial   = x(ecpi_choice == 'unsegregated' and random.random() > 0.4)
    ecpi_amount = whole_amount(5000, 80000) if ecpi_choice != 'no' else ''
    ecpi_e_yes  = x(random.random() > 0.6)
    ecpi_e_no   = x(not ecpi_e_yes)

    # Audit
    audit_a  = random.choice(['yes', 'no'])
    audit_b  = random.choice(['yes', 'no'])
    audit_r  = random.choice(['yes', 'no']) if audit_b == 'yes' else 'no'

    # Contact title
    contact_title = random.choice(TITLES)
    agent_title   = random.choice(TITLES)

    contact_first, contact_last = rand_name()
    agent_first,   agent_last   = rand_name()

    # Assets – whole dollars
    def wa(mn=0, mx=500000): return whole_amount(mn, mx)

    # Trustee
    has_corp_trustee = random.random() > 0.5
    trustee_name = f"{last1} Pty Ltd" if has_corp_trustee else ''
    trustee_abn  = rand_abn()          if has_corp_trustee else ''

    with open('smsf_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    replacements = {
        '{{TFN}}': tfn,
        '{{FUND_NAME}}': fund_name,
        '{{ABN}}': rand_abn(),
        '{{AUDIT_A_NO}}':     x(audit_a == 'no'),
        '{{AUDIT_A_YES}}':    x(audit_a == 'yes'),
        '{{AUDIT_B_NO}}':     x(audit_b == 'no'),
        '{{AUDIT_B_YES}}':    x(audit_b == 'yes'),
        '{{AUDIT_RECT_NO}}':  x(audit_r == 'no'),
        '{{AUDIT_RECT_YES}}': x(audit_r == 'yes'),
        '{{EFT_A_BSB}}':     rand_bsb(),
        '{{EFT_A_ACCOUNT}}': rand_account(),
        '{{EFT_A_NAME}}':    fund_name,
        '{{EFT_B_BSB}}':     rand_bsb(),
        '{{EFT_B_ACCOUNT}}': rand_account(),
        '{{EFT_B_NAME}}':    fund_name,
        '{{ESA}}':           random.choice(ESA_ALIASES),
        '{{ECPI_NO}}':       ecpi_no,
        '{{ECPI_YES}}':      ecpi_yes,
        '{{ECPI_AMOUNT}}':   ecpi_amount,
        '{{ECPI_SEG}}':      ecpi_seg,
        '{{ECPI_UNSEG}}':    ecpi_unseg,
        '{{ACTUARIAL_CERT}}': actuarial,
        '{{ECPI_E_YES}}':    ecpi_e_yes,
        '{{ECPI_E_NO}}':     ecpi_e_no,
        '{{MGMT_EXPENSE_J1}}': wa(1000, 20000),
        '{{MGMT_EXPENSE_J2}}': wa(0, 5000),
        '{{TAX_LOSSES_U}}':    wa(0, 50000),
        '{{CAPITAL_LOSSES_V}}': wa(0, 50000),
        '{{MEMBERS_HTML}}':    build_members_html(num_members),
        # Assets
        '{{ASSET_LISTED_TRUSTS}}':   wa(0, 300000),
        '{{ASSET_UNLISTED_TRUSTS}}': wa(0, 100000),
        '{{ASSET_INSURANCE}}':       wa(0, 200000),
        '{{ASSET_OTHER_MANAGED}}':   wa(0, 300000),
        '{{ASSET_J1}}': wa(0, 500000),
        '{{ASSET_J2}}': wa(0, 300000),
        '{{ASSET_J3}}': wa(0, 200000),
        '{{ASSET_J4}}': wa(0, 800000),
        '{{ASSET_J5}}': wa(0, 200000),
        '{{ASSET_J6}}': wa(0, 100000),
        '{{ASSET_CASH}}':          wa(0, 500000),
        '{{ASSET_DEBT}}':          wa(0, 100000),
        '{{ASSET_LOANS}}':         wa(0, 100000),
        '{{ASSET_LISTED_SHARES}}': wa(0, 800000),
        '{{ASSET_UNLISTED_SHARES}}': wa(0, 100000),
        '{{ASSET_LRBA}}':          wa(0, 300000),
        '{{ASSET_NON_RES}}':       wa(0, 500000),
        '{{ASSET_RES}}':           wa(0, 800000),
        '{{ASSET_COLLECTABLES}}':  wa(0, 50000),
        '{{ASSET_OTHER}}':         wa(0, 50000),
        '{{LIABILITIES_TOTAL}}':   wa(0, 200000),
        # Contact
        '{{CONTACT_MR}}':          checkbox_title(contact_title, 'Mr'),
        '{{CONTACT_MRS}}':         checkbox_title(contact_title, 'Mrs'),
        '{{CONTACT_MISS}}':        checkbox_title(contact_title, 'Miss'),
        '{{CONTACT_MS}}':          checkbox_title(contact_title, 'Ms'),
        '{{CONTACT_OTHER_TITLE}}': contact_title if contact_title == 'Dr' else '',
        '{{CONTACT_FAMILY_NAME}}': contact_last,
        '{{CONTACT_FIRST_NAME}}':  contact_first,
        '{{CONTACT_OTHER_NAMES}}': random.choice(FIRST_NAMES),
        '{{CONTACT_PHONE}}':       rand_phone(),
        '{{CONTACT_EMAIL}}':       rand_email(contact_first, contact_last),
        '{{TRUSTEE_NAME}}':        trustee_name,
        '{{TRUSTEE_ABN}}':         trustee_abn,
        # Agent
        '{{AGENT_MR}}':          checkbox_title(agent_title, 'Mr'),
        '{{AGENT_MRS}}':         checkbox_title(agent_title, 'Mrs'),
        '{{AGENT_MISS}}':        checkbox_title(agent_title, 'Miss'),
        '{{AGENT_MS}}':          checkbox_title(agent_title, 'Ms'),
        '{{AGENT_OTHER_TITLE}}': agent_title if agent_title == 'Dr' else '',
        '{{AGENT_FAMILY_NAME}}': agent_last,
        '{{AGENT_FIRST_NAME}}':  agent_first,
        '{{AGENT_PRACTICE}}':    random.choice(PRACTICES),
        '{{AGENT_REF}}':         str(random.randint(10000000, 99999999)),
        '{{AGENT_NUMBER}}':      str(random.randint(10000000, 99999999)),
        '{{AGENT_PHONE}}':       rand_phone(),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(key, str(value))

    pdfkit.from_string(html, output_path, configuration=config, options=PDF_OPTIONS)
    print(f"Generated: {output_path}  ({num_members} members)")

# ── run ──────────────────────────────────────────────────────────────────────
os.makedirs('output', exist_ok=True)

for members in range(1, 7):
    for i in range(1, 3):
        generate_form(f'output/smsf_return_{members}members_{i}.pdf', num_members=members)

print("\nAll PDFs generated in the 'output' folder.")