import json

# Process and stream logs
for log in logs_with_metadata:
    object_name = log["name"]
    print(f"\n🔄 Processing: {object_name} (modified at {log['time_modified']})")

    # Download the object content
    obj = object_storage.get_object(namespace, bucket_name, object_name)
    content = obj.data.content.decode("utf-8")

    try:
        # Assuming the log structure is like: {"date": "...", "log": "<escaped JSON string>"}
        outer_json = json.loads(content)

        if "log" in outer_json:
            # Remove escape characters and load the inner JSON
            fixed_log = json.loads(outer_json["log"])
            outer_json["log"] = fixed_log  # Replace with parsed JSON

        # Do something with cleaned log
        print("✅ Cleaned Log:", json.dumps(outer_json, indent=2))

    except json.JSONDecodeError as e:
        print(f"❌ JSON decode failed for object {object_name}: {e}")
