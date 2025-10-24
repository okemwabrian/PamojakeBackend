#!/usr/bin/env python3
"""
Deployment script for PythonAnywhere
Run this after pulling code from GitHub
"""

import os
import subprocess
import sys

def run_command(command, description):
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Starting PythonAnywhere deployment...")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Commands to run
    commands = [
        ("python3.10 manage.py makemigrations", "Creating migrations"),
        ("python3.10 manage.py migrate", "Running migrations"),
        ("python3.10 manage.py collectstatic --noinput", "Collecting static files"),
        ("python3.10 manage.py check", "Checking for issues"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 Deployment Summary:")
    print(f"✓ {success_count}/{len(commands)} commands completed successfully")
    
    if success_count == len(commands):
        print("\n🎉 Deployment completed successfully!")
        print("📝 Next steps:")
        print("1. Go to your PythonAnywhere Web tab")
        print("2. Click 'Reload' to restart your web app")
        print("3. Test your API endpoints")
        print("\n🔗 Your API should be available at:")
        print("https://okemwabrianny.pythonanywhere.com/")
    else:
        print("\n⚠️  Some commands failed. Please check the errors above.")
        print("You may need to fix issues before reloading your web app.")

if __name__ == "__main__":
    main()