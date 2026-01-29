from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from pathlib import Path
import os

app = FastAPI()

# Directory where all sites will be stored
SITES_DIRECTORY = Path("/app/sites")
NGINX_CONFIGS_DIRECTORY = Path("/etc/nginx/sites-available")

# Ensure directories exist
SITES_DIRECTORY.mkdir(parents=True, exist_ok=True)
NGINX_CONFIGS_DIRECTORY.mkdir(parents=True, exist_ok=True)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Hosting Manager backend!"}


@app.post("/site/")
def create_new_site(name: str, site_type: str):
    """
    Create a new site.
    :param name: Name of the site.
    :param site_type: Type of the site (wordpress, php, static).
    """
    site_path = SITES_DIRECTORY / name
    if site_path.exists():
        raise HTTPException(status_code=400, detail="Site already exists")

    # Create site directory
    site_path.mkdir(parents=True)

    # Generate Nginx config
    server_name = f"{name}.localhost"
    generate_nginx_config(name, server_name, site_path, site_type)

    return {"message": f"Site '{name}' created successfully!"}


@app.delete("/site/{name}")
def delete_site(name: str):
    """
    Delete a site along with its files and Nginx config.
    :param name: Name of the site.
    """
    site_path = SITES_DIRECTORY / name
    nginx_config_path = NGINX_CONFIGS_DIRECTORY / f"{name}.conf"

    # Delete site files and Nginx config
    if site_path.exists():
        for item in site_path.iterdir():
            if item.is_file():
                item.unlink()
            else:
                os.rmdir(item)
        site_path.rmdir()
    if nginx_config_path.exists():
        nginx_config_path.unlink()

    return {"message": f"Site '{name}' deleted successfully!"}


@app.post("/site/{name}/upload/")
def upload_file(name: str, file: UploadFile = File(...)):
    """
    Upload files to a site.
    :param name: Name of the site.
    :param file: File uploaded.
    """
    site_path = SITES_DIRECTORY / name
    if not site_path.exists():
        raise HTTPException(status_code=404, detail="Site does not exist")

    destination = site_path / file.filename
    with open(destination, "wb") as f:
        f.write(file.file.read())

    return {"message": f"File '{file.filename}' uploaded to site '{name}'."}


def generate_nginx_config(name: str, server_name: str, site_path: Path, site_type: str):
    """
    Generate an Nginx server block configuration for the site.
    """
    config_template = f"""
server {{
    listen 80;
    server_name {server_name};

    root {site_path};
    index index.html index.php;

    location / {{
        try_files $uri $uri/ =404;
    }}

    location ~ \\.php$ {{
        include fastcgi_params;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }}
}}
"""
    config_path = NGINX_CONFIGS_DIRECTORY / f"{name}.conf"
    with open(config_path, "w") as f:
        f.write(config_template)