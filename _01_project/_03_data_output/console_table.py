import os
from typing import List


class ConsoleTable:
    """A simple class to display and update a dynamic box-style table in the console."""

    def __init__(self, title: str, headers: List[str]):
        """
        Initialize the table with headers.

        Args:
            headers (list of str): The header names for the table columns.
        """
        self.title: str = title
        self.headers: List[str] = headers
        self.rows: List[str] = []
        self.col_widths = [len(header) for header in headers]

    def clear_console(self):
        """Clear the console output."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_widths(self, new_row: List[str]):
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

    def add_rows(self, new_rows: List[List[str]]):
        """
        Add multiple new rows to the table and redraw.

        Args:
            new_rows (list of list): List of rows to add, each row is a list of strings.
        """
        self.rows.clear()
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
        print(separator)
        print(self._make_row(self.headers))
        print(separator)
        for row in self.rows:
            print(self._make_row(row))
            print(separator)
