# main.py - SIMPLE VERSION
import os
import subprocess
import sys
import time

def display_banner():
    print("\n" + "="*60)
    print("         ONLINE VOTING SYSTEM")
    print("="*60)
    print("   🔐 Secure • Transparent • Digital Voting")
    print("="*60)

def main():
    display_banner()
    
    while True:
        print("\n" + "="*40)
        print("MAIN PORTAL SELECTION")
        print("="*40)
        print("1. 👤 USER PORTAL")
        print("2. 🔐 ADMIN PORTAL")
        print("3. ❌ EXIT")
        print("="*40)

        choice = input("\nSelect portal (1-3): ").strip()
        
        if choice == "1":
            print("\n➡️  Redirecting to USER PORTAL...")
            time.sleep(1)
            
            # Check for run.py first, then main_user.py
            if os.path.exists("user/run.py"):
                os.system(f'"{sys.executable}" user/run.py')
            elif os.path.exists("user/main_user.py"):
                os.system(f'"{sys.executable}" user/main_user.py')
            else:
                print("❌ User portal files not found!")
                
        elif choice == "2":
            print("\n➡️  Redirecting to ADMIN PORTAL...")
            time.sleep(1)
            
            # Check for run.py first, then main_admin.py
            if os.path.exists("admin/run.py"):
                os.system(f'"{sys.executable}" admin/run.py')
            elif os.path.exists("admin/main_admin.py"):
                os.system(f'"{sys.executable}" admin/main_admin.py')
            else:
                print("❌ Admin portal files not found!")
                
        elif choice == "3":
            print("\n" + "="*60)
            print("Thank you for using the Online Voting System!")
            print("Goodbye! 👋")
            print("="*60)
            break
            
        else:
            print("❌ Invalid choice! Please select 1-3.")

if __name__ == "__main__":
    main()