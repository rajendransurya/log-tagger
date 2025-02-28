import csv
from collections import defaultdict


def read_lookup_table(lookup_file):
    """
    Load the lookup file
    """
    lookup_dict = {}
    with open(lookup_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (int(row['dstport']), row['protocol'].lower())  # Normalize protocol case
            lookup_dict[key] = row['tag']
    return lookup_dict


def count_write_flow_logs(flow_log_file, lookup_dict, tagged_logs_file, count_file):
    """
    Parse the flow logs and count he tags and port protocol counts
    """
    tagged_logs = {}
    port_protocol_counts = defaultdict(int)
    protocol_map={6:"tcp",17:"udp",1:"icmp"}
    with open(flow_log_file, "r") as file:
        for line in file:
            fields = line.strip().split()
            if len(fields) < 10:
                continue  # Skip invalid lines
            dstport = int(fields[6])
            protocol = protocol_map[int(fields[7])]
            tag = lookup_dict.get((dstport, protocol), "Unknown")
            tagged_logs[tag]=tagged_logs.get(tag,0)+1
            port_protocol_counts[(dstport, protocol)] += 1
    write_tag_count(tagged_logs_file, tagged_logs)
    write_port_protocol_counts(count_file, port_protocol_counts)
def write_tag_count(tagged_logs_file, tagged_logs):
    # Write tagged logs file
    with open(tagged_logs_file, "w",newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Count"])
        for tag,count in tagged_logs.items():
            writer.writerow([tag,count])
    print(f"Tagged logs saved to {tagged_logs_file}")
def write_port_protocol_counts(count_file, port_protocol_counts):
    # Write port/protocol count file
    with open(count_file, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            writer.writerow([port, protocol, count])
    print(f"Port/Protocol counts saved to {count_file}")


def parse_logs_write_results(flow_log_file, lookup_file, tagged_logs_file, count_file):
    """Main function to process logs and generate output files."""
    lookup_dict = read_lookup_table(lookup_file)
    count_write_flow_logs(flow_log_file, lookup_dict, tagged_logs_file, count_file)

# Example usage:
parse_logs_write_results("flow_logs.txt", "tag_list.csv", "tag_counts.csv", "port_protocol_counts.csv")