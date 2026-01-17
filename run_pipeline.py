import subprocess
import sys
import time

def run_pipeline(script_name):
    print(f'Running {script_name}...')
    try:    
        subprocess.run([sys.executable, script_name])
        print(f'{script_name} stage completed successfully.\n')
    except subprocess.CalledProcessError:
        print(f'{script_name} stage failed. Exiting pipeline.')
        sys.exit(1)


if __name__ == "__main__":
    start_time = time.time()

    run_pipeline('ingest_api.py')
    run_pipeline('scrape_market.py')
    run_pipeline('refine_silver.py')
    run_pipeline('gold_volatility_alert.py')

    end_time = time.time()
    duration = round(end_time - start_time, 2)
    print(f'Pipeline completed in {duration} seconds.')