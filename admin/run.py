# admin/run.py
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import main_admin
    import main_admin
    
    # Check if main_admin has main() function
    if hasattr(main_admin, 'main'):
        main_admin.main()
    else:
        # If no main() function, try to find and call the entry point
        print("Running admin portal...")
        # Look for the function that starts everything
        if hasattr(main_admin, 'start'):
            main_admin.start()
        elif hasattr(main_admin, 'run'):
            main_admin.run()
        else:
            print("❌ Could not find entry point in main_admin.py")
            print("   Please add a main() function to main_admin.py")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")