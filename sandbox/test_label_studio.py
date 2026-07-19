import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))
 
from label_studio_sdk.client import LabelStudio
from core.config import settings


def main():
    # ============================================
    # DEBUG: ตรวจสอบค่าที่อ่านได้จาก .env
    # ============================================
    print("--- DEBUG SETTINGS ---")
    raw_key = settings.LABEL_STUDIO_API_KEY
    print(f"URL: {settings.LABEL_STUDIO_URL}")
    print(f"Raw API Key: '{raw_key}'")
    print("----------------------")

    if not raw_key or raw_key.strip() in {"", "******", "YOUR_LABEL_STUDIO_API_KEY", "your_api_key_here"}:
        print("[ERROR] LABEL_STUDIO_API_KEY is not configured or contains a placeholder value.")
        print("Please set LABEL_STUDIO_API_KEY in backend/.env before running this test.")
        return

    # If the API key was copied with a token prefix, strip it.
    api_key = raw_key.strip()
    for prefix in ("Token ", "token ", "Bearer ", "bearer "):
        if api_key.startswith(prefix):
            api_key = api_key[len(prefix):]
            print(f"[WARN] Stripped prefix '{prefix.strip()}' from LABEL_STUDIO_API_KEY.")
            break

    # ============================================
    # Create a client to connect
    # ============================================
    print("\n[INFO] Connecting to Label Studio...")
    try:
        ls = LabelStudio(
            base_url=settings.LABEL_STUDIO_URL,
            api_key=api_key
        )
        # ทดสอบเชื่อมต่อโดยการดึงรายการ project (วิธีที่ถูกต้อง)
        test_projects = ls.projects.list()
        print("[OK] Successfully connected to Label Studio.")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return

    # ============================================
    # Create the example project
    # ============================================
    print("\n[INFO] Creating example project...")
    label_config = '''
    <View>
      <Text name="text" value="$text"/>
      <Choices name="sentiment" toName="text" choice="single">
        <Choice value="Positive"/>
        <Choice value="Negative"/>
        <Choice value="Neutral"/>
      </Choices>
    </View>
    '''
    
    try:
        project = ls.projects.create(
            title='AI Ecosystem Test Project',
            label_config=label_config
        )
        print(f"[OK] Created project: '{project.title}' (ID: {project.id})")
    except Exception as e:
        print(f"[ERROR] Failed to create project: {e}")
        return

    # ============================================
    # List all projects
    # ============================================
    print("\n[INFO] Listing all projects in Label Studio:")
    projects = ls.projects.list()
    for p in projects:
        print(f"  - ID: {p.id} | Title: {p.title} | Tasks: {p.task_number}")

    # เพิ่มข้อมูลตัวอย่าง (Dummy Tasks)
    print(f"\n[INFO] Importing 3 dummy tasks into project ID {project.id}...")
    dummy_tasks = [
        {'data': {'text': 'This product is amazing, I love it!'}},
        {'data': {'text': 'Terrible experience, will never buy again.'}},
        {'data': {'text': 'It works as expected, nothing special.'}}
    ]
    ls.projects.import_tasks(id=project.id, request=dummy_tasks)
    print("[OK] Imported 3 tasks successfully.")

    # ============================================
    # Choose one project and list all tasks
    # ============================================
    print(f"\n[INFO] Listing all tasks inside project '{project.title}':")
    tasks = ls.tasks.list(project=project.id)
    for task in tasks:
        print(f"  - Task ID: {task.id} | Data: {task.data}")

    print("\n[OK] Label Studio SDK test completed.")


if __name__ == "__main__":
    main()