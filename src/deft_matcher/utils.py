import os
import re


def validate_file_path_has_version_and_return(file_path: str) -> str:
    """
    Validates that the file name has the format <prefix>_vYYYY-MM-DD.<extension>
    and returns the version string in the format 'vYYYY-MM-DD'.

    Example:
        'hp_v2026-02-16.obo' -> 'v2026-02-16'
        'data_v2026-02-16.json' -> 'v2026-02-16'
    """

    file_name = os.path.basename(file_path)

    pattern = r"^[a-zA-Z0-9]+_v(\d{4}-\d{2}-\d{2})\.[a-zA-Z0-9]+$"
    match = re.match(pattern, file_name)

    if not match:
        raise ValueError(
            f"Invalid file name format: {file_name}. Expected format: prefix_vYYYY-MM-DD.<extension>"
        )

    date_str = match.group(1)
    return f"v{date_str}"
