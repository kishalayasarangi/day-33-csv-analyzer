# CSV Analysis Report
**File:** sample_students.csv
**Rows:** 100 | **Columns:** 8

## Columns
- `student_id` (int64)
- `name` (str)
- `age` (int64)
- `branch` (str)
- `cgpa` (float64)
- `attendance` (int64)
- `projects` (int64)
- `placement` (str)

## Numeric Summary
       student_id         age        cgpa  attendance    projects
count  100.000000  100.000000  100.000000  100.000000  100.000000
mean    50.500000   21.270000    7.573800   76.980000    4.880000
std     29.011492    2.377738    1.494414   13.911684    3.121383
min      1.000000   18.000000    5.040000   50.000000    0.000000
25%     25.750000   19.000000    6.205000   65.750000    2.000000
50%     50.500000   21.000000    7.830000   77.000000    5.000000
75%     75.250000   23.000000    8.697500   89.000000    7.250000
max    100.000000   25.000000    9.880000   99.000000   10.000000

## Charts Generated
- charts/student_id_histogram.png
- charts/age_histogram.png
- charts/cgpa_histogram.png
- charts/attendance_histogram.png
- charts/name_barchart.png
- charts/branch_barchart.png
- charts/correlation_heatmap.png