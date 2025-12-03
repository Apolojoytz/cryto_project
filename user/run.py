# user/run.py
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import main_user
    import main_user
    
    # Check if main_user has main() function
    if hasattr(main_user, 'main'):
        main_user.main()
    else:
        # If no main() function, try to find and call the entry point
        print("Running user portal...")
        # Look for the function that starts everything
        # This depends on your code structure
        # For example, if you have a function called start():
        if hasattr(main_user, 'start'):
            main_user.start()
        elif hasattr(main_user, 'run'):
            main_user.run()
        else:
            print("❌ Could not find entry point in main_user.py")
            print("   Please add a main() function to main_user.py")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")