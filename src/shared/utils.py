from typing import Optional, Type, TypeVar, Callable

T = TypeVar("T")

def get_input(prompt: str, cast_type: Type[T], error_msg: str = "Invalid input. Please try again.") -> Optional[T]:
    """Generic input helper with type casting and error handling. Returns None if input is empty."""
    while True:
        val = input(prompt).strip()
        if not val:
            return None
        try:
            return cast_type(val)
        except (ValueError, TypeError):
            print(error_msg)

def get_confirmation(prompt: str) -> bool:
    """Helper to handle yes/no confirmations."""
    while True:
        val = input(f"{prompt} (y/n): ").strip().lower()
        if val == 'y':
            return True
        if val == 'n':
            return False
        print("Please enter 'y' for yes or 'n' for no.")


def display_table(header: str, rows: list[str], footer: Optional[str] = None):
    """Generic table renderer for CLI."""
    print()
    if not rows:
        print("No data found.")
        return

    print(header)
    print("-" * len(header))
    
    for row in rows:
        print(row)
    
    if footer:
        print("-" * len(header))
        print(footer)
    print()
