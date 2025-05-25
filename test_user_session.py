"""
Test script to verify user session initialization.
"""

from user_session import init_user_session

if __name__ == "__main__":
    user_info = init_user_session()

    print("\n🧾 User session initialized with the following files:\n")
    for k, v in user_info.items():
        print(f"{k}: {v}")