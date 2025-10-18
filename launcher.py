import sys
import os

# Add the site-packages to path
site_packages = r'C:\Users\Saptarshi Ghosh\AppData\Local\Programs\Python\Python312\Lib\site-packages'
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

# Now try to import and run the bot
try:
    import telegram_bot
    print("Bot started successfully!")
except Exception as e:
    print("Error:", e)
