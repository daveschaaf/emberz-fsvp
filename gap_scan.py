from airtable_client import get_records
from datetime import datetime

def get_document_records_by_requirement():
    """Build a lookup dict: requirement record ID -> document record"""
    records = get_records("Document Records")
    lookup = {}
    for r in records:
        fields = r.get("fields", {})
        linked = fields.get("Linked Requirement", [])
        if linked:
            lookup[linked[0]] = r
    return lookup

def run_gap_scan():
    print("Fetching requirements...")
    requirements = get_records("Document Requirements")
    
    print("Fetching document records...")
    doc_lookup = get_document_records_by_requirement()
    
    results = {"Missing": [], "Complete": [], "Other": []}

    for req in requirements:
        fields = req.get("fields", {})
        req_id = req["id"]
        name = fields.get("Record Title", "Unknown")

        if req_id not in doc_lookup:
            results["Missing"].append(name)
        else:
            status = doc_lookup[req_id].get("fields", {}).get("Status", "Unknown")
            if status == "Complete":
                results["Complete"].append(name)
            else:
                results["Other"].append(f"{name}: {status}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"GAP SCAN RESULTS")
    print(f"{'='*60}")
    print(f"Complete:  {len(results['Complete'])}")
    print(f"Missing:   {len(results['Missing'])}")
    print(f"Other:     {len(results['Other'])}")
    
    # Sort missing by the record title (which starts with the number)
    results["Missing"].sort(key=lambda x: (
        x.split(" | ")[1],  # FSVP Program
        int(x.split(" | ")[0])  # Requirement number
    ))
    print(f"\nMissing Documents:")
    for name in results["Missing"]:
        print(f"  - {name}")

if __name__ == "__main__":
    run_gap_scan()
