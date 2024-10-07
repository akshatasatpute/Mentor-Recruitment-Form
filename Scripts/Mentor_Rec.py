#import necessary libraries
import streamlit as st
import pandas as pd
import pyperclip  # Import the pyperclip module for clipboard operations
import os
import requests

from supabase_py import create_client,Client
# Read the category dataset and extract unique categories

from io import StringIO  # Import StringIO directly from the io module
from io import BytesIO


# Set initial scale for very small screens
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=0.5">', unsafe_allow_html=True)


# Display the PNG image in the top left corner of the Streamlit sidebar with custom dimensions
image_path = 'https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/VS-logo.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svVlMtbG9nby5wbmciLCJpYXQiOjE3MjE5NzA3ODUsImV4cCI6MTc1MzUwNjc4NX0.purLZOGk272W80A4OlvnavqVB9u-yExhzpmI3dZrjdM&t=2024-07-26T05%3A13%3A02.704Z'
st.sidebar.image(image_path, width=150)

logo_path = 'https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/Logo__.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svTG9nb19fLmpwZyIsImlhdCI6MTcyMTk3MDgxMCwiZXhwIjoxNzUzNTA2ODEwfQ.iG-36L48IvAEvB8X6uI3pNBZk1StNykH1PEbijCA368&t=2024-07-26T05%3A13%3A28.196Z'
st.sidebar.image(logo_path, width=90)

# Update the user name list with Shalini, Titli, and Deepika
#user_names = ['Shalini', 'Titli', 'Deepika']
# Predefined dictionary of user names and access codes known only to administrators
user_access_codes = {
    "Salini": "1122",
    "Titly": "4455",
    "Dipika": "3399",
    # Add more user names and access codes as needed
}

# Prompt the user to enter their access code
entered_code = st.sidebar.text_input("Enter Your Access Code:", type="password")
# Check if either of the boxes is not selected
if not entered_code:
    st.error("Please fill in all the compulsory fields marked with * before proceeding.")
    st.stop()

# Filter the user names based on the entered access code
filtered_user_names = [user_name for user_name, access_code in user_access_codes.items() if entered_code == access_code]

# If a user name is found for the entered access code, display the select box for that user

selected_user_name = st.sidebar.selectbox('Select Your User Name:', filtered_user_names)

selected_Cohort = st.sidebar.selectbox("Select a Cohort", ["Incubator_4","Incubator_1","Incubator_2","Incubator_3"])

# Display the selected option
st.write("Selected Cohort:", selected_Cohort)

# Function to read all CSV files from a folder and store them in a dictionary
# Function to read CSV files from a folder path obtained from GitHub and store them in a dictionary
# Define the GitHub API URLs for the folders containing CSV files


github_urls = {
    "Incubator_4":{
        "Goal Setting": "https://docs.google.com/spreadsheets/d/1N5xI5KkCxKL6YYA2a3mfaj4F-wSl5zFifu4A84UHoOY/edit?usp=sharing",
        "Searching & Securing Internship": 'https://docs.google.com/spreadsheets/d/1DnUPMOOxqgaPRJ6b0V9e8usGQtkVG1qJ7ffRzl_E5Uc/edit?usp=sharing',
        "Career Exploration": 'https://docs.google.com/spreadsheets/d/1nKOWNzHazM49Dw15vMEWhdJEhSTZvk3Wv4DU-eaImHY/edit?usp=sharing',
        "CAP": 'https://docs.google.com/spreadsheets/d/1aEeSsVazN2Zt0gOEOrC8zq5ikE9L9IQ2JA5yP3qUolU/edit?usp=sharing',
        "SMART Goals": 'https://docs.google.com/spreadsheets/d/19UrJUqaeXPDVcL6_bN0CiIc3fcSh_DputLNl4ciiR3w/edit?usp=sharing',
        "Resume": 'https://docs.google.com/spreadsheets/d/159uBGYMsbJGv70jbXF5vwEdB7m8zbubif_EbY1TFeVg/edit?usp=sharing'
        
    }
    ,
    "Incubator_6":{
        "Goal Setting(UK)": 'https://docs.google.com/spreadsheets/d/133hrhht7g2TC8NQIG30JKbSfDSoAr4SkPuuTvcQpYnY/edit?usp=sharing'
        # Add file names for Incubator_3
    }
}

# Update the URLs to point to the export format
urls = github_urls.get(selected_Cohort, {key: value.replace('/edit?usp=sharing', '/export?format=xlsx') for key, value in github_urls.items()})

# Read the data from the modified URLs into a pandas DataFrame based on user selection
selected_assignment_file = st.sidebar.selectbox('Select an assignment file', list(github_urls.keys()))
df = pd.read_excel(urls[selected_assignment_file])   



# Streamlit app interface
# Create the Streamlit app interface
st.title('STEMCHECK - STEM Assignment Checker Kit')


# URL pointing to the CSV file
file_url = 'https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/Comments_sheet__.csv?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svQ29tbWVudHNfc2hlZXRfXy5jc3YiLCJpYXQiOjE3MjU2MTUxMjMsImV4cCI6MTc1NzE1MTEyM30.xzsZgiQrq8uK4vvWLCbE8KHqvTUHFS5JBM-YQzLiXlo&t=2024-09-06T09%3A32%3A00.544Z'
# Make a GET request to the URL to retrieve the CSV file
try:
    response = requests.get(file_url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Read the content of the response as a pandas DataFrame, specifying the appropriate encoding
    category_dataset = pd.read_csv(BytesIO(response.content), encoding='latin1')  # You can try 'latin1' encoding as an alternative
    # Proceed with processing the data in the dataframe 'df'
except requests.exceptions.RequestException as e:
    print("An error occurred while accessing the CSV file:", e)
except Exception as e:
    print("An error occurred while reading the CSV file:", e)


unique_categories = category_dataset['Category '].unique()
unique_status=category_dataset['Accepted /Rejected'].unique()

#data = get_dataset(selected_assignment_file)
data=df

# Create a dropdown to select the file status
file_statuses = ["under review", "reviewed", "rejected"]
selected_status = st.sidebar.selectbox('Select File Status', file_statuses)

# Filter the data based on the selected status from the selected assignment file
filtered_data = df
filtered_data = filtered_data[filtered_data['status'] == selected_status]


# Create a dropdown to select the email ID
if 'user/email' in filtered_data.columns:
    email_list = filtered_data['user/email'].str.split('-').str[1].tolist()  # Extract email IDs after the hyphen

    # Placeholder to store the list of processed email IDs

    if "processed_emails" not in st.session_state:
        st.session_state.processed_emails = []  # Initialize the variable
    
    # Filter out the processed email IDs
    email_list = [email for email in email_list if email not in st.session_state.processed_emails]
    
    selected_email = st.selectbox('Select Email ID:', email_list)
    # Filter data based on selected email
    filtered_email_data = filtered_data[filtered_data['user/email'] == 'vigyanshaalainternational1617-'+selected_email]

    # Add a copy button to copy the email address to the clipboard
    if selected_email:
        #pyperclip.copy(selected_email)  # Copy the email address to the clipboard
        st.code(selected_email)
        st.write("Email address copied to clipboard")  # Inform the user that the email address has been copied

        

    if not filtered_email_data.empty:
       latest_submission_email = None
       latest_submission_col = None
       latest_submission_no = None
    
    
    # Get the latest filled column without NA or blank for the file name format 'data/{i}/fileName'
    for col in filtered_email_data.columns[::-1]:  # Iterate in reverse to get the last filled column
        if 'fileName' in col:
            latest_submission_email = filtered_email_data[col].dropna().iloc[-1] if not filtered_email_data[col].dropna().empty else None
            if latest_submission_email:
                latest_submission_col = col
                break

    #if latest_submission_email is not None:
        # Display the latest file name in the Streamlit sidebar
        #st.sidebar.markdown(f"File name: {latest_submission_email} (from column: {latest_submission_col})")
        #st.markdown(f"File name: {latest_submission_email}")
        #st.markdown(f"Submission No:{latest_submission_col}")
    file_name = latest_submission_col
    split_file_name = file_name.split('/')
    if len(split_file_name) > 2:
        result = split_file_name[1]  # Extract the part between the slashes
        latest_submission_no=result
    else:
        print("Invalid format")
    
    if latest_submission_email is not None:
        #st.markdown(f"File name: {latest_submission_email} (Submission No: {latest_submission_col})")
        #st.markdown(f"File name: {latest_submission_email} (Submission No: {result})")
        st.markdown(f"File name: {latest_submission_email}")
    else:
        st.sidebar.text("No valid file name found")


    if latest_submission_no is not None:
        st.markdown(f"Submission Number:{latest_submission_no}")

    if not filtered_email_data.empty:
        latest_messages = []
        # Get the latest message for the filtered email ID
        for col in filtered_email_data.columns:
            if 'message' in col:
                latest_message_column = filtered_email_data[col].dropna()
                if not latest_message_column.empty:
                    latest_message = latest_message_column.iloc[-1]
                    latest_messages.append(latest_message)

        if latest_messages:
            latest_email_message = latest_messages[-1]
            write_text = f"Comment: **{latest_email_message}**"
            st.sidebar.write(write_text)
        else:
            st.write('No message found for the selected email')
    else:
        st.write('No data found for the selected email')

    

# Display the select boxes with asterisk for compulsory selection
selected_category = st.sidebar.selectbox('Select category*', unique_categories, key='category_select')
selected_category_status = st.sidebar.radio('Select comments category status*', unique_status, key='category_status_radio')


# Check if either of the boxes is not selected
if not selected_category or not selected_category_status:
    st.error("Please fill in all the compulsory fields marked with * before proceeding.")
    st.stop()


# Filter the comments based on acceptance or rejection
if 'Accepted /Rejected' in category_dataset.columns and 'Comment' in category_dataset.columns:
    selected_category_accepted = category_dataset[(category_dataset['Category '] == selected_category) & (category_dataset['Accepted /Rejected'] ==selected_category_status)]['Comment'].tolist()
    
    if selected_category_accepted:
        # Create a multiselect to choose from the available comments
        selected_comments_accepted = st.multiselect('Select Comments:', selected_category_accepted)


        # Check if either of the boxes is not selected
        #if not selected_comments_accepted:
            #st.error("Please fill in all the compulsory fields marked with * before proceeding.")
            #st.stop()
        selected_comments_text_accepted=''
            
        if selected_comments_accepted:
            selected_comments_text_accepted = '\n'.join(selected_comments_accepted)
            comment_area_accepted = st.text_area('Selected Comments:', value=selected_comments_text_accepted, height=120)


        # Text area to allow the user to provide a custom comment
        custom_comment = st.text_area('Add Custom Comment:', height=60)
        
        # Concatenate the selected comments with the custom comment
        all_comments = selected_comments_accepted + [custom_comment] if custom_comment else selected_comments_accepted

        if all_comments:
            selected_comments_text_accepted = '\n'.join(all_comments)



# Create a text box to enter marks for the selected email ID and assignment file

if selected_email and selected_assignment_file:
    marks_key = f"marks_{selected_email}_{selected_assignment_file}"
    entered_marks = st.number_input("Enter Marks (Integer only):", max_value=10, key=marks_key)

    # Validate if the entered marks are within the allowed range
    if not isinstance(entered_marks, int) and entered_marks:  # Check if entered_marks is not empty
        st.warning("Please enter a valid integer for marks.")
        st.error("Please fill in all the compulsory fields marked with * before proceeding.")
        st.stop()
        
    if entered_marks is not None:  # Check if entered_marks is not None
        if entered_marks != 0:  # Check if entered_marks is not equal to 0
            st.write(f"Marks entered: {entered_marks}")
            marks = entered_marks  # Assign entered_marks to the marks variable
        else:
            marks = 0  # Assign 0 if entered_marks is 0
    else:
        marks = None

    # Proceed with using the 'marks' variable
    #if marks is not None:  # Check if marks has been properly assigned
        #st.write(f"Marks entered and validated: {marks}")
    #else:
        #st.warning("Marks is not provided or invalid.")

# Add an empty line to visually separate the elements
st.write("")

unique_key = latest_submission_email + " " + f"_Email {selected_email}"+" "+f"_Sub No:{latest_submission_no}"
# Define a function to create a DataFrame with the provided data
# Define the function to create the feedback DataFrame
def create_feedback_dataframe(unique_key, selected_user_name, selected_assignment_file, selected_status, latest_submission_email, latest_submission_no, selected_email, latest_messages, selected_comments_accepted, marks, selected_Cohort):
    data = {
        'key': [unique_key],
        'User_Name': [selected_user_name],
        'Assignment_File': [selected_assignment_file],
        'File_Status': [selected_status],
        'PDF_Name': [latest_submission_email],
        'Submission_Number': [latest_submission_no],
        'Email_ID': [selected_email],
        'Message_Displayed': [latest_messages],
        'Comments': [", ".join(selected_comments_accepted) if selected_comments_accepted else None],
        'Marks': [marks],
        'Cohort': [selected_Cohort]
    }

    feedback_df = pd.DataFrame(data)
    return feedback_df

# Your Supabase configurations
url: str = 'https://twetkfnfqdtsozephdse.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR3ZXRrZm5mcWR0c296ZXBoZHNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE5Njk0MzcsImV4cCI6MjAzNzU0NTQzN30.D76H5RoTel0M7Wj6PTRSAXxxYGic7K25BSaeQDZqIN0'

supabase: Client = create_client(url, key)

# Function to process the selected email
def process_email(selected_email):
    st.session_state.processed_emails.append(selected_email)

if 'processed_emails' not in st.session_state:
    st.session_state.processed_emails = []

# Process the button click
if selected_comments_text_accepted:
    combined_button_text = "Copy Comment, Save Feedback Data, and Extract Email IDs"
    if st.button(combined_button_text):
        st.code(selected_comments_text_accepted)
        process_email(selected_email)

        feedback_df = create_feedback_dataframe(unique_key, selected_user_name, selected_assignment_file, selected_status, latest_submission_email, latest_submission_no, selected_email, latest_messages, selected_comments_accepted, marks, selected_Cohort)
        if feedback_df is not None:
            # Insert the records into the Supabase table "TableF"
            records = feedback_df.to_dict(orient='records')
            for record in records:
                if record['Comments'] is None:  # Check for null values in the Comments column
                    record['Comments'] = ""  # Replace null with an empty string to satisfy the not-null constraint

            response = supabase.table("TableF").insert(records).execute()
            if response.get('error'):
                st.error("An error occurred while storing data in Supabase.")
            else:
                st.success("Data stored successfully in Supabase.")
else:
    st.info("Please provide comments before proceeding.")


# Make a GET request to fetch data from the specified table
# Fetch and display data from Supabase table 'TableF'
supabase_table_name = 'TableF'
supabase_url = 'https://twetkfnfqdtsozephdse.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR3ZXRrZm5mcWR0c296ZXBoZHNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE5Njk0MzcsImV4cCI6MjAzNzU0NTQzN30.D76H5RoTel0M7Wj6PTRSAXxxYGic7K25BSaeQDZqIN0'

response = requests.get(f'{supabase_url}/rest/v1/{supabase_table_name}', headers={'apikey': supabase_key})

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Extract the JSON response data
    # Convert the JSON data to a Pandas DataFrame
    df = pd.DataFrame(data)

    if filtered_user_names:


        # Group the DataFrame by 'Cohort' and 'User_Name' and count the number of occurrences
        cohort_user_counts = df.groupby(['Cohort','User_Name']).size().reset_index(name='User_Count')

        # Filter the cohort_user_counts DataFrame based on the selected_user_name
        selected_user_cohort_count = cohort_user_counts[cohort_user_counts['User_Name'] == selected_user_name]
        selected_user_cohort_count = cohort_user_counts[(cohort_user_counts['User_Name'] == selected_user_name) & (cohort_user_counts['Cohort'] == selected_Cohort)]

        if not selected_user_cohort_count.empty:
            st.write(f"Total Assignments corrected by {selected_user_name} in {selected_Cohort}: {selected_user_cohort_count['User_Count'].values[0]}")
        else:
            st.write(f"No assignments found for {selected_user_name} in {selected_Cohort}.")
    else:
        st.write("No user found for the entered access code. Please enter a valid code.")

            

        

