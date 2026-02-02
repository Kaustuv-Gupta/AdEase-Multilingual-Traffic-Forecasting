import pandas as pd
import zipfile
from pathlib import Path
import os
import glob

def merge_zipped_data(input_dir: str = './data', output_file: str = 'train.csv', pattern: str = '*_part_*.zip', base_name: str = None) -> None:
    """
    Extract CSV files from zip archives, merge them, and save as a single file.
    
    Args:
        input_dir: Directory containing zip files
        output_file: Name of output merged CSV file
        pattern: Glob pattern to match zip files (default: *_part_*.zip)
        base_name: Base name filter (e.g., 'train_1' to match 'train_1_part_*.zip')
    """
    # Create input directory reference
    input_path = Path(input_dir)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    # Determine search pattern
    if base_name:
        search_pattern = os.path.join(input_dir, f'{base_name}_part_*.zip')
    else:
        search_pattern = os.path.join(input_dir, pattern)
    
    # Find all matching zip files
    zip_files = sorted(glob.glob(search_pattern))
    
    if not zip_files:
        print(f"⚠ No zip files found matching pattern: {search_pattern}")
        return
    
    print(f"Found {len(zip_files)} zip files to merge")
    
    merged_df = None
    
    # Extract and merge CSVs from each zip file
    for idx, zip_file in enumerate(zip_files):
        print(f"Processing [{idx + 1}/{len(zip_files)}]: {os.path.basename(zip_file)}")
        
        try:
            with zipfile.ZipFile(zip_file, 'r') as zipf:
                # Get the CSV file name inside the zip
                csv_files = [f for f in zipf.namelist() if f.endswith('.csv')]
                
                if not csv_files:
                    print(f"  ⚠ No CSV file found in {os.path.basename(zip_file)}")
                    continue
                
                # Read the first CSV found in the zip
                csv_name = csv_files[0]
                with zipf.open(csv_name) as csv_file:
                    df = pd.read_csv(csv_file)
                    
                    # Merge with existing dataframe
                    if merged_df is None:
                        merged_df = df
                    else:
                        # Append rows, ignoring index
                        merged_df = pd.concat([merged_df, df], ignore_index=True)
                    
                    print(f"  ✓ Extracted {csv_name} ({len(df)} rows)")
        
        except Exception as e:
            print(f"  ✗ Error processing {os.path.basename(zip_file)}: {str(e)}")
            continue
    
    # Save merged dataframe
    if merged_df is not None:
        output_path = os.path.join(input_dir, output_file)
        merged_df.to_csv(output_path, index=False)
        
        print(f"\n✓ Merge complete!")
        print(f"✓ Total rows: {len(merged_df)}")
        print(f"✓ Total columns: {len(merged_df.columns)}")
        print(f"✓ Output file: {output_path}")
    else:
        print("✗ No data to merge")


def merge_zipped_data_with_cleanup(input_dir: str = './data', output_file: str = 'merged_data.csv', 
                                   pattern: str = '*_part_*.zip', base_name: str = None, 
                                   cleanup: bool = False) -> None:
    """
    Extract, merge CSV files from zips, and optionally clean up intermediate files.
    
    Args:
        input_dir: Directory containing zip files
        output_file: Name of output merged CSV file
        pattern: Glob pattern to match zip files
        base_name: Base name filter
        cleanup: If True, removes original zip and CSV files after merging
    """
    # First merge
    merge_zipped_data(input_dir, output_file, pattern, base_name)
    
    # Cleanup if requested
    if cleanup:
        print("\nCleaning up intermediate files...")
        
        if base_name:
            search_pattern = os.path.join(input_dir, f'{base_name}_part_*.*')
        else:
            search_pattern = os.path.join(input_dir, pattern.replace('.zip', '.*'))
        
        files_to_remove = glob.glob(search_pattern)
        
        for file_path in files_to_remove:
            try:
                os.remove(file_path)
                print(f"  ✓ Removed {os.path.basename(file_path)}")
            except Exception as e:
                print(f"  ✗ Could not remove {os.path.basename(file_path)}: {str(e)}")


if __name__ == '__main__':
    merge_zipped_data(input_dir='./data', output_file='train.csv', base_name='train_1')
