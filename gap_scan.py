from airtable_client import get_records
from datetime import datetime

def get_requirement_coverage():
    """
    Build a lookup dict: requirement record ID -> list of document records
    One requirement can be covered by multiple documents.
    """
    records = get_records("Document Records")
    coverage = {}
    for r in records:
        fields = r.get("fields", {})
        linked = fields.get("Linked Requirement", [])
        for req_id in linked:
            if req_id not in coverage:
                coverage[req_id] = []
            coverage[req_id].append(r)
    return coverage

def evaluate_status(doc_records):
    """
    Given a list of document records covering a requirement,
    return the most relevant status.
    Priority: Complete > Expiring Soon > Expiring Critical > Expired > Pending
    """
    statuses = [r.get("fields", {}).get("Status", "Unknown") for r in doc_records]
    
    if "Complete" in statuses:
        return "Complete"
    elif "Expiring Soon" in statuses:
        return "Expiring Soon"
    elif "Expiring Critical" in statuses:
        return "Expiring Critical"
    elif "Expired" in statuses:
        return "Expired"
    elif "Pending" in statuses:
        return "Pending"
    else:
        return "Unknown"

def run_gap_scan():
    print("Fetching requirements...")
    requirements = get_records("Document Requirements")
    
    print("Fetching document records...")
    coverage = get_requirement_coverage()
    
    results = {
        "Complete": [],
        "Expiring Soon": [],
        "Expiring Critical": [],
        "Expired": [],
        "Pending": [],
        "Missing": [],
        "Unknown": [],
    }

    for req in requirements:
        fields = req.get("fields", {})
        req_id = req["id"]
        name = fields.get("Record Title", "Unknown")

        if req_id not in coverage:
            results["Missing"].append(name)
        else:
            status = evaluate_status(coverage[req_id])
            results[status].append(name)

    # Sort each category
    for key in results:
        results[key].sort(key=lambda x: (
            x.split(" | ")[1],
            int(x.split(" | ")[0])
        ))

    # Print summary
    print(f"\n{'='*60}")
    print(f"GAP SCAN RESULTS")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    for status, docs in results.items():
        if docs:
            print(f"\n{status} ({len(docs)}):")
            for name in docs:
                print(f"  - {name}")

if __name__ == "__main__":
    run_gap_scan()
