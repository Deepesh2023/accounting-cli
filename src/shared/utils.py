from typing import Optional, Type, TypeVar, Callable

T = TypeVar("T")

def get_input(prompt: str, cast_type: Type[T], error_msg: str = "Invalid input. Please try again.") -> T:
    """Generic input helper with type casting and error handling."""
    while True:
        val = input(prompt).strip()
        if not val:
            print("Input cannot be empty.")
            continue
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
