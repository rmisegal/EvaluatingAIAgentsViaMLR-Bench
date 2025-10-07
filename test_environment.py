"""Test environment setup and dependencies."""

import sys
import os
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("=" * 60)
    print("Checking Python Version")
    print("=" * 60)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Python version: {version_str}")
    
    if version.major == 3 and version.minor >= 11:
        print("✅ PASS: Python 3.11+ detected")
        return True
    else:
        print(f"⚠️  WARNING: Python 3.11+ recommended, found {version_str}")
        return True  # Still pass but warn


def check_nodejs():
    """Check Node.js installation."""
    print("=" * 60)
    print("Checking Node.js")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"Node.js version: {version}")
            print("✅ PASS: Node.js installed")
            return True
        else:
            print("❌ FAIL: Node.js not working")
            return False
            
    except FileNotFoundError:
        print("⚠️  WARNING: Node.js not found (optional)")
        return True  # Optional, so pass with warning
    except Exception as e:
        print(f"⚠️  WARNING: Could not check Node.js: {e}")
        return True


def check_python_packages():
    """Check required Python packages."""
    print("=" * 60)
    print("Checking Python Packages")
    print("=" * 60)
    
    required_packages = {
        "google.adk": "Google ADK",
        "pydantic": "Pydantic",
        "loguru": "Loguru",
        "flask": "Flask",
        "flask_socketio": "Flask-SocketIO",
        "aiohttp": "aiohttp",
        "pytest": "pytest"
    }
    
    all_found = True
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name}: Installed")
        except ImportError:
            print(f"❌ {name}: NOT INSTALLED")
            all_found = False
    
    if all_found:
        print()
        print("✅ PASS: All required packages installed")
        return True
    else:
        print()
        print("❌ FAIL: Some packages missing")
        return False


def check_api_keys():
    """Check API keys in environment."""
    print("=" * 60)
    print("Checking API Keys")
    print("=" * 60)
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("⚠️  WARNING: .env file not found")
        print("   Copy .env.example to .env and add your keys")
    
    # Check GOOGLE_API_KEY
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key:
        masked = google_key[:8] + "..." + google_key[-4:] if len(google_key) > 12 else "***"
        print(f"✅ GOOGLE_API_KEY: Found ({masked})")
        has_google = True
    else:
        print("❌ GOOGLE_API_KEY: NOT SET")
        print("   Get your key from: https://aistudio.google.com/")
        has_google = False
    
    # Optional keys
    brave_key = os.getenv("BRAVE_API_KEY")
    if brave_key:
        print(f"✅ BRAVE_API_KEY: Found (optional)")
    else:
        print("ℹ️  BRAVE_API_KEY: Not set (optional)")
    
    print()
    if has_google:
        print("✅ PASS: Required API keys present")
        return True
    else:
        print("❌ FAIL: GOOGLE_API_KEY required")
        return False


def check_flask_socketio():
    """Check Flask and SocketIO setup."""
    print("=" * 60)
    print("Checking Flask + SocketIO")
    print("=" * 60)
    
    try:
        from flask import Flask
        from flask_socketio import SocketIO
        
        # Try to create a test app
        app = Flask(__name__)
        socketio = SocketIO(app)
        
        print("✅ Flask: Working")
        print("✅ SocketIO: Working")
        print("✅ PASS: Flask + SocketIO ready")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def check_project_structure():
    """Check project structure."""
    print("=" * 60)
    print("Checking Project Structure")
    print("=" * 60)
    
    required_dirs = [
        "mlr_bench",
        "mlr_bench/agent",
        "mlr_bench/judge",
        "mlr_bench/models",
        "mlr_bench/mcp",
        "mlr_bench/ui",
        "data/tasks",
        "tests"
    ]
    
    all_exist = True
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - MISSING")
            all_exist = False
    
    print()
    if all_exist:
        print("✅ PASS: Project structure correct")
        return True
    else:
        print("❌ FAIL: Some directories missing")
        return False


def check_data_files():
    """Check data files."""
    print("=" * 60)
    print("Checking Data Files")
    print("=" * 60)
    
    tasks_file = Path("data/tasks/tasks.json")
    
    if tasks_file.exists():
        import json
        with open(tasks_file) as f:
            tasks = json.load(f)
        
        print(f"✅ tasks.json: Found ({len(tasks)} tasks)")
        print("✅ PASS: Data files present")
        return True
    else:
        print("❌ tasks.json: NOT FOUND")
        print("❌ FAIL: Data files missing")
        return False


def main():
    """Run all environment checks."""
    print()
    print("🔍 MLR-Bench Environment Check")
    print()
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Node.js", check_nodejs()))
    results.append(("Python Packages", check_python_packages()))
    results.append(("Flask + SocketIO", check_flask_socketio()))
    results.append(("API Keys", check_api_keys()))
    results.append(("Project Structure", check_project_structure()))
    results.append(("Data Files", check_data_files()))
    
    # Summary
    print()
    print("=" * 60)
    print("Environment Check Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print()
    print(f"Total: {passed}/{total} checks passed")
    
    if passed == total:
        print()
        print("🎉 Environment is ready!")
        print()
        print("Next steps:")
        print("1. Start UI server: python -m mlr_bench.cli.ui_server")
        print("2. Run MLR-Bench: mlr-bench --task-id iclr2025_bi_align")
        print("3. Open browser: http://localhost:5000")
    else:
        print()
        print("⚠️  Please fix the failed checks above")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
