"""
This script reads a lookup table and flow logs, tags the logs based on the lookup table, and counts the tags and port/protocol combinations.
The results are written to separate CSV files.
"""
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


def count_write_flow_logs(flow_log_file, lookup_dict, tagged_logs_file, port_protocol_count_file):
    """
    Parse the flow logs and count the tags and port protocol counts
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
    port_protocol_counts=[[port,protocol,count] for (port,protocol),count in port_protocol_counts.items()]
    _write_output_file(tagged_logs_file, ["Tag", "Count"], tagged_logs.items())
    _write_output_file(port_protocol_count_file, ["Port", "Protocol", "Count"], port_protocol_counts)
    print(f"Tag counts saved to {tagged_logs_file}")
    print(f"Port/Protocol counts saved to {port_protocol_count_file}")


def _write_output_file(filename, headers, data):
    """
    Write output file
    """
    with open(filename, "w",newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)


def parse_logs_write_results(flow_log_file, lookup_file, tagged_logs_file, count_file):
    """
    Parse logs and write results
    """
    lookup_dict = read_lookup_table(lookup_file)
    count_write_flow_logs(flow_log_file, lookup_dict, tagged_logs_file, count_file)

parse_logs_write_results("flow_logs.txt", "tag_list.csv", "tag_counts.csv", "port_protocol_counts.csv")