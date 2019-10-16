# Module to create file paths across operating systems
import os
# Module for reading CSV files
import csv
# Set path for file
filepath = os.path.join('.', 'Resources', 'election_data.csv')

# Open the CSV
with open(filepath, newline='') as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    # Read the header row first 
    csv_header = next(csvreader)

    candidate_list = [candidate[2] for candidate in csvreader]
    
# Calculate total votes
total_votes = len(candidate_list)

# Create a unique list of candidates with the number of votes for each
canditates_info = [[candidate,candidate_list.count(candidate)] for candidate in set(candidate_list)]

# Sort the list so the first is the winner
canditates_info = sorted(canditates_info, key=lambda x: x[1], reverse=True)

# Print election results to the terminal 
print("Election Results")
print("-------------------------")
print(f"Total Votes: {total_votes}")
print("-------------------------")

for candidate in canditates_info:
    percent_votes = (candidate[1] / total_votes) * 100
    print(f'{candidate[0]}: {percent_votes:6.3f}% ({candidate[1]})')

print("-------------------------")
print(f"Winner: {canditates_info[0][0]}")
print("-------------------------")


#  Print election results to text file 
# Set path for file
filepath = os.path.join('.', 'Resources', 'PyPoll_Results.txt')
with open(filepath, "w") as text_file:
    print("Election Results", file=text_file)
    print("-------------------------", file=text_file)
    print(f"Total Votes: {total_votes}", file=text_file)
    print("-------------------------", file=text_file)

    for candidate in canditates_info:
        percent_votes = (candidate[1] / total_votes) * 100
        print(f'{candidate[0]}: {percent_votes:6.3f}% ({candidate[1]})', file=text_file)

    print("-------------------------", file=text_file)
    print(f"Winner: {canditates_info[0][0]}", file=text_file)
    print("-------------------------", file=text_file)
