# Attendance Manager

A simple CLI tool to tracker attendance built with Pandas, and CSV files.

The app store attendance in CSV files

- Overall data in `Data/Overall.csv`
- each subject's data in separate CSV files in `Data/Sub/`.

## Features

- View overall and subject-wise attendance in table format.
- Add attendance for an existing subject.
- Toggle attendance for a recorded lecture date.
- Add new subjects from the CLI.
- Persist attendance data locally as CSV files.

## Project Structure

```text
.
├── Data
│   ├── Overall.csv
│   └── Sub
│       └── DSA.csv
├── README.md
├── main.py
├── requirements.txt
├── run.sh
└── setup.sh
```

## Requirements

- Python

Python packages:

- `tabulate`
- `pandas`

## Setup

Run the setup script in the project folder

```sh
sh setup.sh
```

## Running the App

After setup, you can start the app with:

```sh
sh run.sh
```

## Usage

When the app starts, it prints the current attendance tables and shows a menu:

```text
1. Add Attendance
2. Toggle Attendance
3. Add Sub
4. Exit
```

### Add Attendance

Choose `1`, select a subject by index, then enter:

- `P`/`p` for present
- `A`/`a` for absent

### Toggle Attendance

Choose `2`, select a subject, then enter the lecture date exactly as shown in the subject table.

Example date format:

```text
Wed May 06 2026
```

tip - copy form the subject table

### Add Subject

Choose `3` and enter the subject name.

## Data Format

`Data/Overall.csv` uses this format:

```csv
Subject,Present,Total Classes,Attendance Percentage,Last Updated
DSA,0,0,0.0,Wed May 06 2026
Overall,0,0,0.0,Wed May 06 2026
```

Each subject file in `Data/Sub/` uses this format:

```csv
Lec_Date,Status
Wed May 06 2026,True
```
