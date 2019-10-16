# Module to create file paths across operating systems
import os
# Module for reading CSV files
import csv
# Set path for file
filepath = os.path.join('.', 'Resources', 'budget_data.csv')

# Lists to store data
budget_data = []

# Open the CSV
with open(filepath) as csvfile:
    reader = csv.DictReader(csvfile)

    # Loop through data to store into a dictionary
    for row in reader:
        budget_data.append(
            {
                "month": row["Date"],
                "amount": int(row["Profit/Losses"]),
                "change": 0
            }
        )


# Calculate total months
total_months = len(budget_data)

# Loop through dictionary to calculate changes between months
prev_amount = budget_data[0]["amount"]
for i in range(total_months):
    budget_data[i]["change"] = budget_data[i]["amount"] - prev_amount
    prev_amount = budget_data[i]["amount"]

# Calculate total amount
total_amount = sum(row['amount'] for row in budget_data) 

# Calculate the average of amount changes
total_change = sum(row['change'] for row in budget_data)
average = round(total_change / (total_months-1), 2)

# Get Greatest Increase and Decrease from changes
gt_increase = max(budget_data, key=lambda x:x['change'])
gt_decrease = min(budget_data, key=lambda x:x['change'])


# Print the analysis to the terminal 
print('Financial Analysis')
print('----------------------------')
print(f'Total Months: {total_months}')
print(f'Total: ${total_amount}')
print(f'Average Change: ${average}')
print(f'Greatest Increase in Profits: {gt_increase["month"]} (${gt_increase["change"]})')
print(f'Greatest Decrease in Profits: {gt_decrease["month"]} (${gt_decrease["change"]})')


# Print the analysis to text file 
# Set path for file
filepath = os.path.join('.', 'Resources', 'PyBank_Results.txt')
with open(filepath, "w") as text_file:
    print('Financial Analysis', file=text_file)
    print('----------------------------', file=text_file)
    print(f'Total Months: {total_months}', file=text_file)
    print(f'Total: ${total_amount}', file=text_file)
    print(f'Average Change: ${average}', file=text_file)
    print(f'Greatest Increase in Profits: {gt_increase["month"]} (${gt_increase["change"]})', file=text_file)
    print(f'Greatest Decrease in Profits: {gt_decrease["month"]} (${gt_decrease["change"]})', file=text_file)