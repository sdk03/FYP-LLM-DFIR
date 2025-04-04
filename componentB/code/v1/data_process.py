import pickle
import pandas as pd
# pd.set_option('display.max_columns', None) 
pd.set_option('display.max_rows', None) 


file_path = '../Messages_20250129123541.csv'

# Load CSV Messages from the exported file
df = pd.read_csv(file_path)

print("\n\n[DEBUG]: RAW DATAFRAME\n")
print ("[DEBUG]: \n\n",df.head()) #DEBUG THE DATAFRAME LOAD  

# -------------------------------------------------------------

# Function to handle timezone conversion
def convert_to_gmt(datetime_str):
    if "BST" in datetime_str:
        # Remove 'BST', convert to datetime, and adjust by subtracting 1 hour (DST)
        datetime = pd.to_datetime(datetime_str.replace("BST", "").strip()) - pd.Timedelta(hours=1)
    elif "GMT" in datetime_str:
        # Convert directly if it's GMT
        datetime = pd.to_datetime(datetime_str.replace("GMT", "").strip())
    else:
        # If no timezone info, attempt regular parsing
        datetime = pd.to_datetime(datetime_str)
    return datetime

# Apply the conversion function to the "Date/Time" column
df["Date/Time"] = df["Date/Time"].apply(convert_to_gmt)

df = df.sort_values("Date/Time").reset_index(drop=True)
print("\n\n[DEBUG]: DATE TIME CONVERTED\n")
print ("[DEBUG]: \n\n",df["Date/Time"]) #DEBUG the converted datetime

# ------------------------------------------------------------------

# # Define the sliding window parameters
# window_size = "60m"
# slide_step = "0m"

# # Generate overlapping time ranges
# start_time = df["Date/Time"].min()
# end_time = df["Date/Time"].max()
# windows = []
# current_time = start_time
# while current_time <= end_time:
#     window_end = current_time + pd.Timedelta(window_size)
#     windows.append((current_time, window_end))
#     current_time += pd.Timedelta(slide_step)

# Define the window size
window_size = pd.Timedelta("1440m")  # Ensures it’s recognized as timedelta

# Generate non-overlapping time ranges aligned to the hour
start_time = df["Date/Time"].min().floor('H')  # Align to nearest hour
end_time = df["Date/Time"].max()
windows = []
current_time = start_time

while current_time <= end_time:
    window_end = current_time + window_size
    mask = (df["Date/Time"] >= current_time) & (df["Date/Time"] < window_end)
    window_data = df[mask]
    if not window_data.empty:
        windows.append((current_time, window_end))
    current_time = window_end  # Move to next window

print("\n\n[DEBUG]: WINDOW TIMES\n")
for window in windows:
    print("[DEBUG]:", window)
print(f"\n\n[DEBUG]: WINDOWS LEN {len(windows)}")

# --------------------------------------------------------------
# Apply consistent mask with window_end exclusive
clustered_data = []
for window_start, window_end in windows:
    mask = (df["Date/Time"] >= window_start) & (df["Date/Time"] < window_end)
    cluster = df.loc[mask]
    if not cluster.empty:
        clustered_data.append({
            "window_start": window_start,
            "window_end": window_end,
            "messages": cluster.to_dict("records")
        })

print("\n\n[DEBUG]: MESSAGE CLUSTERS\n")
for cluster in clustered_data[:1]:
    print("[DEBUG]:", cluster['messages'],"\n")

# --------------------------------------------------------------------

clean_file_name = '../cleaned_data.pkl'
with open(clean_file_name, 'wb') as file:
    pickle.dump(clustered_data, file)