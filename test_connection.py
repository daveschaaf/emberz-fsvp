from airtable_client import get_records, create_record, update_record, delete_record

# Test create
print("Testing create...")
record = create_record("Actions", {
    "Action Type": "Review Required",
    "Priority": "Medium",
    "Status": "Open",
    "Detail": "Test record — safe to delete"
})
record_id = record["id"]
print(f"  Created: {record_id}")

# Test update
print("Testing update...")
update_record("Actions", record_id, {"Status": "Resolved"})
print(f"  Updated status to Resolved")

# Test delete
print("Testing delete...")
delete_record("Actions", record_id)
print(f"  Deleted successfully")

print("All operations working.")
