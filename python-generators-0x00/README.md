# Python Generators - Streaming Data from SQL

This project demonstrates how to use **Python generators** to stream data **row by row** or in **batches** from a MySQL database. It includes database setup, data seeding from CSV, and processing using generators.

---

## 📁 Project Structure

```bash
python-generators-0x00/
├── 0-main.py                # Main script to test seed.py functionality
├── 0-stream_users.py        # Generator that streams one row at a time
├── 1-main.py                # Test script for streaming single users
├── 1-batch_processing.py    # Batch processing with filtering
├── 2-main.py                # Test script for batch processing
├── seed.py                  # Database setup and CSV seeding
├── user_data.csv            # Sample user data to populate the DB
└── README.md                # Project documentation
