def handler(job):
    print("Image Worker Start")
    
    job_input = job["input"]

    if not job_input.get("image", False):
        return {
            "error": "Input is missing the 'image' key. Please include an image."
        }

    # Placeholder for image processing logic
    print("Processing image...")
    
    return {
        "message": "Image processed successfully",
        "status": "completed"
    }
