import os
import shutil
from markdown_converter import markdown_to_html_node
from textnode import TextNode, TextType

def copy_directory(source_dir, dest_dir):
    """Recursively copy all contents from source_dir to dest_dir."""
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Removing existing destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create destination directory
    os.mkdir(dest_dir)
    print(f"Created directory: {dest_dir}")
    
    # Get all items in source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # Copy file
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")
        else:
            # Recursively copy directory
            copy_directory(source_path, dest_path)

def main():
    # Copy static directory to public
    static_dir = "static"
    public_dir = "public"
    
    if not os.path.exists(static_dir):
        print(f"Static directory '{static_dir}' does not exist")
        return
    
    copy_directory(static_dir, public_dir)
    print(f"Successfully copied contents from {static_dir} to {public_dir}")

if __name__ == "__main__":
    main()