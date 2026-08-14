"""
Script ทดสอบ PostgreSQL CRUD operations
"""
import asyncio
import sys
from pathlib import Path

# เพิ่ม path ของ workspace และ backend
workspace_root = Path(__file__).resolve().parents[1]
backend_path = workspace_root / "backend"
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from sqlalchemy import select, update, delete

from backend.src.db.database import engine, SessionLocal, Base
from backend.src.models.student import Student


async def create_table():
    """สร้าง table students"""
    print("=" * 60)
    print("Creating 'students' table...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Table 'students' created successfully!")


async def insert_data():
    """Insert ข้อมูลตัวอย่าง"""
    print("=" * 60)
    print(" Inserting data...")

    students_data = [
        Student(name="John Doe", age=20, major="Computer Science"),
        Student(name="Jane Smith", age=22, major="Data Science"),
        Student(name="Bob Johnson", age=21, major="Artificial Intelligence"),
    ]

    async with SessionLocal() as session:
        session.add_all(students_data)
        await session.commit()

        print(f" Inserted {len(students_data)} students:")
        for student in students_data:
            print(f"   - {student}")


async def read_data():
    """อ่านข้อมูลทั้งหมด"""
    print("=" * 60)
    print("Reading all data...")

    async with SessionLocal() as session:
        result = await session.execute(select(Student))
        students = result.scalars().all()

        print(f" Found {len(students)} students:")
        for student in students:
            print(f"   - ID {student.id}: {student.name}, Age {student.age}, Major: {student.major}")

    return students


async def update_data():
    """Update ข้อมูล"""
    print("=" * 60)
    print("Updating data...")

    async with SessionLocal() as session:
        stmt = (
            update(Student)
            .where(Student.name == "John Doe")
            .values(age=25, major="Machine Learning")
        )
        await session.execute(stmt)
        await session.commit()

        print("Updated John Doe:")
        print("   - Age: 20 → 25")
        print("   - Major: Computer Science → Machine Learning")


async def delete_data():
    """Delete ข้อมูล"""
    print("=" * 60)
    print("Deleting data...")

    async with SessionLocal() as session:
        stmt = delete(Student).where(Student.name == "Bob Johnson")
        result = await session.execute(stmt)
        await session.commit()

        print(f"Deleted {result.rowcount} student(s):")
        print("   - Bob Johnson")


async def delete_table():
    """Delete table"""
    print("=" * 60)
    print("Deleting 'students' table...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    print("Table 'students' deleted successfully!")


async def main():
    """รันทุกขั้นตอน"""
    try:
        print("\n" + "-" * 30)
        print("PostgreSQL CRUD Test with SQLAlchemy")
        print("" * 30)

        await create_table()
        await insert_data()
        await read_data()
        await update_data()
        await read_data()
        await delete_data()
        await read_data()
        await delete_table()

        print("\n" + "" * 30)
        print("All CRUD operations completed successfully!")
        print("" * 30 + "\n")

    except Exception as e:
        print(f"\nError: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())