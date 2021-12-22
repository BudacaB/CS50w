## Distinctiveness and Complexity

- The idea for my project is a budget application, i.e. distinct from a social network application or an e-commerce application
- The functionality of the project is aimed at helping users keep track of expenses and accessing a breakdown over the current day, or other selected days or date ranges
- I have used new and complex elements like: 
    - working with dates or date ranges
    - formatting and using browser/client-side date and time for displaying information, for requests, and for database operations
    - some basic calculations for precentages
    - used input validation with regular expressions
    - used query strings
    - refreshing the UI for date changes, e.g. when the current day changes
    - employed HTTP 'Delete' requests

## Files and contents

- ### JavaScript:
    - edit.js:
        - on 'DOMContentLoaded': code used for displaying the date of the day being viewed for editing
        - 'editExpense()': code used for arranging the UI for editing individual expenses
        - 'saveExpense()': code used for sending the request to save the updated expense and rearrange the UI
        - 'deleteExpense()': code used for sending the request to delete an expense
    - index.js:
        - on 'DOMContentLoaded': 
            - code used for displaying the current date and attaching it to certain elements for subsequent requests
            - getting and displaying the expenses information
            - code to update the date every second and refresh the expenses information (e.g. if the day changes then there shouldn't be any expenses displayed if not introduced yet)
        - 'addExpense()': code for adding a new expense
        - 'getPercentages()': code used for retrieving the expenses information
        - 'getDateDay()': code used for getting and validating the date selected by the user
        - 'getDateRange()': code used for getting and validating the date range selected by the user 
        - 'useDateRange()': code used to retrieve the expenses information based on the date range selected and arrange the UI to display it
        - 'changeDate()': code used to pass the selected date to the elements that use it and to retrieve and display the expenses information for this date
        - 'resetAndReload()': code for allowing the user to clear previous selections and start fresh
    - profile.js:
        - 'deleteAccount()': code used for deleting a user and all its data

- ### CSS: 
    - styles.css: CSS code used for styling

- ### HTML:
    - edit.html: displaying the expenses for a particular date and expense and allowing edits and removals
    - index.html: main page, allowing the users to input expenses, view the expenses info for the current day, or for different dates and date ranges that can be selected
    - layout.html: skeleton HTML for navbar and stylesheets
    - login.html: login page
    - register.html: register page
    - profile.html: page where the user can see the date when they joined and also delete the account if they want to remove it and all its data

- ### Python:
    - models.py:
        - 'User(AbstractUser)': used for managing users and authentication
        - Four models with the same structure for the chosen categories: a user (foreign key to the 'user' table), the created date and the amount
            - 'Food': used for 'food' expenses
            - 'Bill': used for 'bills' expenses
            - 'Transport': used for 'transport' expenses
            - 'Fun': used for 'fun' expenses
    - urls.py
        - 'index', 'login', 'logout', 'register': similar to previous applications, code used for the 'root' path or for routing to registration and authentication pages
        - 'edit': used for editing expenses and the 'edit' page
        - 'stats': used for retrieving expense information
        - 'profile': used for accessing the profile page to view user info and/or delete an account
        - 'range': used for retrieving expense information for a given date range
    - views.py:
        - 'login_view()', 'logout_view()' and 'register()': similar to previous applications, code used for the registration and authentication pages
        - 'index()': code used for serving 'index.html' or saving new expenses to the database
        - 'edit()': code used for serving 'edit.html' with expenses information, performing expenses updates or deletes
        - 'get_expense_total()': code used for calculating the total for a QuerySet of expenses
        - 'get_percentage()': code used for calculating the percentage of an expense type out of the grand total for all four expense types combined
        - 'get_stats()': code used for serving the statistical information for the expenses on a given date
        - 'profile()': code used for serving the 'profile.html' page, user information and performing deletes for the account
        - 'get_range_stats()': code used for serving the statistical information for the expenses in a given date range

## How to run

- in the terminal, cd into the 'capstone' directory
- run 'python manage.py migrate --run-syncdb'
- run 'python manage.py runserver'
- (no Python packages added)

## Additional information

N/A