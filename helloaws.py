from fastapi import FastAPI, UploadFile, File
import boto3
import uuid

BUCKET_NAME = "jarvis-demo-images"

s3_client = boto3.client("s3")

app = FastAPI(title="jarvis-demo")


@app.get("/")
def hello_aws() -> dict[str, str]:
    return {"message": "Hello AWS Techies"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1]

    object_key = f"images/{uuid.uuid4()}.{extension}"

    s3_client.upload_fileobj(
        file.file,
        BUCKET_NAME,
        object_key,
        ExtraArgs={
            "ContentType": file.content_type
        }
    )

    return {
        "message": "Image uploaded successfully",
        "key": object_key
    }