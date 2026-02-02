import pandas as pd
import zipfile
from pathlib import Path
import os

def split_and_zip_data(csv_path: str, output_dir: str = './data', chunk_size: int = 50000, zip_file: str = 'train_parts.zip', base_name: str = None) -> None:
    """
    Split large CSV file into chunks and compress them.
    
    Args:
        csv_path: Path to the input CSV file
        output_dir: Directory to save chunks and zip file
        chunk_size: Number of rows per chunk
        zip_file: Name of output zip file
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load dataset with chunking for memory efficiency
    chunks = pd.read_csv(csv_path, chunksize=chunk_size)
    
    chunk_files = []
    
    # Determine base filename to use for produced files
    if base_name:
        base = base_name
    else:
        base = Path(csv_path).stem

    # Split, save chunks, and compress each individually
    zip_files = []
    
    for idx, chunk in enumerate(chunks):
        # Save CSV with headers using dynamic base name
        chunk_path = os.path.join(output_dir, f'{base}_part_{idx}.csv')
        chunk.to_csv(chunk_path, index=False, header=True)
        chunk_files.append(chunk_path)
        
        # Compress each CSV into individual zip file
        zip_path = os.path.join(output_dir, f'{base}_part_{idx}.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(chunk_path, arcname=os.path.basename(chunk_path))
        
        zip_files.append(zip_path)
        print(f"✓ Chunk {idx}: {os.path.basename(chunk_path)} → {os.path.basename(zip_path)}")
    print(f"✓ Total zip files created: {len(zip_files)}")


if __name__ == '__main__':
    split_and_zip_data('./data/train_1.csv')