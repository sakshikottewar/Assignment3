Facility Dataset Analysis

A short Python script that loads a facility inspection dataset, cleans it, computes key statistics, generates insights, and produces 5 charts.

Files
File	Description
facilityAnalysis.py	Main analysis script
facility_data.csv	Input dataset (must be in the same folder)
facility_analysis.png	Output chart image (generated after running)
Requirements
Python 3.9+
pandas
matplotlib

Install dependencies:

bash
pip install pandas matplotlib
Setup
Place facilityAnalysis.py and facility_data.csv in the same folder.
Open a terminal in that folder.
How to Run
bash
python facilityAnalysis.py

No arguments needed. The script reads facility_data.csv from the current folder and writes facility_analysis.png to the current folder.

Note: If you get FileNotFoundError: facility_data.csv, make sure the CSV is in the same directory you're running the command from.

Dataset Columns Expected
Column	Type	Description
facility_id	string	Unique facility identifier
location	string	Zone (North / South / East / West / Central)
cleanliness_score	float (0–10)	Inspection cleanliness rating
odor_score	float (0–10)	Inspection odor rating
waste_level	string	Low / Medium / High
water_availability	string	Yes / No
footfall	int	Daily visitor count
complaints	int	Number of complaints logged
inspection_date	date	Date of inspection
What the Script Does
Load — reads the CSV, parses inspection_date as a real date.
Audit — counts missing values, duplicate facility_ids, negative footfall, and out-of-range (0–10) scores, before touching the data.
Clean — drops duplicate rows, converts invalid footfall to missing, fills missing numeric values with the column median.
Outlier detection — flags values outside the IQR bounds (Q1 - 1.5×IQR to Q3 + 1.5×IQR) for each numeric column.
Statistics — mean, std, min, median, max overall, plus averages grouped by location.
Insights — three auto-generated, data-driven takeaways.
Charts — saves one PNG containing:
Bar chart: avg cleanliness score by location
Bar chart: facility count by waste level
Histogram: cleanliness score distribution
Scatter plot: footfall vs complaints (colored by odor score)
Pie chart: water availability split
Expected Output

Console output (values will vary slightly with random seed / real data):

=== DATA QUALITY REPORT ===
missing_values: {'facility_id': 0, 'location': 0, 'cleanliness_score': 16, 'odor_score': 0, 'waste_level': 0, 'water_availability': 0, 'footfall': 0, 'complaints': 0, 'inspection_date': 0}
duplicate_facility_ids: 5
negative_footfall: 3
out_of_range_scores: 0
outliers: {'cleanliness_score': 3, 'odor_score': 4, 'footfall': 0, 'complaints': 26}

=== KEY STATISTICS ===
                      mean     std   min    50%    max
cleanliness_score    6.94    1.43   1.2    6.9   10.0
odor_score            2.94    1.14   0.0    2.9    6.4
footfall            261.19  139.58  20.0  263.0  499.0
complaints             1.49    1.15   0.0    1.0    6.0

=== AVERAGES BY LOCATION ===
           cleanliness_score  odor_score  footfall  complaints
location
Central                 6.95        2.85    255.99        1.56
East                    6.98        3.07    259.80        1.44
North                   6.92        2.87    252.87        1.40
South                   7.23        3.01    270.74        1.49
West                    6.68        2.93    269.10        1.56

=== INSIGHTS ===
1. 'West' has the lowest avg cleanliness score (6.68) — needs priority attention.
2. Cleanliness vs complaints correlation = -0.01 (cleaner facilities get fewer complaints).
3. 12.2% of facilities lack water availability — a direct hygiene risk.

Saved charts -> facility_analysis.png

Plus a file facility_analysis.png in the same folder, containing 5 subplots:

Top-left — Bar chart: average cleanliness score per location
Top-middle — Bar chart: facility count per waste level
Top-right — Histogram: distribution of cleanliness scores
Bottom-left — Scatter plot: footfall vs complaints (color = odor score)
Bottom-middle — Line chart: weekly average cleanliness trend
Bottom-right — Pie chart: water availability (Yes/No split)
Troubleshooting
Error	Cause	Fix
FileNotFoundError: facility_data.csv	CSV not in the working folder	Move the CSV next to the script, or cd into the correct folder
FileNotFoundError: '/mnt/user-data/outputs/...'	Leftover sandbox output path	In make_charts(), change out_path default to "facility_analysis.png"
ModuleNotFoundError: pandas / matplotlib	Dependencies not installed	Run pip install pandas matplotlib
