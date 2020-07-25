Watch the video:

https://www.youtube.com/watch?v=VCxzmaSKGIc

# Project 1

Web Programming with Python and JavaScript

This is a book review website. Users can register, login, and then search for a book using title, author or isbn. They will then be taken to a ‘search results’ page. After clicking on any book title, they will be taken to a ‘book page’ where there are further details about the book, including information from goodreads. They will also be able to leave a review on this page. The project also includes an api. When calls to the api are made, using an isbn number, users will be able to access details about the relevant book.

*application.py*
This is the Python code for the web application. It contains functions such as register, login, search, etc, to run the application using Flask

*import.py*
This file contains code to import the details of the books given in the books.csv file into the PostgreSQL database.

*layout.html*
This is the Flask base template for the entire website. It includes the logo and a background image.

*index.html*
This is the home page of the website. It includes a catchphrase.

*register.html*
This is where users can register for the website.

*apology.html*
This page appears when users that are not logged experience an error, such passwords not matching when they register.

*login.html*
Users can login on this page

*search.html*
Users can search for a book once logged in on this page

*book.html*
When users click on a book title on the ‘results.html’ page they will be taken to this page where there are more details about the book, including information about the book from ‘goodreads’ and any reviews of the book left on the website. Users can also submit their own rating and review of the book.

*goodbye.html*
When users logout they will be taken to this page, with the opportunity of login back in or registering.

*results.html*
This is the search results page, displaying the title, author and isbn of all books from the search query. By clicking on a book title, users will be directed to the book page, ‘book.html’.

*loggedin_apology.html*
This is the error page for users that have logged in, such when no results match their search.

*apology.jpg*
This is an image that is shown in the apology page.

*logo.png*
This is a logo I have designed for the website using FreeLogoDesign.com

*books.jpg*
This is the background image I have chosen for the website from a Google search.

*main.css*
This is the styling for ‘layout.html’ the base template for the website.

*styles.css*
This is the styling for the home page of the website ‘index.html’.

*register.css*
This is the additional styling for the registration page, ‘register.html’.

*apology.css*
This is the additional styling for the ‘apology.html’ page.

*login.css*
This is the additional styling for the ‘login.html’ page.

*book.css*
This is the additional styling for the ‘book.html’ page.

*goodbye.css*
This is the additional styling for the ‘goodbye.html’ page.

*results.css*
This is the additional styling for the ‘results.html’ page.

*search.css*
This is the additional styling for the ‘search.html’ page.

*loggedin_apology.css*
This is the additional styling for the ‘loggedin_apology.html’ page.





