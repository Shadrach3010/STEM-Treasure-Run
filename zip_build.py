import os
import zipfile

def create_zip():
    build_dir = os.path.join("build", "web")
    zip_path = "web_build.zip"
    
    if not os.path.isdir(build_dir):
        print(f"Error: {build_dir} directory does not exist! Please build the game first.")
        return
        
    print(f"Compressing contents of {build_dir} into {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Keep index.html at the root of the zip
                arcname = os.path.relpath(file_path, build_dir)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")
    print(f"\nSuccess! '{zip_path}' has been created in your project folder.")
    print("You can upload this zip directly to Itch.io!")

if __name__ == "__main__":
    create_zip()
