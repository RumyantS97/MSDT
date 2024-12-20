"""Starter module of pixel python game."""

# Add some info for each imports
import base64
import glob
import multiprocessing
import os
import pathlib
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile

import pixel
import pixel.utils

METADATA_FIELDS = ["title", "author", "desc", "site", "license", "version"]

def cli():
    """Define a command-line interface for interacting
    with various functions related to a retro game engine called Pixel.

    :return: The `cli()` function returns the appropriate usage information
    based the command line arguments provided by the user. If the arguments
    match a defined command, the corresponding function associated with that
    command is executed. If the arguments do not match any command or if the
    number parameters is incorrect, an error message is displayed along with
    the correct usage information.

    """
    commands = [
        (["run", "PYTHON_SCRIPT_FILE(.py)"], run_python_script),
        (
            ["watch", "WATCH_DIR", "PYTHON_SCRIPT_FILE(.py)"],
            watch_and_run_python_script,
        ),
        (
            ["play", f"PIXEL_APP_FILE({pixel.APP_FILE_EXTENSION})"],
            play_pixel_app,
        ),
        (
            [
                "edit",
                f"[PIXEL_RESOURCE_FILE({pixel.RESOURCE_FILE_EXTENSION})]",
            ],
            edit_pixel_resource,
        ),
        (
            ["package", "APP_DIR", "STARTUP_SCRIPT_FILE(.py)"],
            package_pixel_app,
        ),
        (
            ["app2exe", f"PIXEL_APP_FILE({pixel.APP_FILE_EXTENSION})"],
            create_executable_from_pixel_app,
        ),
        (
            ["app2html", f"PIXEL_APP_FILE({pixel.APP_FILE_EXTENSION})"],
            create_html_from_pixel_app,
        ),
        (["copy_examples"], copy_pixel_examples),
    ]

    def print_usage(command_name=None):
        """The function `print_usage` prints the usage information for a given command
        or all commands if no specific command is provided.

        :param command_name: The `command_name` parameter in the `print_usage`
        function is used to specify a particular command for which the usage
        information should be printed. If `command_name` is provided, only the
        usage information for that specific command will be displayed. If
        `command_name` is not provided (i.e)

        """
        print("usage:")
        for command in commands:
            if command_name is None or command[0] == command_name:
                print(f"    pixel {' '.join(command[0])}")
        _check_newer_version()

    num_args = len(sys.argv)
    if num_args <= 1:
        print(f"Pixel {pixel.VERSION}, a retro game engine for Python")
        print_usage()
        return
    for command in commands:
        if sys.argv[1] != command[0][0]:
            continue
        max_args = len(command[0]) + 1
        min_args = max_args - len(list(filter(lambda s: s.startswith("["), command[0])))
        if min_args <= num_args <= max_args:
            command[1](*sys.argv[2:])
            return
        else:
            print("invalid number of parameters")
            print_usage(command[0])
            sys.exit(1)
    print(f"invalid command: '{sys.argv[1]}'")
    print_usage()
    sys.exit(1)


def _check_newer_version():
    """The function checks for a newer version of Pixel by scraping the GitHub page
    and comparing it with the current version.

    :return: The `_check_newer_version` function is returning `None` if there is an
    error during the URL request or if the latest version is not found in the
    response. If a new version is found and it is greater than the current version
    of Pixel, a message is printed indicating that a new version is available.

    """
    url = "https://www.github.com/kitao/pixel"
    req = urllib.request.Request(url)
    latest_version = None
    try:
        with urllib.request.urlopen(req, timeout=3) as res:
            pattern = r"/kitao/pixel/releases/tag/v(\d+\.\d+\.\d+)"
            text = res.read().decode("utf-8")
            result = re.search(pattern, text)
            if result:
                latest_version = result.group(1)
    except urllib.error.URLError:
        return
    if not latest_version:
        return

    def parse_version(version):
        return list(map(int, version.split(".")))

    if parse_version(latest_version) > parse_version(pixel.VERSION):
        print(f"A new version, Pixel {latest_version}, is available.")


def _complete_extension(filename, command, valid_ext):
    """The function `_complete_extension` ensures that a given filename has a
    specificvalid extension and handles cases where the extension is missing
    or incorrect.

    :param filename: The `filename` parameter is a string representing the name
    ofa file
    :param command: The `command` parameter is a string representing the name
    of a command or operation being performed
    :param valid_ext: The `valid_ext` parameter in the `_complete_extension`
    function represents the valid file extension that the `command`
    is expecting.
    This parameter is used to ensure that the filename provided matches the
    expected file extension. If the file extension of the provided
    filename does not match the `valid_ext`, an error

    :return: The function `_complete_extension` returns the `filename` after
    ensuring that it has the correct extension based on the `valid_ext`
    parameter.
    If the `filename` does not have an extension, it appends the `valid_ext`
    to it.
    If the existing extension of the `filename` does not match the `valid_ext`,
    it prints an error message and exits the program.

    """  # noqa: D205
    file_ext = os.path.splitext(filename)[1].lower()
    if not file_ext:
        filename += valid_ext
    elif file_ext != valid_ext:
        print(f"'{command}' command only accepts {valid_ext} files")
        sys.exit(1)
    return filename


def _files_in_dir(dirname):
    """The function `_files_in_dir` returns a sorted list of
    file paths within a specified directory.

    :param dirname: The `dirname` parameter in the `_files_in_dir`
    function is a string representing the directory path for which you want
    to find all files

    :return: The function `_files_in_dir` returns a sorted list of file paths
    within the specified directory `dirname`.
    """
    paths = glob.glob(os.path.join(dirname, "**/*"), recursive=True)
    return sorted(list(filter(os.path.isfile, paths)))


def _check_file_exists(filename):
    """The function `_check_file_exists` checks if a file exists and
    prints an error message if it does not.

    :param filename: The `filename` parameter is a string that represents
    the name of the file that needs to be checked for existence. The function
    `_check_file_exists` takes this filename as input and checks if the file
    exists in the file system. If the file does not exist, it prints a message
    indicating that the

    """
    if not os.path.isfile(filename):
        print(f"no such file: '{filename}'")
        sys.exit(1)


def _check_dir_exists(dirname):
    """The function checks if a directory exists and exits the program
    if it does not.

    :param dirname: The `dirname` parameter in the `_check_dir_exists`function
    is a string representing the name of a directory. The function checks
    if the directory exists on the file system. If the directory does not
    exist, it prints a message indicating that the directory does not exist
    and exits the program with a status
    """
    if not os.path.isdir(dirname):
        print(f"no such directory: '{dirname}'")
        sys.exit(1)


def _check_file_under_dir(filename, dirname):
    """The function `_check_file_under_dir` checks if a specified file is located
    under a specified directory.

    :param filename: The `filename` parameter is a string that represents the path
    to a file in the file system
    :param dirname: The `dirname` parameter in the `_check_file_under_dir` function
    represents the directory path where the file should be located. This function
    is designed to check if the specified `filename` is under the `dirname`
    directory. If the file is not under the specified directory, it will print a
    message
    """
    if os.path.relpath(filename, dirname).startswith(".."):
        print("specified file is not under the directory")
        sys.exit(1)


def _create_app_dir():
    """The function `_create_app_dir` creates a temporary directory for an
    application, removing any existing directories associated with the application
    process.
    :return: The function `_create_app_dir` returns the path to the newly created
    application directory `app_dir`.
    """
    play_dir = os.path.join(tempfile.gettempdir(), pixel.BASE_DIR, "play")
    pathlib.Path(play_dir).mkdir(parents=True, exist_ok=True)
    for path in glob.glob(os.path.join(play_dir, "*")):
        pid = int(os.path.basename(path))
        if not pixel.process_exists(pid):
            shutil.rmtree(path)
    app_dir = os.path.join(play_dir, str(os.getpid()))
    if os.path.exists(app_dir):
        shutil.rmtree(app_dir)
    os.mkdir(app_dir)
    return app_dir


def _create_watch_info_file():
    """The function `_create_watch_info_file` creates a watch directory, removes any
    existing files that do not correspond to active processes, and then creates a
    new watch info file with the current process ID.
    :return: The function `_create_watch_info_file` returns the path to the watch
    info file that is created within the specified watch directory.
    """
    watch_dir = os.path.join(tempfile.gettempdir(), pixel.BASE_DIR, "watch")
    pathlib.Path(watch_dir).mkdir(parents=True, exist_ok=True)
    for path in glob.glob(os.path.join(watch_dir, "*")):
        pid = int(os.path.basename(path))
        if not pixel.process_exists(pid):
            os.remove(path)
    watch_info_file = os.path.join(watch_dir, str(os.getpid()))
    with open(watch_info_file, "w") as f:
        f.write("")
    return watch_info_file


def _timestamps_in_dir(dirname):
    """This Python function retrieves the last modification timestamps of files in a
    specified directory and its subdirectories.

    :param dirname: The `dirname` parameter in the `_timestamps_in_dir` function is
    a string representing the directory path where you want to search for files and
    retrieve their timestamps
    :return: A dictionary containing the file paths in the specified directory
    along with their corresponding modification timestamps.
    """
    paths = glob.glob(os.path.join(dirname, "*"))
    paths += glob.glob(os.path.join(dirname, "*/*"))
    paths += glob.glob(os.path.join(dirname, "*/*/*"))
    files = filter(os.path.isfile, paths)
    timestamps = {}
    for file in files:
        timestamps[file] = os.path.getmtime(file)
    return timestamps


def _run_python_script_in_separate_process(python_script_file):
    """The function `_run_python_script_in_separate_process` creates a separate
    process to run a Python script file.

    :param python_script_file: The `python_script_file` parameter is a string that
    represents the file path of the Python script that you want to run in a
    separate process. This function `_run_python_script_in_separate_process`
    creates a new process using the `multiprocessing` module in Python to execute
    the specified Python script file
    :return: The function `_run_python_script_in_separate_process` is returning the
    `worker` process that was started to run the Python script in a separate
    process.
    """
    worker = multiprocessing.Process(
        target=run_python_script, args=(python_script_file,)
    )
    worker.daemon = True
    worker.start()
    return worker


def _extract_pixel_app(pixel_app_file):
    """The function `_extract_pixel_app` extracts a Pixel app file, searches for a
    specific startup script file, and returns the path to the script file if found.

    :param pixel_app_file: The `pixel_app_file` parameter is the file path to a
    Pixel application file that you want to extract information from. This function
    is designed to extract a specific setting file from the Pixel application
    archive
    :return: The function `_extract_pixel_app` is returning the path to the startup
    script file of a Pixel application.
    """
    _check_file_exists(pixel_app_file)
    app_dir = _create_app_dir()
    zf = zipfile.ZipFile(pixel_app_file)
    zf.extractall(app_dir)
    pattern = os.path.join(app_dir, "*", pixel.APP_STARTUP_SCRIPT_FILE)
    for setting_file in glob.glob(pattern):
        with open(setting_file, "r") as f:
            return os.path.join(os.path.dirname(setting_file), f.read())
    return None


def _make_metadata_comment(startup_script_file):
    """The function `_make_metadata_comment` reads a startup script file
    to extract specific metadata fields and formats them into a comment block.

    :param startup_script_file: The function `_make_metadata_comment` reads a
    startup script file and extracts metadata information from comments in the
    file. The metadata fields it looks for are "title", "author", "desc", "site",
    "license", and "version". It then formats this metadata into a comment block
    :return: The function `_make_metadata_comment` is returning a formatted
    metadata comment extracted from a startup script file. The comment includes
    metadata fields such as title, author, description, site, license, and version.
    The function reads the startup script file, extracts metadata using a regular
    expression pattern, formats the metadata comment, and returns it. If no
    metadata is found in the file, an empty string is returned.
    """
    metadata = {}
    metadata_pattern = re.compile(r"#\s*(.+?)\s*:\s*(.+)")
    with open(startup_script_file, "r", encoding="utf8") as f:
        for line in f:
            match = metadata_pattern.match(line)
            if match:
                key, value = match.groups()
                key = key.strip().lower()
                if key in METADATA_FIELDS:
                    metadata[key] = value.strip()
    if not metadata:
        return ""
    metadata_comment = ""
    max_key_len = max(len(key) for key in metadata)
    max_value_len = max(len(value) for _, value in metadata.items())
    border = "-" * min((max_key_len + max_value_len + 3), 80)
    metadata_comment = border + "\n"
    for key in METADATA_FIELDS:
        if key in metadata:
            value = metadata[key]
            metadata_comment += f"{key.ljust(max_key_len)} : {value}\n"
    metadata_comment += border
    return metadata_comment


def run_python_script(python_script_file):
    """The function `run_python_script` runs a Python script file as the
    main program.

    :param python_script_file: The `python_script_file` parameter is a string
    thatrepresents the file path of the Python script that you want to run
    using the `run_python_script` function.

    """
    python_script_file = _complete_extension(python_script_file, "run", ".py")
    _check_file_exists(python_script_file)
    sys.path.append(os.path.dirname(python_script_file))
    runpy.run_path(python_script_file, run_name="__main__")


def watch_and_run_python_script(watch_dir, python_script_file):
    """This Python function watches a directory for changes and reruns a specified
    Python script when changes are detected.

    :param watch_dir: The `watch_and_run_python_script` function seems to be
    designed to watch a directory for changes and run a Python script whenever
    a change is detected. The function takes two parameters:
    :param python_script_file: The `python_script_file` parameter is the
    file path of the Python script that you want to watch and run whenever
    changes occur in the specified `watch_dir`.

    """
    python_script_file = _complete_extension(python_script_file, "watch", ".py")
    _check_dir_exists(watch_dir)
    _check_file_exists(python_script_file)
    _check_file_under_dir(python_script_file, watch_dir)
    os.environ[pixel.WATCH_INFO_FILE_ENVVAR] = _create_watch_info_file()
    try:
        print(f"start watching '{watch_dir}' (Ctrl+C to stop)")
        cur_time = last_time = time.time()
        timestamps = _timestamps_in_dir(watch_dir)
        worker = _run_python_script_in_separate_process(python_script_file)
        while True:
            time.sleep(0.5)
            cur_time = time.time()
            if cur_time - last_time >= 10:
                last_time = cur_time
                print(f"watching '{watch_dir}' (Ctrl+C to stop)")
            last_timestamps = timestamps
            timestamps = _timestamps_in_dir(watch_dir)
            if timestamps != last_timestamps:
                print(f"rerun {python_script_file}")
                worker.terminate()
                worker = _run_python_script_in_separate_process(python_script_file)
    except KeyboardInterrupt:
        print("\r", end="")
        print("stopped watching")


def get_pixel_app_metadata(pixel_app_file):
    """The function `get_pixel_app_metadata` extracts metadata from a Pixel
    application file.

    :param pixel_app_file: The `pixel_app_file` parameter is a file path to
    a Pixel application file. This function `get_pixel_app_metadata` reads
    the metadata from the Pixel application file and returns it as a dictionary
    :return: An empty dictionary is being returned if the zipfile comment is
    emptyor does not contain any key-value pairs. If the comment contains
    key-value pairs, a dictionary with the extracted metadata
    is being returned.

    """
    _check_file_exists(pixel_app_file)
    metadata = {}
    zf = zipfile.ZipFile(pixel_app_file)
    if zf.comment:
        comment = zf.comment.decode(encoding="utf-8")
    else:
        return metadata
    for line in comment.splitlines():
        if line.startswith("-"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata


def print_pixel_app_metadata(pixel_app_file):
    """The function `print_pixel_app_metadata` reads a Pixel application file,
    checks if it exists, and prints the comment metadata if available.

    :param pixel_app_file: The `print_pixel_app_metadata` function
    takes a Pixel app file as input and prints out any metadata stored in
    the file's comment section. The `pixel_app_file` parameter should be the
    path to the Pixel app file that you want to extract metadata from
    """
    _check_file_exists(pixel_app_file)
    zf = zipfile.ZipFile(pixel_app_file)
    if zf.comment:
        print(zf.comment.decode(encoding="utf-8"))


def play_pixel_app(pixel_app_file):
    """The `play_pixel_app` function plays a Pixel application by running
    its startup script.

    :param pixel_app_file: The `play_pixel_app` function seems to be a Python
    function that plays a Pixel app. The function takes a `pixel_app_file`
    parameter, which is the file path of the Pixel app to be played
    :return: The function `play_pixel_app` returns None.

    """
    pixel_app_file = _complete_extension(
        pixel_app_file, "play", pixel.APP_FILE_EXTENSION
    )
    _check_file_exists(pixel_app_file)
    print_pixel_app_metadata(pixel_app_file)
    startup_script_file = _extract_pixel_app(pixel_app_file)
    if startup_script_file:
        sys.path.append(os.path.dirname(startup_script_file))
        runpy.run_path(startup_script_file, run_name="__main__")
        return
    print(f"file not found: '{pixel.APP_STARTUP_SCRIPT_FILE}'")
    sys.exit(1)


def edit_pixel_resource(pixel_resource_file=None, starting_editor="image"):
    """The function `edit_pixel_resource` opens the Pixel editor with a specified
    resource file and starting editor.

    :param pixel_resource_file: The `pixel_resource_file` parameter is a string
    that represents the file path of the Pixel resource file that you want
    to edit.
    If this parameter is not provided, the default value is set
    to "my_resource".
    This file should be a Pixel resource file with the appropriate extension
    :param starting_editor: The `starting_editor` parameter in the
    `edit_pixel_resource` function is used to specify the initial edito
    mode when opening the Pixel resource file. It determines whether the
    resource file willbe opened in the "image" editor mode or another
    specified mode, defaults to image (optional)
    """
    import pixel.editor

    if not pixel_resource_file:
        pixel_resource_file = "my_resource"
    pixel_resource_file = _complete_extension(
        pixel_resource_file, "edit", pixel.RESOURCE_FILE_EXTENSION
    )
    pixel.editor.App(pixel_resource_file, starting_editor)


def package_pixel_app(app_dir, startup_script_file):
    """The function `package_pixel_app` packages a Pixel application
    by creating a zip file containing the necessary files and metadata.

    :param app_dir: The `app_dir` parameter in the `package_pixel_app` function
    refers to the directory where the Pixel application files are located. This
    function is designed to package a Pixel application by creating a zip file
    containing the necessary files for the application to run
    :param startup_script_file: The `startup_script_file` parameter is the file
    that contains the main script of the Pixel application that you want to
    package. This script is the entry point of your Pixel application
    and will be included in the packaged application.

    """
    startup_script_file = _complete_extension(startup_script_file, "package", ".py")
    _check_dir_exists(app_dir)
    _check_file_exists(startup_script_file)
    _check_file_under_dir(startup_script_file, app_dir)
    metadata_comment = _make_metadata_comment(startup_script_file)
    if metadata_comment:
        print(metadata_comment)
    app_dir = os.path.abspath(app_dir)
    setting_file = os.path.join(app_dir, pixel.APP_STARTUP_SCRIPT_FILE)
    with open(setting_file, "w") as f:
        f.write(os.path.relpath(startup_script_file, app_dir))
    pixel_app_file = os.path.basename(app_dir) + pixel.APP_FILE_EXTENSION
    app_parent_dir = os.path.dirname(app_dir)
    with zipfile.ZipFile(
        pixel_app_file,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zf:
        zf.comment = metadata_comment.encode(encoding="utf-8")
        files = [setting_file] + _files_in_dir(app_dir)
        for file in files:
            if os.path.basename(file) == (pixel_app_file or "/__pycache__/" in file):
                continue
            arcname = os.path.relpath(file, app_parent_dir)
            zf.write(file, arcname)
            print(f"added '{arcname}'")
    os.remove(setting_file)


def create_executable_from_pixel_app(pixel_app_file):
    """This Python function creates an executable file from a Pixel application
    file.

    :param pixel_app_file: The `pixel_app_file` parameter in the
    `create_executable_from_pixel_app` function is the file path to the Pixel
    application file that you want to convert into an executable. This function
    takes this file path as input and performs the necessary steps to create an
    executable from the.

    """
    pixel_app_file = _complete_extension(
        pixel_app_file, "app2exe", pixel.APP_FILE_EXTENSION
    )
    _check_file_exists(pixel_app_file)
    app2exe_dir = os.path.join(tempfile.gettempdir(), pixel.BASE_DIR, "app2exe")
    if os.path.isdir(app2exe_dir):
        shutil.rmtree(app2exe_dir)
    pathlib.Path(app2exe_dir).mkdir(parents=True, exist_ok=True)
    pixel_app_name = os.path.splitext(os.path.basename(pixel_app_file))[0]
    startup_script_file = os.path.join(app2exe_dir, pixel_app_name + ".py")
    with open(startup_script_file, "w") as f:
        f.write(
            "import os, pixel.cli; pixel.cli.play_pixel_app("
            "os.path.join(os.path.dirname(__file__), "
            f"'{pixel_app_name}{pixel.APP_FILE_EXTENSION}'))"
        )
    cp = subprocess.run("pyinstaller -h", capture_output=True, shell=True)
    if cp.returncode != 0:
        print("Pyinstaller is not found. Please install it.")
        sys.exit(1)
    command = f"{sys.executable}" "-m PyInstaller --windowed --onefile --distpath . "
    command += f"--add-data {pixel_app_file}{os.pathsep}. "
    modules = pixel.utils.list_imported_modules(_extract_pixel_app(pixel_app_file))[
        "system"
    ]
    command += "".join([f"--hidden-import {module} " for module in modules])
    command += startup_script_file
    print(command)
    subprocess.run(command, shell=True)
    if os.path.isdir(app2exe_dir):
        shutil.rmtree(app2exe_dir)
    spec_file = os.path.splitext(pixel_app_file)[0] + ".spec"
    if os.path.isfile(spec_file):
        os.remove(spec_file)


def create_html_from_pixel_app(pixel_app_file):
    """The function `create_html_from_pixel_app` generates an HTML
    file that embeds a Pixel app using base64 encoding.

    :param pixel_app_file: The `pixel_app_file` parameter is a file path to
    a Pixel application file that you want to convert to an HTML file for
    running in a web browser using Pixel's JavaScript library.

    """
    pixel_app_file = _complete_extension(
        pixel_app_file, "app2html", pixel.APP_FILE_EXTENSION
    )
    _check_file_exists(pixel_app_file)
    base64_string = ""
    with open(pixel_app_file, "rb") as f:
        base64_string = base64.b64encode(f.read()).decode()
    pixel_app_name = os.path.splitext(os.path.basename(pixel_app_file))[0]
    with open(pixel_app_name + ".html", "w") as f:
        f.write(
            "<!DOCTYPE html>\n"
            "<script "
            'src="https://cdn.jsdelivr.net/gh/kitao/pixel/wasm/pixel.js">'
            "</script>\n"
            "<script>\n"
            'launchPixel({{ command: "play", name: '
            f'"{pixel_app_name}{pixel.APP_FILE_EXTENSION}", '
            f'gamepad: "enabled", base64: "{base64_string}" }});\n'
            "</script>\n"
        )


def copy_pixel_examples():
    """The function `copy_pixel_examples` copies files from the "examples"
    directory to a destination directory "pixel_examples".

    """
    src_dir = os.path.join(os.path.dirname(__file__), "examples")
    dst_dir = "pixel_examples"
    shutil.rmtree(dst_dir, ignore_errors=True)
    for src_file in _files_in_dir(src_dir):
        dst_file = os.path.join(dst_dir, os.path.relpath(src_file, src_dir))
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copyfile(src_file, dst_file)
        print(f"copied '{dst_file}'")
