import click
import os
import subprocess
import time
from jut.registry import register_command


@register_command()
@click.argument("command")
@click.option("-r", "--max-retries", default=5, help="The number of retries")
@click.option("-d", "--delay", default=1, help="The delay in seconds between retries")
def retry(command, max_retries, delay):
    attempt = 0
    while attempt < max_retries:
        try:
            # Run the command in the terminal
            result = subprocess.run(
                command, shell=True, check=True, text=True, capture_output=False
            )
            # print(f"Command succeeded: {result.stdout}")
            return result.stdout  # Return the command output if successful
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            if attempt < max_retries:
                time.sleep(delay)  # Wait before retrying
    raise Exception(f"All retries failed for command: {command}")
