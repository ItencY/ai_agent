import subprocess
import os

def run_python_file(working_directory, file_path):
    """
    Executes a Python file within a specified working directory.

    Args:
        working_directory (str): The directory in which the Python file should be executed.
        file_path (str): The path to the Python file to execute.

    Returns:
        str: A formatted string containing the stdout, stderr, and exit code of the
             executed process, or an error message if an issue occurs.
    """
    # Construct the absolute path for the working directory and the file path
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # 1. Check if the file_path is outside the working directory
    # This checks if the absolute file path starts with the absolute working directory path
    # and ensures that the resolved path is indeed within the working directory structure.
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # 2. Check if the file_path exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    # 3. Check if the file ends with ".py"
    if not file_path.lower().endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Execute the Python file using subprocess.run
        # - [sys.executable, abs_file_path]: Runs the Python interpreter with the specified file.
        # - cwd: Sets the current working directory for the subprocess.
        # - timeout: Limits execution time to 30 seconds.
        # - capture_output=True: Captures stdout and stderr.
        # - text=True: Decodes stdout and stderr as text using default encoding.
        result = subprocess.run(
            [os.sys.executable, abs_file_path],
            cwd=abs_working_directory,
            timeout=30,
            capture_output=True,
            text=True
        )

        output_parts = []

        # Add STDOUT if available
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")

        # Add STDERR if available
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")

        # Add exit code if non-zero
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        # If no output was produced
        if not output_parts:
            return "No output produced."
        else:
            return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        # Handle cases where the process exceeds the timeout
        # Access stdout/stderr from the exception object
        stdout_output = f"STDOUT:\n{e.stdout.strip()}" if e.stdout else ""
        stderr_output = f"STDERR:\n{e.stderr.strip()}" if e.stderr else ""
        timeout_message = f"Error: Process timed out after 30 seconds."
        
        # Combine parts, ensuring to only add non-empty strings
        output_parts = [part for part in [stdout_output, stderr_output, timeout_message] if part]
        return "\n".join(output_parts)

    except Exception as e:
        # Catch any other exceptions during execution
        return f"Error: executing Python file: {e}"
