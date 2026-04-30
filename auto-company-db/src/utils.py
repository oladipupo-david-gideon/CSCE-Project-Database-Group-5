def print_dynamic_table(headers, data_rows):
    """
    Dynamically prints a formatted table adjusting to the longest string in each column.
    """
    if not data_rows:
        print("No data available.")
        return

    # Convert everything to strings first so we can measure the length
    string_rows = [[str(item) if item is not None else "NULL" for item in row] for row in data_rows]
    
    # Find the maximum width for each column (start with header lengths)
    col_widths = [len(str(h)) for h in headers]
    
    for row in string_rows:
        for i, item in enumerate(row):
            col_widths[i] = max(col_widths[i], len(item))

    # Create the format string dynamically (e.g., "{:<20} | {:<15}")
    format_str = " | ".join([f"{{:<{width}}}" for width in col_widths])
    
    # Print Header
    print("\n" + format_str.format(*headers))
    
    # Print a separator line that matches the total table width
    total_width = sum(col_widths) + (3 * (len(headers) - 1)) 
    print("-" * total_width)
    
    # Print all the rows
    for row in string_rows:
        print(format_str.format(*row))