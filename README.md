# bookshop-app-api
Bookshop API project.

Dockerized Django App for a Bookshop with PostgreSQL db.<br />
To run  docker-compose build && docker-compose build.<br />
The app will wait for db initialization, then load the data from data/BOOKS.ods to the db during startup via Django Commands
* Endpoints are as follows:
    * For filtering via GET request: /api/book/books/?number_of_pages=100&author_gender=female
    * For creating a new book via POST request: /api/book/books/
    * For updating a book via PUT andPATCH request: /api/book/books/id
