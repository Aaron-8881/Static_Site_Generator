import os
import shutil
from markdown_converter import markdown_to_html_node
from markdown_extract import extract_title

def copy_directory(source_dir, dest_dir):
    """Recursively copy all contents from source_dir to dest_dir."""
    if os.path.exists(dest_dir):
        print(f"Removing existing destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    os.mkdir(dest_dir)
    print(f"Created directory: {dest_dir}")
    
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")
        else:
            copy_directory(source_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    """Generate an HTML page from markdown using a template."""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_content = template_content.replace("{{ Title }}", title)
    final_content = final_content.replace("{{ Content }}", html_content)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final HTML to destination
    with open(dest_path, 'w') as f:
        f.write(final_content)
    print(f"Generated HTML file: {dest_path}")

def generate_pages_recursive(content_dir, template_path, public_dir):
    """Recursively generate HTML pages from markdown files."""
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                # Construct paths
                from_path = os.path.join(root, file)
                # Calculate relative path and convert to public path
                rel_path = os.path.relpath(from_path, content_dir)
                dest_path = os.path.join(public_dir, rel_path[:-3] + ".html")
                
                generate_page(from_path, template_path, dest_path)

def main():
    # Define directories and files
    static_dir = "static"
    public_dir = "public"
    content_dir = "content"
    template_path = "template.html"
    
    # Copy static files
    if os.path.exists(static_dir):
        copy_directory(static_dir, public_dir)
    else:
        print(f"Static directory '{static_dir}' does not exist")
    
    # Generate pages recursively
    if os.path.exists(content_dir) and os.path.exists(template_path):
        generate_pages_recursive(content_dir, template_path, public_dir)
    else:
        print(f"Missing content directory '{content_dir}' or template file '{template_path}'")

if __name__ == "__main__":
    main()