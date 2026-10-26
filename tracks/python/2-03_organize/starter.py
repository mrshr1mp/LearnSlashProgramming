"""organize: sort the files in a folder into subfolders by type.

Read the mission brief for the rules. You write everything below.
"""


def plan(folder):
    """Return {filename: destination_folder_name} for each file in folder. Moves nothing."""
    raise NotImplementedError


def organize(folder, dry_run=True):
    """Return the plan. If dry_run is False, actually move the files (never overwrite)."""
    raise NotImplementedError


if __name__ == "__main__":
    # Your call. Try it on ../samples/messy
    pass
