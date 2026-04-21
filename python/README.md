# Pet Portrait Example - TheDogAPI

This repository provides a concrete example of how to use **TheDogAPI** portrait-related endpoints to create a pet profile, upload source images, perform physical analyses, and generate artistic portraits.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.x
- A valid API Key from [TheDogAPI.com](https://thedogapi.com)

### 2. Setup
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install requests python-dotenv
   ```
3. Create a `.env` file in the `python/` directory:
   ```env
   API_KEY=your_api_key_here
   API_URL=https://api.thedogapi.com/v1
   ```

### 3. Run the Example
```bash
cd python
python3 create-portraits.py
```

---

## 🛠 API Endpoints Used

The follow table summarizes the portrait-related endpoints demonstrated in this repo:

| Operation | Method | URL | Description |
| :--- | :--- | :--- | :--- |
| **Check Pet** | `GET` | `/v1/pets?sub_id={id}` | Checks if a pet already exists using its `sub_id`. |
| **Create Pet** | `POST` | `/v1/pets` | Creates a pet record and uploads multiple images in one multipart request. |
| **Add Images** | `POST` | `/v1/pets/{id}/images` | Uploads additional images to an existing pet profile. |
| **Analyze** | `POST` | `/v1/pets/{id}/{module}` | Runs physical analyses: `genealogy`, `estimated-age`, `body-condition-score`, `muscle-condition-score`. |
| **Health Tips** | `GET` | `/v1/health-tips` | Retrieves breed-specific recommendations using the breed ID from genealogy analysis. |
| **Request Portrait** | `POST` | `/v1/pets/{id}/portrait` | Triggers the generation of an artistic portrait. Supports styles like `studio`, `pencil_sketch`, `watercolour`, `oil_painting`, and `july_4th`. |

---

## 📂 Project Structure

- `create-portraits.py`: The main script that orchestrates the entire workflow.
- `output-data/`: Contains subfolders for each pet with raw JSON analysis responses.
- `output-portraits/`: Contains subfolders for each pet with generated portrait images.
- `../test-images/dogs/`: Source directory. Each subfolder here is treated as a separate pet.

## 💡 Workflow Explained

1. **Automatic Discovery**: The script scans `../test-images/dogs/` for subfolders. Each folder name is used as the `pet_name` and `sub_id`.
2. **Bulk Upload**: For each folder, it collects all valid image files and uploads them in a single `multipart/form-data` request when creating the pet profile.
3. **Organized Outputs**: Analysis results and portraits are saved in dedicated subfolders within `output-data/` and `output-portraits/`, matching the source folder name.
4. **Multi-Style Portraits**: It generates five artistic styles (`studio`, `pencil_sketch`, `watercolour`, `oil_painting`, `july_4th`) for every discovered pet.

---

## 📧 Support
If you are having issues with specific endpoints, ensure your `x-api-key` header is correctly set and that you are using the correct `PET_ID` returned from the `/pets` endpoint.
