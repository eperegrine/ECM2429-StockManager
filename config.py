import pathlib
import sys

# SOURCE: get_datadir was sourced from https://stackoverflow.com/a/61901696
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform == "linux"
IS_WINDOWS = sys.platform == "win32"

DEV_MODE = True


def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if IS_WINDOWS:
        return home / "AppData/Roaming"
    elif IS_LINUX:
        return home / ".local/share"
    elif IS_MACOS:
        return home / "Library/Application Support"


# File locations
my_datadir = get_datadir() / "stock-manager"
app_dir = pathlib.Path(__file__).parents[0]
_db_filename = "stock_manager.db"
database_store = app_dir / _db_filename if DEV_MODE else my_datadir / _db_filename
sample_data_file_location = app_dir / "SQLScripts" / "SampleData.sql"

# Enaure that the path exists
try:
    my_datadir.mkdir(parents=True)
except FileExistsError:
    pass
