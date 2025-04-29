import hashlib
import os
import csv
import argparse


def sha256_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def collect_files(directory_path):
    file_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, directory_path)
            file_paths.append((relative_path, full_path))
    return file_paths


def hash_directory(directory_path, output_csv):
    files = collect_files(directory_path)
    hash_list = []

    for relative_path, full_path in files:
        file_hash = sha256_hash(full_path)
        hash_list.append((relative_path, file_hash))

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Relative Path", "SHA256 Hash"])
        csv_writer.writerows(hash_list)

    print(f"✅ Hashes written to {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Generate SHA256 hashes for files in a directory.")
    parser.add_argument("directory", help="Path to the directory to scan")
    parser.add_argument("output", help="Path to the output CSV file")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"❌ Error: The directory '{args.directory}' does not exist.")
        return

    hash_directory(args.directory, args.output)


if __name__ == "__main__":
    main()