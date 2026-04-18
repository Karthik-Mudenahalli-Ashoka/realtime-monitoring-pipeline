import sqlite3
import time
import random
import numpy as np
from datetime import datetime

def init_db():
    conn = sqlite3.connect('pipeline.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_usage REAL,
            memory_usage REAL,
            network_io REAL,
            is_anomaly INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def generate_metric():
    # Normal operating ranges
    cpu = random.gauss(45, 10)       # avg 45%, std 10%
    memory = random.gauss(60, 8)     # avg 60%, std 8%
    network = random.gauss(100, 20)  # avg 100 MB/s

    # Inject anomaly 5% of the time
    if random.random() < 0.05:
        cpu = random.uniform(85, 100)
        memory = random.uniform(85, 100)
        network = random.uniform(200, 300)

    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_usage': round(max(0, min(100, cpu)), 2),
        'memory_usage': round(max(0, min(100, memory)), 2),
        'network_io': round(max(0, network), 2)
    }

def stream_data(duration_seconds=120):
    init_db()
    conn = sqlite3.connect('pipeline.db')
    c = conn.cursor()

    print(f"🚀 Streaming data for {duration_seconds} seconds...")
    for i in range(duration_seconds):
        metric = generate_metric()
        c.execute('''
            INSERT INTO metrics (timestamp, cpu_usage, memory_usage, network_io)
            VALUES (?, ?, ?, ?)
        ''', (metric['timestamp'], metric['cpu_usage'],
              metric['memory_usage'], metric['network_io']))
        conn.commit()

        print(f"[{metric['timestamp']}] CPU: {metric['cpu_usage']}% | "
              f"Memory: {metric['memory_usage']}% | "
              f"Network: {metric['network_io']} MB/s")
        time.sleep(1)

    conn.close()
    print("✅ Streaming complete!")

if __name__ == "__main__":
    stream_data(30)  # Run for 30 seconds