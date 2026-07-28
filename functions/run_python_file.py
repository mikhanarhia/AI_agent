import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", target_file]
        if args is not None:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_result = ""
        if result.returncode != 0:
            output_result = "Process exited with code X\n"
        if not result.stdout and not result.stderr:
            output_result += "\nNo output produced"
        if result.stdout:
            output_result += f"\nSTDOUT: {result.stdout}"
        if result.stderr:
            output_result += f"\nSTDERR: {result.stderr}"
        return output_result




    except Exception as e:
        return f"Error: {e}"
