# Nimble Project

This project is designed to retrieve information from the "Nimble" server and store it.
Information is stored in the fields: first name, last name, email, description.
Of course, this project is done as an example, and there are many things that need to be improved.

### Getting Started

#### 1. Running the Entire Project in Docker

- Clone the repository to your local computer:
 https://github.com/SergGurzhy/Nimble.git
- In the `.env` file, enter your database parameters.
- Run service  (You should have Docker installed and running.):
```sh
  docker-compose up --build -d
  ```
## Possible Actions with the Service:

1. **GET**  `http://localhost:5000/api/search`  with param: (a string you want to find occurrences of). Returns: JSON with records containing the given word.
2. **GET**  `http://localhost:5000/api`       Returns: JSON with all records in the database, status code.
3. **POST** `http://localhost:5000/api/drop`  Deletes all information in the database, status code.
4. **POST** `http://localhost:5000/api/update`  Updates the database from the Nimble API.
5. **POST** `http://localhost:5000/api/initialization`  Creates a table and populates it with data from the Nimble Contacts.csv file.




## Logic for Updating and Storing Information:

**The database update strategy was determined independently. Not specified in the specification.**

- Information is stored only about "person" entities.
- A person may not have an email.
- A person may not have a description.
- In the database, records with the same email for a person cannot be stored.
- The database allows storing persons with the same full name.
- A person can delete an Email.
- A person can add an Email.

## Upon Starting the Service:
- If the database is empty: initialization and populating of the database are performed from the Nimble Contacts 2.csv file.
- If information exists: connection to the database is established.

## Running Tests

- Tests are located in the `tests` directory.
- Tests that validate the logic of the database update function can be found in `test_update_db.py`.
- Tests that verify the functionality of the Nimble API's `endpoint are available.
- Note that the test suites are not exhaustive and may not cover all scenarios.
