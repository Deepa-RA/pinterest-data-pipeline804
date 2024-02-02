# Milestone 2 - Get started

## Pinterest data
The file user_posting_emulation.py contains the login credentials for a RDS database, which contains three tables with data resembling data received by the Pinterest API when a POST request is made by a user uploading data to Pinterest:
- pinterest_data contains data about posts being updated to Pinterest
- geolocation_data contains data about the geolocation of each Pinterest post found in pinterest_data
- user_data contains data about the user that has uploaded each post found in pinterest_data

The provided script contains an infinite loop that illustrates streaming data for Pinterest.
```
python user_posting_emulation.py
```

## Sign into AWS Cloud
Credentials required include:
- Account ID
- IAM Username
- Password
