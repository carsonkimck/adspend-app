# AdSpend App: Your Ultimate Ad Campaign Spending Tracker

Welcome to AdSpend App, the web application designed to empower users in tracking their ad campaign spending across various platforms. Developed using Flask, a lightweight micro web framework written in Python, AdSpend-App offers a seamless and efficient solution for managing ad expenditures with precision.

## Features and Workflow

### Etsy Authorization Flow

- **Request Authorization**: Simply click the button on the home page to initiate the Etsy authorization process.
- **Permission Granting**: Users are directed to grant permission via a generated link.
- **Access Token Retrieval**: Upon permission, the application retrieves the access code, facilitating the acquisition of a permanent access token stored securely in the database.
- **Real-time Charge Updates**: Etsy charges (resources) are dynamically retrieved every time a sheet is generated, ensuring charges are up-to-date for the respective month.

### Google Authorization Flow

- **Streamlined Authorization**: Generate a Google link through the site button.
- **Scope Access**: Users are prompted to grant access for sheets and AdWords scopes.
- **Token Generation**: Upon acceptance, the application generates access and refresh tokens for the user.

### Sheet Initialization

- **Template Duplication**: AdSpend-App automates the initialization process by creating a custom Google Sheet using the Google Sheets API.
- **Initial Value Setup**: Sets initial values to zero, laying the foundation for monthly charge updates.
- **Monthly Charge Updates**: AdSpend-App ensures monthly charge updates by pulling Etsy and Google charges and updating associated cells with the most current values. The API is called each time a sheet is generated, guaranteeing updated numbers within the month.

## Technical Specifications

### Tech Stack

- **Backend Framework**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **OAuth Integration**: Etsy, Pinterest, and Google OAuth for authorization
- **External APIs**: Integration with Etsy, Pinterest, and Google APIs for charge retrieval

Experience the efficiency and precision of AdSpend-App in managing your ad campaign spending. With its intuitive workflows and real-time updates, AdSpend-App is your ultimate companion for optimizing ad expenditures across platforms.

## Get in Touch

Ready to elevate your ad campaign tracking experience? 

Unlock the power of precise ad spending tracking with AdSpend-App today! 📊💡
