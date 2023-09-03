import multiprocessing

bind = "0.0.0.0:8000"  # Replace with your desired host and port
workers = multiprocessing.cpu_count() * 2 + 1  # Adjust the number of workers as needed
worker_class = "uvicorn.workers.UvicornWorker"  # Use the Uvicorn worker class
