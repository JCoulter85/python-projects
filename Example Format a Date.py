from datetime import datetime
now = datetime.now()
print(f"Current date and time: {now}")

formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"The Date and Time is currently: {formatted_date}")