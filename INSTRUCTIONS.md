# TypeBot - How to Change Firefox Profile Path

This document provides instructions on how to configure the Firefox profile path for the TypeBot.

## Configuration

1.  **Firefox Profile:**
    *   The bot uses your Firefox profile to run. You need to provide the path to your profile.
    *   To find your profile path, navigate to `about:profiles` in your Firefox address bar.
    *   You will see a list of profiles. Find the one you want to use (usually the one in use) and copy the "Root Directory" path.

2.  **Create or Update `.env` file:**
    *   Create a file named `.env` in the same directory as `main.py` if it doesn't already exist.
    *   Add or update the following line in the `.env` file, replacing `"your_firefox_profile_path"` with the path you copied in the previous step:
        ```
        PROFILE_PATH="your_firefox_profile_path"
        ```
        **Example:**
        ```
        PROFILE_PATH="C:\Users\YourUser\AppData\Roaming\Mozilla\Firefox\Profiles\abcdef12.default-release"
        ```
