import os
import re

status_path = "vendor/xiaomi/ice/status"
manifest_path = "out/target/product/ice/installed-files-vendor.txt"

if not os.path.exists(status_path):
    print(f"Error: Status file not found at {status_path}")
    exit(1)
if not os.path.exists(manifest_path):
    print(f"Error: Build manifest not found at {manifest_path}. Did you complete the build?")
    exit(1)

# Read the built target files layout
with open(manifest_path, "r") as f:
    manifest_content = f.read()

print("==================================================")
print("     AUDITING DELETED FILES AGAINST OUT TREE      ")
print("==================================================")

missing_count = 0
checked_count = 0

with open(status_path, "r") as f:
    for line in f:
        # Match standard git status short formats: " D path" or " M path" or just plain status lists
        match = re.search(r'(?:^[ \t]*[DM][ \t]+|^[ \t]*deleted:[ \t]+)?(?:proprietary/)?(vendor/.*)', line.strip())
        if match:
            # Extract the destination path inside the system image (e.g., vendor/lib/libxyz.so)
            target_path = match.group(1)
            checked_count += 1
            
            # Verify if this specific file component made it into the image manifest
            if target_path not in manifest_content:
                print(f"❌ DROPPED FROM BUILD: {target_path}")
                missing_count += 1

print("==================================================")
print(f"Audit Complete. Checked: {checked_count} | Dropped/Missing: {missing_count}")
if missing_count == 0:
    print("✨ Perfect! All modifications resolved. No essential files are missing.")
else:
    print("⚠️  Warning: Review the dropped files above to ensure they aren't needed by other modules.")
print("==================================================")
