import pandas as pd

# data = [
#     {"Name": "Alex", "Age": 28, "Salary": 50000},
#     {"Name": "Bob", "Age": 22, "Salary": 45000},
#     {"Name": "Alice", "Age": 24, "Salary": 30000}
# ]

data = [
    {"Name":"Alex", "Number": "+7 701"},
    {"Name":"Bob", "Number": "+7 702"}
]


df = pd.DataFrame(data)

print(df)