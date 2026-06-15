import os
import uuid
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException, status
from PIL import Image

from ..config import settings


def ensure_upload_dir():
    upload_path = Path(settings.UPLOAD_DIR)
    specimens_path = upload_path / "specimens"
    avatars_path = upload_path / "avatars"
    specimens_path.mkdir(parents=True, exist_ok=True)
    avatars_path.mkdir(parents=True, exist_ok=True)
    return upload_path, specimens_path, avatars_path


def generate_filename(original_name: str) -> str:
    ext = os.path.splitext(original_name)[1].lower()
    return f"{uuid.uuid4().hex}{ext}"


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower().lstrip(".")


def validate_image_file(file: UploadFile) -> Tuple[bool, Optional[str]]:
    if not file.filename:
        return False, "No filename provided"

    ext = get_file_extension(file.filename)
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        return False, f"Unsupported file type: {ext}. Allowed types: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"

    return True, None


async def save_upload_file(
    file: UploadFile,
    subdirectory: str = "specimens",
    validate_image: bool = True
) -> Tuple[Optional[str], Optional[str], Optional[int], Optional[str]]:
    upload_path, _, _ = ensure_upload_dir()
    target_dir = upload_path / subdirectory
    target_dir.mkdir(parents=True, exist_ok=True)

    if validate_image:
        is_valid, error = validate_image_file(file)
        if not is_valid:
            return None, None, None, error

    original_name = file.filename or "unknown"
    file_name = generate_filename(original_name)
    file_path = target_dir / file_name

    file_size = 0
    try:
        contents = await file.read()
        file_size = len(contents)

        if file_size > settings.MAX_UPLOAD_SIZE:
            return None, None, None, f"File too large. Max size: {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB"

        with open(file_path, "wb") as f:
            f.write(contents)

        if validate_image:
            try:
                with Image.open(file_path) as img:
                    img.verify()
            except Exception:
                file_path.unlink(missing_ok=True)
                return None, None, None, "Invalid image file"

        relative_path = f"/{settings.UPLOAD_DIR}/{subdirectory}/{file_name}"
        return relative_path, file_name, file_size, None

    except Exception as e:
        file_path.unlink(missing_ok=True)
        return None, None, None, f"Upload failed: {str(e)}"
