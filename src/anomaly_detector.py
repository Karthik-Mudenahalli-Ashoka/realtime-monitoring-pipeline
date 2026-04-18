import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies():
    # Load data from database
    conn = sqlite3.connect('pipeline.db')
    df = pd.read_sql_query("SELECT * FROM metrics", conn)
    conn.close()

    print(f"📊 Loaded {len(df)} records from database")

    # Features for anomaly detection
    features = ['cpu_usage', 'memory_usage', 'network_io']
    X = df[features]

    # Train Isolation Forest
    model = IsolationForest(contamination=0.05, random_state=42)
    predictions = model.fit_predict(X)

    # -1 = anomaly, 1 = normal → convert to 0/1
    df['is_anomaly'] = (predictions == -1).astype(int)

    anomaly_count = df['is_anomaly'].sum()
    print(f"🚨 Detected {anomaly_count} anomalies out of {len(df)} records "
          f"({anomaly_count/len(df)*100:.1f}%)")

    # Update database with anomaly labels
    conn = sqlite3.connect('pipeline.db')
    c = conn.cursor()
    for _, row in df.iterrows():
        c.execute(
            "UPDATE metrics SET is_anomaly = ? WHERE id = ?",
            (int(row['is_anomaly']), int(row['id']))
        )
    conn.commit()
    conn.close()

    print("✅ Anomaly labels saved to database!")
    return df

if __name__ == "__main__":
    df = detect_anomalies()
    print("\nSample anomalies:")
    print(df[df['is_anomaly'] == 1][['timestamp', 'cpu_usage', 
                                      'memory_usage', 'network_io']].head())