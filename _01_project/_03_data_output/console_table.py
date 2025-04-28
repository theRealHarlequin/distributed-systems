import os


class ConsoleTable:
    """A simple class to display and update a dynamic box-style table in the console."""

    def __init__(self, title, headers):
        """
        Initialize the table with headers.

        Args:
            headers (list of str): The header names for the table columns.
        """
        self.title = title
        self.headers = headers
        self.rows = []
        self.col_widths = [len(header) for header in headers]

    def clear_console(self):
        """Clear the console output."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_widths(self, new_row):
        """
        Update the column widths based on a new row.

        Args:
            new_row (list): A single row of data (list of strings).
        """
        for idx, value in enumerate(new_row):
            if idx < len(self.col_widths):
                self.col_widths[idx] = max(self.col_widths[idx], len(str(value)))
            else:
                # Handle case where a new row has more columns than headers
                self.col_widths.append(len(str(value)))

    def add_rows(self, new_rows):
        """
        Add multiple new rows to the table and redraw.

        Args:
            new_rows (list of list): List of rows to add, each row is a list of strings.
        """
        for row in new_rows:
            self.update_widths(row)
            self.rows.append(row)
        self.display()

    def _make_separator(self):
        """Create a separator line like +-----+------+."""
        return '+' + '+'.join('-' * (width + 2) for width in self.col_widths) + '+'

    def _make_row(self, row):
        """Format a single row with | and proper spacing."""
        return '|' + '|'.join(f" {str(cell):<{self.col_widths[idx]}} " for idx, cell in enumerate(row)) + '|'

    def display(self):
        """Clear console and display the updated table."""
        self.clear_console()

        separator = self._make_separator()
        print(self.title)
        print("")
        print(separator)
        print(self._make_row(self.headers))
        print(separator)
        for row in self.rows:
            print(self._make_row(row))
        print(separator)


# Example usage
if __name__ == "__main__":
    title = """                                                       _ _             _             
                                                      (_) |           (_)            
 ___  ___ _ __  ___  ___  _ __   _ __ ___   ___  _ __  _| |_ ___  _ __ _ _ __   __ _ 
/ __|/ _ \ '_ \/ __|/ _ \| '__| | '_ ` _ \ / _ \| '_ \| | __/ _ \| '__| | '_ \ / _` |
\__ \  __/ | | \__ \ (_) | |    | | | | | | (_) | | | | | || (_) | |  | | | | | (_| |
|___/\___|_| |_|___/\___/|_|    |_| |_| |_|\___/|_| |_|_|\__\___/|_|  |_|_| |_|\__, |
                                                                                __/ |
                                                                               |___/ 
"""
    table = ConsoleTable(title=title,headers=["Name", "Age", "City"])
    table.add_rows([
        ["Alice", "30", "New York"],
        ["Bob", "25", "Los Angeles"]
    ])
    input("Press Enter to add more rows...")
    table.add_rows([
        ["Christina", "29", "San Francisco"],
        ["Dave", "32", "Houston"]
    ])
    input("Press Enter to add more rows...")