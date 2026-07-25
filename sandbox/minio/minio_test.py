from minio import Minio
from minio.commonconfig import Filter
from minio.versioningconfig import VersioningConfig, ENABLED
from minio.lifecycleconfig import LifecycleConfig, Rule, NoncurrentVersionExpiration

# เชื่อมต่อกับ MinIO Server
client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False        # เพราะเราไม่ได้ใช้ HTTPS ใน Local
)

BUCKET_NAME = "my-profile"

def setup_bucket():
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' created.")
    else:
        print(f"Bucket '{BUCKET_NAME}' already exists.")
    
    # เปิดใช้ Versioning
    config = VersioningConfig(ENABLED)
    client.set_bucket_versioning(BUCKET_NAME, config)
    print("Versioning enabled.")

    # ตั้งค่า Lifecycle
    lifecycle_config = LifecycleConfig(
        [
            Rule(
                status=ENABLED,
                rule_filter=Filter(prefix=""),                                                  # prefix="" หมายถึงให้กฎนี้มีผลกับ "ทุกไฟล์" ใน Bucket
                rule_id="auto-delete-old-versions",
                noncurrent_version_expiration=NoncurrentVersionExpiration(noncurrent_days=7)    # กฎข้อที่ 1: ลบไฟล์ "เวอร์ชันเก่า" (ที่ถูกเซฟทับไปแล้ว) เมื่ออายุเกิน 7 วัน
            )
        ]
    )
    client.set_bucket_lifecycle(BUCKET_NAME, lifecycle_config)
    print("Lifecycle rules applied.")

def upload(file_path, object_name):
    client.fput_object(BUCKET_NAME, object_name, file_path)
    print(f"Uploaded '{file_path}' as '{object_name}'.") 

def download(object_name, download_path, version_id=None):
    client.fget_object(BUCKET_NAME, object_name, download_path, version_id=version_id)
    print(f"Downloaded '{object_name}' (Version: {version_id}) to '{download_path}'.")

def check_versions(object_name):
    versions = client.list_objects(BUCKET_NAME, prefix=object_name, include_version=True)
    print(f"--- Versions of '{object_name}' ---")
    for version in versions:
        status = "(Latest)" if version.is_latest else ""
        print(f"Version ID: {version.version_id} {status} | Last Modified: {version.last_modified}")

if __name__ == "__main__":
    # 1. Setup และเปิด Versioning (รันครั้งแรกครั้งเดียว)
    setup_bucket()

    # 2. ทดสอบ Upload รูปที่ 1 และ 2
    # upload("sandbox/myphoto.jpg", "myphoto.jpg") 
    upload("sandbox/myphoto_v2.jpg", "myphoto.jpg") 

    # 3. ทดสอบ Download แบบไม่ระบุ Version
    # download('myphoto.jpg', 'sandbox/minio/result.jpg')

    # check_versions('myphoto.jpg')

    # 4. ทดสอบ Download แบบระบุ Version 
    # download('myphoto.jpg', 'sandbox/minio/result2.jpg', version_id='4b108abf-27ef-415f-b4e1-e41e6d94ea92')