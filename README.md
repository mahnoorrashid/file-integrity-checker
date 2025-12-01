🔐 File Integrity Checker (Python)

A simple Python tool that monitors file integrity by creating a baseline of SHA-256 hashes and later detecting:
	•	Modified files
	•	New files
	•	Missing files

This type of tool is commonly used in cybersecurity for detecting unauthorized changes and verifying system integrity.

⸻

🚀 Features
	•	Generates a baseline of all files in a directory
	•	Stores hashes in baseline.json
	•	Detects:
	•	Modified files
	•	New files
	•	Deleted/missing files
	•	Uses secure SHA-256 hashing
	•	Beginner-friendly and fully CLI-based

⸻

🧭 How to Run
	1.	Make sure you have Python 3 installed.
	2.	Clone or download this repository.
	3.	Open a terminal in the project folder.

1️⃣ Create the baseline
python3 file_integrity_checker.py

Choose option 1, then enter the folder you want to monitor (or . for current folder).

2️⃣ Check integrity later
python3 file_integrity_checker.py

Choose option 2 to compare current files against the saved baseline.

📘 Example Output
🔐 Simple File Integrity Checker
1) Create / update baseline
2) Check integrity against baseline
Choose an option (1 or 2): 2

[+] Loaded baseline for: /Users/mahnoor/projects/file-integrity-checker
[*] Scanning current files...

===== INTEGRITY REPORT =====

Modified files:
  - report.txt

New files since baseline:
  - notes.txt

Missing files since baseline:
  - old_config.json

[+] Check complete.

🔐 Ethical & Practical Notes

This tool is for learning purposes and small personal projects.

Do not use it to monitor or check:
	•	Systems you do not own
	•	Corporate systems without permission
	•	Sensitive production environments

File integrity monitoring should always be done with proper authorization.

⸻

📝 Future Improvements
	•	Ignore certain file types (e.g. .log, .tmp)
	•	Add colored terminal output
	•	Add configuration file for custom rules
	•	Add option to export integrity reports to a file
	•	Add SHA-512 or Blake2b hashing options
	•	Add monitoring of subfolders with filters

⸻

👩🏽‍💻 Author

Mahnoor Rashid
Beginner Cybersecurity & Python Developer
