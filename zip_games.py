import os
import zipfile
import time

def zip_games():
    """Zip the games directory into games.zip"""
    start_time = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    games_dir = os.path.join(base_dir, 'games')
    output_path = os.path.join(base_dir, 'games.zip')
    
    if not os.path.exists(games_dir):
        print(f"Error: {games_dir} does not exist.")
        return False
        
    print(f"Zipping {games_dir} to {output_path}...")
    
    # We use ZIP_DEFLATED for compression, but ZIP_STORED would be faster 
    # if we don't care about space. Given Vercel limits, compression is better.
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        count = 0
        for root, dirs, files in os.walk(games_dir):
            for file in files:
                if file.endswith('.lua'):
                    file_path = os.path.join(root, file)
                    # Use arcname to avoid storing the full path inside the zip
                    arcname = os.path.relpath(file_path, games_dir)
                    zipf.write(file_path, arcname)
                    count += 1
                    if count % 5000 == 0:
                        print(f"Zipped {count} files...")
    
    elapsed = time.time() - start_time
    print(f"Successfully zipped {count} files in {elapsed:.2f} seconds.")
    return True

if __name__ == "__main__":
    zip_games()
