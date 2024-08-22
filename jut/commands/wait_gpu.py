import click
from jut.registry import register_command
import subprocess
import time


@register_command()
@click.option(
    "-t", "--threshold", default=10, help="The threshold utilization percentage"
)
@click.option(
    "-i", "--interval", default=5, help="The interval in seconds between checks"
)
def wait_gpu(threshold, interval):
    print("Waiting for a free GPU...")
    while True:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            stdout=subprocess.PIPE,
            text=True,
        )
        gpu_utilizations = result.stdout.splitlines()

        for gpu_id, utilization in enumerate(gpu_utilizations):
            utilization = int(utilization)
            if utilization < threshold:
                print(f"GPU {gpu_id} is free with utilization {utilization}%")
                return gpu_id

        print(f"No GPU is free. Checking again in {interval} seconds...")
        time.sleep(interval)
