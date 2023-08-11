
import os
import re

def scan_file(file_path):
    patterns = [
        r'XMLHttpRequest',
        r'fetch\(',
        r'\$\s*\.ajax\(',
        r'navigator\.sendBeacon\(',
        r'"https?://\S+"|\'https?://\S+\''  # Detect URLs in string literals
    ]

    findings = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:  # Added errors='ignore' to handle potential encoding issues
        content = f.read()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                findings.append(match)

    return findings

def scan_directory(directory_path):
    all_findings = {}

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                findings = scan_file(file_path)
                if findings:
                    all_findings[file_path] = findings
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return all_findings

def report_findings(findings):
    for file_path, patterns in findings.items():
        print(f"In {file_path}, found:")
        for pattern in patterns:
            print(f"  - {pattern}")

# Example usage
directory_path = "extensions/" + "your/extension/folder/path/"
findings = scan_directory(directory_path)
report_findings(findings)
