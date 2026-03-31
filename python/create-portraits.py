import os
import requests
import json
import time
from dotenv import load_dotenv
from pathlib import Path

# --- Configuration & Setup ---

def load_environment():
    """
    Load API credentials from .env file and validate them.
    Returns (api_url, api_key).
    """
    # Look for .env in the current directory
    load_dotenv(dotenv_path=Path("./.env"))
    
    api_url = os.getenv("API_URL", "https://api.thedogapi.com/v1").rstrip('/')
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("CRITICAL: API_KEY is missing. Please ensure it's set in your .env file.")
        exit(1)
        
    return api_url, api_key

# Global configuration
API_URL, API_KEY = load_environment()
HEADERS = {"x-api-key": API_KEY}

# Constants for local file paths
BASE_IMAGE_DIR = Path("../test-images/dogs")
OUTPUT_DATA_DIR = Path("output-data")
OUTPUT_PORTRAITS_DIR = Path("output-portraits")

# The list of artistic styles to generate for each pet
PORTRAIT_STYLES = ["studio", "pencil_sketch", "watercolour", "oil_painting","july_4th"]

# Ensure root output directories exist
OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PORTRAITS_DIR.mkdir(parents=True, exist_ok=True)

# --- API Helper Functions ---

def get_existing_pet(sub_id):
    """
    Check if a pet with a specific 'sub_id' already exists in the system.
    Returns the full pet data JSON if found, otherwise None.
    """
    try:
        response = requests.get(f"{API_URL}/pets?sub_id={sub_id}", headers=HEADERS)
        if response.status_code == 200:
            pets = response.json()
            if isinstance(pets, list) and pets:
                return pets[0]
    except Exception as e:
        print(f"Error checking for existing pet: {e}")
    return None

def create_pet_and_upload_images(folder_path):
    """
    Ensures a pet exists and has images uploaded.
    If the pet exists but lacks images, it uploads all images found in folder_path.
    """
    pet_name = folder_path.name
    print(f"\n--- Processing Pet Folder: {pet_name} ---")

    # Step 1: Check if pet already exists and if it has images
    pet_data = get_existing_pet(pet_name)
    pet_id = pet_data.get("id") if pet_data else None
    
    if pet_data:
        images = pet_data.get("images", [])
        if images:
            print(f"Pet '{pet_name}' found! ID: {pet_id} with {len(images)} existing image(s).")
            return pet_id
        else:
            print(f"Pet '{pet_name}' exists (ID: {pet_id}) but has NO images. Proceeding to upload.")

    # Step 2: Prepare image files for the multipart request
    files_to_upload = []
    # Supported image extensions
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    
    for img_file in folder_path.iterdir():
        if img_file.is_file() and img_file.suffix.lower() in valid_extensions:
            # We use 'images' as the field name (multiple files allowed by the API)
            files_to_upload.append(
                ('images', (img_file.name, open(img_file, 'rb'), 'image/png'))
            )

    if not files_to_upload:
        print(f"No valid images found in {folder_path}. Skipping.")
        return pet_id

    # Step 3: Handle Creation or Upload to Existing Pet
    try:
        if not pet_id:
            # Create NEW pet with images in one go
            data = {
                'name': pet_name.replace('-', ' ').capitalize(),
                'sub_id': pet_name,
                'species_id': '1'  # 1 = Dog
            }
            print(f"Creating NEW pet '{pet_name}' with {len(files_to_upload)} image(s)...")
            response = requests.post(f"{API_URL}/pets", headers=HEADERS, data=data, files=files_to_upload)
            if response.status_code in (200, 201):
                pet_id = response.json().get("id")
                print(f"Successfully created pet! ID: {pet_id}")
            else:
                print(f"Failed to create pet ({response.status_code}): {response.text}")
        else:
            # Upload images to EXISTING pet using the pet-specific images endpoint
            # As confirmed in PetsController, this uses 'POST /v1/pets/:id/images' and the 'images' field
            print(f"Uploading {len(files_to_upload)} image(s) to existing pet {pet_id}...")
            response = requests.post(
                f"{API_URL}/pets/{pet_id}/images", 
                headers=HEADERS, 
                files=files_to_upload
            )
            if response.status_code in (200, 201):
                print(f"Successfully uploaded {len(files_to_upload)} image(s) to pet {pet_id}")
            else:
                print(f"Failed to upload images ({response.status_code}): {response.text}")
        
        return pet_id

    except Exception as e:
        print(f"Exception during pet/image processing: {e}")
    finally:
        # ALWAYS close file handles
        for _, (_, handle, _) in files_to_upload:
            handle.close()
    
    return None

def run_pet_analysis(pet_id, pet_name, endpoint, output_dir):
    """
    Executes a specific analysis module for a pet and saves the JSON result.
    """
    print(f"Triggering analysis: /{endpoint}...")
    try:
        start_time = time.time()
        response = requests.post(f"{API_URL}/pets/{pet_id}/{endpoint}", headers=HEADERS)
        elapsed = time.time() - start_time
        
        if response.status_code in (200, 201):
            data = response.json()
            output_file = output_dir / f"{pet_name}_{endpoint}.json"
            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✓ {endpoint} Success ({elapsed:.1f}s). File: {output_file}")
        else:
            print(f"✗ {endpoint} failed with code {response.status_code}")
    except Exception as e:
        print(f"Exception during {endpoint}: {e}")

def generate_portrait(pet_id, pet_name, output_dir, style="studio"):
    """
    Requests an artistic portrait generation for the pet and saves to the subfolder.
    """
    print(f"Requesting '{style}' portrait...")
    try:
        # Request generation
        response = requests.post(
            f"{API_URL}/pets/{pet_id}/portrait", 
            headers=HEADERS, 
            json={"style": style}
        )
        
        if response.status_code not in (200, 201):
            print(f"✗ Portrait request failed ({response.status_code}): {response.text}")
            return

        portrait_data = response.json()
        image_url = portrait_data.get("url")
        
        if not image_url:
            print("✗ API response missing image URL.")
            return

        # Download the generated image
        print(f"Downloading {style} portrait for {pet_name}...")
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            file_path = output_dir / f"{pet_name}_{style}.png"
            with open(file_path, "wb") as f:
                f.write(img_response.content)
            print(f"✓ Portrait saved successfully to {file_path}")
        else:
            print(f"✗ Failed to download portrait image: {img_response.status_code}")
            
    except Exception as e:
        print(f"Exception during portrait workflow: {e}")

# --- Main entry point ---

def main():
    print(f"API Target: {API_URL}")
    
    # Supported Analysis Modules
    analysis_modules = ["genealogy", "body-condition-score", "estimated-age", "muscle-condition-score"]

    # Iterate through each folder in the dogs directory
    for pet_folder in [d for d in BASE_IMAGE_DIR.iterdir() if d.is_dir()]:
        pet_name = pet_folder.name
        
        # 1. Register Pet & Upload Source Images from folder
        pet_id = create_pet_and_upload_images(pet_folder)
        
        if pet_id:
            # Initialize pet-specific output subfolders
            pet_data_dir = OUTPUT_DATA_DIR / pet_name
            pet_portrait_dir = OUTPUT_PORTRAITS_DIR / pet_name
            pet_data_dir.mkdir(parents=True, exist_ok=True)
            pet_portrait_dir.mkdir(parents=True, exist_ok=True)

            # 2. Perform various health/physical analyses
            for module in analysis_modules:
                run_pet_analysis(pet_id, pet_name, module, pet_data_dir)
            
            # 3. Generate Artistic Portraits for all requested styles
            for style in PORTRAIT_STYLES:
                generate_portrait(pet_id, pet_name, pet_portrait_dir, style=style)

if __name__ == "__main__":
    main()
