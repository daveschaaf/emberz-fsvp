from airtable_client import get_records, create_record
from datetime import datetime

def get_requirement_coverage():
    records = get_records("Document Records")
    coverage = {}
    for r in records:
        linked = r.get("fields", {}).get("Linked Requirement", [])
        for req_id in linked:
            if req_id not in coverage:
                coverage[req_id] = []
            coverage[req_id].append(r)
    return coverage

def evaluate_status(doc_records):
    statuses = [r.get("fields", {}).get("Status", "Unknown") for r in doc_records]
    if "Complete" in statuses:
        return "Complete", None
    elif "Expiring Critical" in statuses:
        rec = next(r for r in doc_records if r.get("fields", {}).get("Status") == "Expiring Critical")
        days = calculate_days_remaining(rec)
        return "Expiring Critical", days
    elif "Expiring Soon" in statuses:
        rec = next(r for r in doc_records if r.get("fields", {}).get("Status") == "Expiring Soon")
        days = calculate_days_remaining(rec)
        return "Expiring Soon", days
    elif "Expired" in statuses:
        rec = next(r for r in doc_records if r.get("fields", {}).get("Status") == "Expired")
        days = calculate_days_remaining(rec)
        return "Expired", days
    elif "Pending" in statuses:
        return "Pending", None
    return "Unknown", None

def calculate_days_remaining(doc_record):
    expiry_str = doc_record.get("fields", {}).get("Expiry Date", "")
    if not expiry_str:
        return None
    try:
        expiry = datetime.strptime(expiry_str[:10], "%Y-%m-%d").date()
        return (expiry - datetime.today().date()).days
    except:
        return None

def write_action_log():
    run_timestamp = datetime.now().isoformat()
    
    print("Fetching requirements...")
    requirements = get_records("Document Requirements")
    
    print("Fetching document records...")
    coverage = get_requirement_coverage()

    print("Writing action log...")
    logged = 0

    for req in requirements:
        req_id = req["id"]
        fields = req.get("fields", {})
        req_record_id = req["id"]
        prog_links = fields.get("FSVP Program", [])

        if req_id not in coverage:
            status = "Missing"
            days = None
            detail = f"No document on file for: {fields.get('Requirement Name', 'Unknown')}"
        else:
            status, days = evaluate_status(coverage[req_id])
            if status == "Complete":
                continue  # Don't log complete items — only log gaps
            detail = build_detail(status, days, fields)

        action = {
            "Linked Requirement": [req_record_id],
            "Status Found": status,
            "Detail": detail,
            "Run Timestamp": run_timestamp,
        }

        if days is not None:
            action["Days Until Expiry"] = days

        create_record("Actions", action)
        logged += 1

    print(f"\n{'='*60}")
    print(f"ACTION LOG")
    print(f"Run: {run_timestamp}")
    print(f"{'='*60}")
    print(f"Events logged: {logged}")

def build_detail(status, days, req_fields):
    name = req_fields.get("Requirement Name", "Unknown")
    if status == "Missing":
        return f"{name} — no document on file"
    elif status == "Expired":
        return f"{name} — expired {abs(days)} days ago"
    elif status == "Expiring Critical":
        return f"{name} — expires in {days} days. Immediate action required."
    elif status == "Expiring Soon":
        return f"{name} — expires in {days} days"
    elif status == "Pending":
        return f"{name} — document requested, awaiting receipt"
    return f"{name} — status unknown"

if __name__ == "__main__":
    write_action_log()
