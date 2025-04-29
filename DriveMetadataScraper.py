import os
import csv
import argparse
from datetime import datetime

def get_file_metadata(root_folder):
    file_data = []
    for dirpath, _, filenames in os.walk(root_folder):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            try:
                stats = os.stat(file_path)
                file_data.append({
                    "Title": file,
                    "Folder Path": dirpath,
                    "Size (Bytes)": stats.st_size,
                    "File Type": os.path.splitext(file)[1].lower(),
                    "Date Created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "Date Modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
                })
            except Exception as e:
                print(f"Could not access {file_path}: {e}")
    return file_data

def save_to_csv(data, output_csv):
    fieldnames = ["Title", "Folder Path", "Size (Bytes)", "File Type", "Date Created", "Date Modified"]
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Extract metadata for all files in a folder recursively.")
    parser.add_argument("folder", help="Target folder to scan")
    args = parser.parse_args()

    root_folder = os.path.abspath(args.folder)
    folder_name = os.path.basename(os.path.normpath(root_folder))
    output_csv = f"{folder_name}.csv"

    print(f"Scanning: {root_folder}")
    metadata = get_file_metadata(root_folder)
    save_to_csv(metadata, output_csv)
    print(f"Metadata saved to {output_csv}")

if __name__ == "__main__":
    main()
