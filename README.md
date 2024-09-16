[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AHFn7Vbn)
# Superjoin Hiring Assignment

### Welcome to Superjoin's hiring assignment! 🚀

### Objective
Build a solution that enables real-time synchronization of data between a Google Sheet and a specified database (e.g., MySQL, PostgreSQL). The solution should detect changes in the Google Sheet and update the database accordingly, and vice versa.

### Problem Statement
Many businesses use Google Sheets for collaborative data management and databases for more robust and scalable data storage. However, keeping the data synchronised between Google Sheets and databases is often a manual and error-prone process. Your task is to develop a solution that automates this synchronisation, ensuring that changes in one are reflected in the other in real-time.

### Requirements:
1. Real-time Synchronisation
  - Implement a system that detects changes in Google Sheets and updates the database accordingly.
   - Similarly, detect changes in the database and update the Google Sheet.
  2.	CRUD Operations
   - Ensure the system supports Create, Read, Update, and Delete operations for both Google Sheets and the database.
   - Maintain data consistency across both platforms.
   
### Optional Challenges (This is not mandatory):
1. Conflict Handling
- Develop a strategy to handle conflicts that may arise when changes are made simultaneously in both Google Sheets and the database.
- Provide options for conflict resolution (e.g., last write wins, user-defined rules).
    
2. Scalability: 	
- Ensure the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimize for scalability and efficiency.

## Submission ⏰
The timeline for this submission is: **Next 2 days**

Some things you might want to take care of:
- Make use of git and commit your steps!
- Use good coding practices.
- Write beautiful and readable code. Well-written code is nothing less than a work of art.
- Use semantic variable naming.
- Your code should be organized well in files and folders which is easy to figure out.
- If there is something happening in your code that is not very intuitive, add some comments.
- Add to this README at the bottom explaining your approach (brownie points 😋)
- Use ChatGPT4o/o1/Github Co-pilot, anything that accelerates how you work 💪🏽. 

Make sure you finish the assignment a little earlier than this so you have time to make any final changes.

Once you're done, make sure you **record a video** showing your project working. The video should **NOT** be longer than 120 seconds. While you record the video, tell us about your biggest blocker, and how you overcame it! Don't be shy, talk us through, we'd love that.

We have a checklist at the bottom of this README file, which you should update as your progress with your assignment. It will help us evaluate your project.

- [ ] My code's working just fine! 🥳
- [ ] I have recorded a video showing it working and embedded it in the README ▶️
- [ ] I have tested all the normal working cases 😎
- [ ] I have even solved some edge cases (brownie points) 💪
- [ ] I added my very planned-out approach to the problem at the end of this README 📜

## Got Questions❓
Feel free to check the discussions tab, you might get some help there. Check out that tab before reaching out to us. Also, did you know, the internet is a great place to explore? 😛

We're available at techhiring@superjoin.ai for all queries. 

All the best ✨.

## Developer's Section

*Add your video here, and your approach to the problem (optional). Leave some comments for us here if you want, we will be reading this :)*

Watch the [overview video on Loom](https://www.loom.com/share/80e4b05e76af414da845fd03dd2789e9?sid=f57e7f69-fce9-40ce-8b02-f4e37b5db1cc) to see a demonstration of the project.


# Google Sheets and MySQL Synchronization

## Overview
This project provides a solution to synchronize data between Google Sheets and a MySQL database. It includes setting up the environment, establishing connections, performing initial data loads, monitoring for changes, and handling CRUD operations. The system also maintains detailed logs and handles errors gracefully.

## Approach

### 1. Setup and Configuration

#### Objective: Prepare the environment and configure access to Google Sheets and MySQL.

**Google Sheets API Configuration:**
1. Create a Google Cloud project and enable the Google Sheets API.
2. Generate a Service Account and download the credentials (`key.json`).
3. Share the Google Sheet with the service account email to allow access.

**MySQL Configuration:**
1. Ensure MySQL is installed and running.
2. Create a MySQL database and user with appropriate permissions.
3. Update the `DB_CONFIG` dictionary in the script with the MySQL credentials.

### 2. Establishing Connections

#### Objective: Set up connections to Google Sheets and MySQL.

**Google Sheets Connection:**
- Use the Google Sheets API to authenticate and connect using the service account credentials.

**MySQL Connection:**
- Establish a connection to the MySQL database using the provided configuration.

### 3. Initial Data Load and Table Creation

#### Objective: Load existing data from Google Sheets and prepare the MySQL database.

**Retrieve Sheet Metadata:**
- Fetch all sheets from the specified Google Sheets document.

**Create Tables:**
- For each sheet, create a corresponding table in MySQL if it does not already exist.
- Define the table schema based on the sheet’s headers.

**Load Initial Data:**
- Retrieve data from each sheet and insert it into the corresponding MySQL table.

### 4. Monitoring and Synchronization

#### Objective: Continuously monitor Google Sheets for changes and synchronize with MySQL.

**Polling Mechanism:**
- Periodically check for changes in the Google Sheets data.
- Compare current data with previously loaded data to detect any changes.

**Apply Changes:**
- If changes are detected, update the MySQL database accordingly:
  - Delete old data and insert new data if significant changes are found.
  - Log all changes for auditing purposes.

### 5. CRUD Operations

#### Objective: Allow users to perform Create, Read, Update, and Append operations on Google Sheets.

**User Operations:**
- Provide options for users to create new sheets, read data from specific ranges, update existing data, or append new data to sheets.
- Implement interactive commands for users to perform these operations.

### 6. Logging and Error Handling

#### Objective: Maintain detailed logs and handle errors gracefully.

**Logging:**
- Record all operations, changes, and errors in a log file (`sheet_monitor.log`).
- Ensure logs are detailed and provide sufficient information for troubleshooting.

**Error Handling:**
- Implement error handling for database connections, API requests, and data operations.
- Log errors and provide appropriate feedback.

## Summary

- **Setup and Configuration:** Prepare Google Sheets and MySQL environments.
- **Establish Connections:** Connect to Google Sheets and MySQL.
- **Initial Data Load and Table Creation:** Load initial data and create MySQL tables.
- **Monitoring and Synchronization:** Continuously monitor Google Sheets and synchronize with MySQL.
- **CRUD Operations:** Allow users to perform Create, Read, Update, and Append operations.
- **Logging and Error Handling:** Maintain logs and handle errors.

This approach ensures that the synchronization process is efficient, reliable, and flexible, allowing for real-time updates and user interactions.

## Getting Started

1. Follow the [Setup and Configuration](#1-setup-and-configuration) steps to prepare your environment.
2. Run the script to start monitoring and synchronizing data.
3. For more detailed information on using the script, refer to the [Usage Instructions](#usage-instructions).

## Usage Instructions

```python
# Example of how to use the script
if __name__ == "__main__":
    SPREADSHEET_ID = 'your_google_sheet_id_here'  # Replace with your Google Sheet ID
    monitor_all_sheets(SPREADSHEET_ID)

