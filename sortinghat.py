import re
import csv
from collections import Counter

# Path to the shared log file
log_file_path = r'\\172.16.14.3\Shared\access.log'

# Function to send email
def send_email(subject, message):
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@example.com"
    password = "your_password"  

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# Function to parse the log file
def parse_log_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    # Regular expression to match IP, timestamp, and URL in 404 errors
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) \S+ \S+ \[([^\]]+)\] "GET (\S+) HTTP/\d\.\d" 404')

    # Extract data
    data = [pattern.match(line).groups() for line in lines if pattern.match(line)]
    return data

# Function to write data to CSV
def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['IP Address', 'Timestamp', 'URL'])
        for row in data:
            writer.writerow(row)

# Main function
def main():
    data = parse_log_file(log_file_path)

    # Count occurrences of each IP address
    ip_count = Counter([row[0] for row in data])

    # Display the IPs sorted by the count of 404s
    for ip, count in ip_count.most_common():
        print(f'IP Address: {ip}, 404 Count: {count}')

    # Write data to CSV
    csv_filename = 'log_analysis.csv'
    write_to_csv(data, csv_filename)
    print(f'Data written to {csv_filename}')

if __name__ == '__main__':
    main()
