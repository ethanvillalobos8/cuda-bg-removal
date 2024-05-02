from prettytable import PrettyTable


def create_table(small_count, small_avg_size, small_avg_time, small_total_time, large_count, large_avg_size,
                 large_avg_time, large_total_time):
    table = PrettyTable()
    table.field_names = ['Image Size', 'Count', 'Average Size (KB)', 'Average Time (sec)', 'Total Time (sec)']

    # Add small files data
    table.add_row(['Under 1MB', small_count, f"{small_avg_size / 1024:.2f}", f"{small_avg_time:.2f}",
                   f"{small_total_time:.2f}"])

    # Add large files data
    table.add_row(
        ['1-10MB', large_count, f"{large_avg_size / 1024:.2f}", f"{large_avg_time:.2f}", f"{large_total_time:.2f}"])

    print(table)
