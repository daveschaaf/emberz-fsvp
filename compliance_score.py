from airtable_client import get_records, update_record
from datetime import datetime

def calculate_scores():
    print("Fetching programs...")
    programs = get_records("FSVP Programs")
    
    print("Fetching requirements...")
    requirements = get_records("Document Requirements")
    
    print("Fetching document records...")
    doc_records = get_records("Document Records")

    # Build requirement coverage: req_id -> list of document records
    coverage = {}
    for r in doc_records:
        linked = r.get("fields", {}).get("Linked Requirement", [])
        for req_id in linked:
            if req_id not in coverage:
                coverage[req_id] = []
            coverage[req_id].append(r)

    # Group requirements by program
    reqs_by_program = {}
    for req in requirements:
        fields = req.get("fields", {})
        linked_programs = fields.get("FSVP Program", [])
        for prog_id in linked_programs:
            if prog_id not in reqs_by_program:
                reqs_by_program[prog_id] = []
            reqs_by_program[prog_id].append(req)

    # Calculate score per program
    print(f"\n{'='*60}")
    print(f"COMPLIANCE SCORES")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")

    for program in programs:
        prog_record_id = program["id"]
        prog_id = program["fields"].get("Program ID", "Unknown")
        
        program_reqs = reqs_by_program.get(prog_record_id, [])
        total = len(program_reqs)
        
        if total == 0:
            print(f"{prog_id}: No requirements found — skipping")
            continue

        complete = 0
        expired = 0
        missing = 0

        for req in program_reqs:
            req_id = req["id"]
            if req_id not in coverage:
                missing += 1
            else:
                statuses = [
                    r.get("fields", {}).get("Status", "Unknown")
                    for r in coverage[req_id]
                ]
                if "Complete" in statuses:
                    complete += 1
                elif "Expired" in statuses:
                    expired += 1
                else:
                    missing += 1

        score = round((complete / total) * 100)

        # Determine overall status
        if score == 100:
            overall_status = "Compliant"
        elif expired > 0 or score < 50:
            overall_status = "Critical"
        elif score < 80:
            overall_status = "Gaps Present"
        else:
            overall_status = "Minor Gaps"

        print(f"{prog_id}: {score}% | {complete}/{total} complete | "
              f"{expired} expired | {missing} missing | {overall_status}")

        # Write to Airtable
        update_record("FSVP Programs", prog_record_id, {
            "Compliance Score": score,
            "Overall Status": overall_status,
            "Open Gaps": missing + expired,
            "Last Agent Run": datetime.now().isoformat(),
        })
        print(f"  ✓ Airtable updated")

if __name__ == "__main__":
    calculate_scores()
