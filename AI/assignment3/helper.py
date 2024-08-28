import re


def visible_length(s: str) -> int:
    """Calculates the length of a string excluding ASCII escape characters and codes

    Args:
        s (str): String whose length is to be calculated

    Returns:
        int: Length of the string excluding ASCII escape characters and codes
    """
    # Remove ANSI escape sequences
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    return len(ansi_escape.sub("", s))


def center_two_strings(s1: str, s2: str, width: int, filler: str = " ") -> str:
    """Center two strings in a line of a defined length

    Args:
        s1 (str): First string in the line
        s2 (str): Second string in the line
        width (int): Width of the line to be printed
        filler (str, optional): Padding is done using the specified fill character. Defaults to " ".

    Raises:
        ValueError: Total length of strings exceeds the specified width
        ValueError: Not enough space for filler between strings.

    Returns:
        str: Centered string of defined length
    """
    total_text_length = visible_length(s1) + visible_length(s2)
    if total_text_length > width:
        raise ValueError("Total length of strings exceeds the specified width.")

    # Calculate space required to fill the line to the desired width
    total_filler_space = width - total_text_length

    # Ensure there's at least one filler between the two strings
    if total_filler_space < 1:
        raise ValueError("Not enough space for filler between strings")

    # Divide space into three parts
    between_space = total_filler_space // 2
    remaining_space = total_filler_space - between_space

    # Print the two strings with fillers
    result = (
        filler * (remaining_space // 2)
        + s1
        + filler * between_space
        + s2
        + filler * (remaining_space - remaining_space // 2)
    )

    return result
