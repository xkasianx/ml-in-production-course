import pandas as pd
import numpy as np
import time
import os
import gc

def create_sample_dataframe(n_rows=1_000_000):
    """Creates a sample DataFrame with various data types."""
    df = pd.DataFrame({
        'int_col': np.random.randint(0, 100, size=n_rows),
        'float_col': np.random.rand(n_rows),
        'str_col': np.random.choice(['foo', 'bar', 'baz'], size=n_rows),
        'datetime_col': pd.date_range('2020-01-01', periods=n_rows, freq='S'),
        'bool_col': np.random.choice([True, False], size=n_rows)
    })
    return df

def save_csv(df, filename='data.csv'):
    df.to_csv(filename, index=False)

def load_csv(filename='data.csv'):
    return pd.read_csv(filename)

def save_pickle(df, filename='data.pkl'):
    df.to_pickle(filename)

def load_pickle(filename='data.pkl'):
    return pd.read_pickle(filename)

def save_parquet(df, filename='data.parquet'):
    df.to_parquet(filename, index=False)

def load_parquet(filename='data.parquet'):
    return pd.read_parquet(filename)

def save_feather(df, filename='data.feather'):
    df.to_feather(filename)

def load_feather(filename='data.feather'):
    return pd.read_feather(filename)

def save_hdf(df, filename='data.h5', key='df'):
    df.to_hdf(filename, key=key, mode='w')

def load_hdf(filename='data.h5', key='df'):
    return pd.read_hdf(filename, key=key)

def save_json(df, filename='data.json'):
    df.to_json(filename, orient='records', lines=True)

def load_json(filename='data.json'):
    return pd.read_json(filename, orient='records', lines=True)

def benchmark_formats(df, formats):
    """Benchmarks different file formats for saving and loading DataFrames."""
    results = []
    for fmt_name, save_func, load_func, filename in formats:
        print(f"Benchmarking format: {fmt_name}")
        try:
            # Garbage collection
            gc.collect()
            # Measure save time
            start_time = time.perf_counter()
            save_func(df, filename=filename)
            save_time = time.perf_counter() - start_time

            # Get file size
            file_size = os.path.getsize(filename)

            # Garbage collection
            gc.collect()
            # Measure load time
            start_time = time.perf_counter()
            df_loaded = load_func(filename=filename)
            load_time = time.perf_counter() - start_time

            # Check that the loaded DataFrame matches the original
            if df.shape != df_loaded.shape:
                print(f"Warning: Loaded DataFrame shape {df_loaded.shape} does not match original {df.shape} for format {fmt_name}")

            results.append({
                'Format': fmt_name,
                'Save Time (s)': save_time,
                'Load Time (s)': load_time,
                'File Size (MB)': file_size / (1024 * 1024),
            })

            # Remove the file to save disk space
            os.remove(filename)

        except Exception as e:
            print(f"Error processing format {fmt_name}: {e}")
            results.append({
                'Format': fmt_name,
                'Save Time (s)': None,
                'Load Time (s)': None,
                'File Size (MB)': None,
            })
            continue
    return results

if __name__ == '__main__':
    # Set seed for reproducibility
    np.random.seed(0)

    df = create_sample_dataframe()

    formats = [
        ('CSV', save_csv, load_csv, 'data.csv'),
        ('Pickle', save_pickle, load_pickle, 'data.pkl'),
        ('Parquet', save_parquet, load_parquet, 'data.parquet'),
        ('Feather', save_feather, load_feather, 'data.feather'),
        ('HDF5', save_hdf, load_hdf, 'data.h5'),
        ('JSON', save_json, load_json, 'data.json'),
    ]

    results = benchmark_formats(df, formats)

    results_df = pd.DataFrame(results)
    print(results_df)

# Benchmarking format: CSV
# Benchmarking format: Pickle
# Benchmarking format: Parquet
# Benchmarking format: Feather
# Benchmarking format: HDF5
# Benchmarking format: JSON
#
#     Format  Save Time (s)  Load Time (s)  File Size (MB)
# 0      CSV       4.215721       0.816499       49.275522
# 1   Pickle       0.281436       0.131746       29.567863 # Fastest save time
# 2  Parquet       2.236073       2.587238       15.308903 # Most space efficient
# 3  Feather       0.427942       0.039350       21.579912 # Fastest load time
# 4     HDF5       4.521895       0.191879       38.210930
# 5     JSON       1.671533       2.620253       96.597058