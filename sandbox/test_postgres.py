#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script ทดสอบ PostgreSQL CRUD operations
"""
import asyncio
import sys
import os
from pathlib import Path

# เพิ่ม path ของ backend
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import engine, async_session, Base
from models.student import Student


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
    
    async with async_session() as session:
        session.add_all(students_data)
        await session.commit()
        
        # แสดงข้อมูลที่เพิ่ม
        print(f" Inserted {len(students_data)} students:")
        for student in students_data:
            print(f"   - {student}")


async def read_data():
    """อ่านข้อมูลทั้งหมด"""
    print("=" * 60)
    print("Reading all data...")
    
    async with async_session() as session:
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
    
    async with async_session() as session:
        # Update age ของ John Doe เป็น 25
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
    
    async with async_session() as session:
        # Delete Bob Johnson
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
        
        # Step 1: Create table
        await create_table()
        
        # Step 2: Insert data
        await insert_data()
        
        # Step 3: Read data
        await read_data()
        
        # Step 4: Update data
        await update_data()
        
        # Step 5: Read again to see update
        await read_data()
        
        # Step 6: Delete data
        await delete_data()
        
        # Step 7: Read again to see deletion
        await read_data()
        
        # Step 8: Delete table
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