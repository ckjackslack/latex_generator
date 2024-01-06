import contextlib
import os
import shlex
import shutil
import subprocess
import tempfile

from settings import DIST_DIR


@contextlib.contextmanager
def tmpdir():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


@contextlib.contextmanager
def tmpfile():
    tempfile_path = tempfile.mktemp()
    try:
        yield tempfile_path
    finally:
        if os.path.exists(tempfile_path):
            os.remove(tempfile_path)


@contextlib.contextmanager
def chdir(new_path):
    original_path = os.getcwd()
    try:
        os.chdir(new_path)
        yield
    finally:
        os.chdir(original_path)


def run_command(command, input_data=None, decode_output=True):
    args = shlex.split(command)

    with subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as process:
        stdout_data, stderr_data = process.communicate(
            input=input_data.encode() if input_data is not None else None
        )
        if decode_output:
            stdout_data = stdout_data.decode()
            stderr_data = stderr_data.decode()

        exit_code = process.returncode

    return stdout_data, stderr_data, exit_code


def clean(name, path):
    for ext in ("aux", "log"):
        what = f"{os.path.join(path, name)}.{ext}"
        if os.path.isfile(what):
            os.remove(what)


def generate_pdf(filepath, content):
    os.makedirs(DIST_DIR, exist_ok=True)
    filename = os.path.basename(filepath)
    target_file = f"{os.path.join(DIST_DIR, filename)}.pdf"
    with tmpfile() as _file:
        where = os.path.dirname(_file)
        with chdir(where):
            with open(_file, mode="w") as fh:
                fh.write(content)
            out, err, exit_code = run_command(f"pdflatex {_file}")
            if err or exit_code != 0:
                print("Error code:", exit_code)
                print("Error:", err or out)
                return False
            name, _ = os.path.splitext(_file)
            cmd = f"mv {os.path.join(where, name)}.pdf {target_file}"
            run_command(cmd)
            clean(name, where)
    return os.path.exists(target_file)