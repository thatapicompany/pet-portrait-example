# Pet Portrait API Example

This repository contains an example integration with [TheDogAPI](https://thedogapi.com) portrait-related endpoints. It demonstrates how to automate the creation of pet profiles, upload images, and generate AI-powered artistic portraits.

## 🚀 Key Features

- **Automated Folder Discovery**: Automatically processes subfolders in `test-images/dogs/` as individual pets.
- **Robust Image Synchronization**: Handles both new pet creation and syncing images to existing profiles.
- **Multi-Style Portraits**: Generates portraits in various styles (`studio`, `pencil_sketch`, `watercolour`, `oil_painting`, `july_4th`).
- **Organized Outputs**: Automatically categorizes analysis data and generated portraits into pet-specific subdirectories.

## 📂 Project Structure

- `python/`: Contains the Python implementation and its own detailed documentation.
- `test-images/`: Sample images for testing the integration.
- `output-data/`: Generated JSON analysis results (genealogy, BCS, etc.).
- `output-portraits/`: Generated AI portraits.

## 🛠️ Getting Started

To explore the code and run the example, navigate to the `python/` directory:

```bash
cd python
```

Follow the instructions in [python/README.md](python/README.md) to set up your environment and run the script.

## 📖 API Documentation

The example interacts with the following endpoints:
- `POST /v1/pets`: Create a pet profile.
- `POST /v1/pets/{id}/images`: Upload images to a pet profile.
- `POST /v1/pets/{id}/portrait`: Generate an AI portrait.
- `POST /v1/pets/{id}/genealogy`: Analyze breed and genealogy.
- `POST /v1/pets/{id}/body-condition-score`: Analyze BCS.

For more details on the API, visit [TheDogAPI Documentation](https://docs.thedogapi.com).
