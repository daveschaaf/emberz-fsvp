from airtable_client import get_records, create_record

def get_program_id(program_code):
    records = get_records("FSVP Programs")
    for r in records:
        if r["fields"].get("Program ID") == program_code:
            return r["id"]
    raise ValueError(f"Program {program_code} not found in Airtable")

REQUIREMENTS_ES_CMC = [
    # ── FOUNDATION ──────────────────────────────────────────
    {"Document Name": "FSVP Program Document",                  "Category": "Foundation",          "CFR Reference": "21 CFR 1.502",               "Validity Days": 0},
    {"Document Name": "Qualified Individual Designation",       "Category": "Foundation",          "CFR Reference": "21 CFR 1.503",               "Validity Days": 0},
    {"Document Name": "Qualified Auditor Designation",          "Category": "Foundation",          "CFR Reference": "21 CFR 1.503(b)",            "Validity Days": 0},
    {"Document Name": "Written Procedures - Approved Supplier", "Category": "Foundation",          "CFR Reference": "21 CFR 1.506(a)(1)",         "Validity Days": 0},
    {"Document Name": "Written Procedures - Verification",      "Category": "Foundation",          "CFR Reference": "21 CFR 1.506(b)",            "Validity Days": 0},
    # ── HAZARD ANALYSIS ─────────────────────────────────────
    {"Document Name": "Written Hazard Analysis",                "Category": "Hazard Analysis",     "CFR Reference": "21 CFR 1.504(a)",            "Validity Days": 1095},
    {"Document Name": "Biological Hazard Assessment",           "Category": "Hazard Analysis",     "CFR Reference": "21 CFR 1.504(b)(1)",         "Validity Days": 1095},
    {"Document Name": "Chemical Hazard Assessment",             "Category": "Hazard Analysis",     "CFR Reference": "21 CFR 1.504(b)(1)",         "Validity Days": 1095},
    {"Document Name": "Physical Hazard Assessment",             "Category": "Hazard Analysis",     "CFR Reference": "21 CFR 1.504(b)(1)",         "Validity Days": 1095},
    {"Document Name": "Hazard Probability & Severity",          "Category": "Hazard Analysis",     "CFR Reference": "21 CFR 1.504(c)(1)",         "Validity Days": 1095},
    {"Document Name": "Hazard Control Determination",           "Category": "Hazard Analysis",     "CFR Reference": "21 CFR 1.504",               "Validity Days": 1095},
    # ── SUPPLIER EVALUATION ──────────────────────────────────
    {"Document Name": "Supplier Food Safety Assessment",        "Category": "Supplier Evaluation", "CFR Reference": "21 CFR 1.505(a)(1)(iii)(A)", "Validity Days": 1095},
    {"Document Name": "FDA Compliance Check",                   "Category": "Supplier Evaluation", "CFR Reference": "21 CFR 1.505(a)(1)(iii)(B)", "Validity Days": 365},
    {"Document Name": "Supplier Food Safety History",           "Category": "Supplier Evaluation", "CFR Reference": "21 CFR 1.505(a)(1)(iii)(C)", "Validity Days": 1095},
    {"Document Name": "Hazard Control Entity Identification",   "Category": "Supplier Evaluation", "CFR Reference": "21 CFR 1.505(a)(1)(ii)",    "Validity Days": 1095},
    {"Document Name": "Supplier Approval Documentation",        "Category": "Supplier Evaluation", "CFR Reference": "21 CFR 1.505(b)",            "Validity Days": 1095},
    {"Document Name": "Sub-Supplier Verification",              "Category": "Supplier Evaluation", "CFR Reference": "21 CFR 1.506(d)(1)(i)",     "Validity Days": 1095},
    # ── VERIFICATION ────────────────────────────────────────
    {"Document Name": "Verification Activity Determination",    "Category": "Verification",        "CFR Reference": "21 CFR 1.506(d)(1)",         "Validity Days": 1095},
    {"Document Name": "Onsite Audit Report",                    "Category": "Verification",        "CFR Reference": "21 CFR 1.506(e)(1)(i)",      "Validity Days": 365},
    {"Document Name": "Verification Results Review",            "Category": "Verification",        "CFR Reference": "21 CFR 1.506(e)(3)",         "Validity Days": 365},
    # ── CORRECTIVE ACTIONS ───────────────────────────────────
    {"Document Name": "Corrective Action Records",              "Category": "Corrective Actions",  "CFR Reference": "21 CFR 1.508(a)",            "Validity Days": 0},
    # ── REEVALUATION ────────────────────────────────────────
    {"Document Name": "3-Year Reevaluation Record",             "Category": "Reevaluation",        "CFR Reference": "21 CFR 1.505(c)(2)",         "Validity Days": 1095},
    # ── ENTRY & RECORDS ─────────────────────────────────────
    {"Document Name": "DUNS Number on File",                    "Category": "Entry & Records",     "CFR Reference": "21 CFR 1.509",               "Validity Days": 0},
    {"Document Name": "FSVP Importer ID at Entry",              "Category": "Entry & Records",     "CFR Reference": "21 CFR 1.509(a)",            "Validity Days": 0},
]

def populate(program_code, requirements):
    print(f"Fetching record ID for {program_code}...")
    program_record_id = get_program_id(program_code)
    print(f"  Found: {program_record_id}")

    print(f"Creating {len(requirements)} requirement records...")
    for req in requirements:
        req["FSVP Program"] = [program_record_id]
        record = create_record("Document Requirements", req)
        print(f"  Created: {record['fields'].get('Record Title', req['Document Name'])}")

    print(f"\nDone. {len(requirements)} records created for {program_code}.")

populate("FSVP-ES-CBC", REQUIREMENTS_ES_CMC)
