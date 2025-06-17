import os

class TableDisplay:
    def __init__(self):
        self.title = ""
        self.columns = []
        self.rows = []

    def create_table(self, title, columns):
        """Initializes the table with a title and column headers."""
        self.title = title
        self.columns = columns
        self.rows = []
        self._clear_console()
        print(f"Table '{title}' with columns {columns} created.")

    def add_row(self, values):
        """Adds a new row of data and refreshes the table display."""
        if len(values) != len(self.columns):
            print("Error: Number of values does not match number of columns!")
            return

        self.rows.append(values)
        self._clear_console()
        self._display_table()

    def _display_table(self):
        """Displays the table with borders and centered values."""
        # Determine column widths
        col_widths = [len(col) for col in self.columns]
        for row in self.rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))

        # Helper functions for borders
        def border_line():
            return "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

        def format_row(row):
            return "|" + "|".join(f" {str(val).center(w)} " for val, w in zip(row, col_widths)) + "|"

        # Display the table
        print(self.title)
        print(border_line())
        print(format_row(self.columns))
        print(border_line())
        for row in self.rows:
            print(format_row(row))
        print(border_line())

    def _clear_console(self):
        """Clears the terminal screen (Windows, Linux, macOS)."""
        os.system('cls' if os.name == 'nt' else 'clear')
