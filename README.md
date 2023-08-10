# Nimble Project

This project is designed to retrieve information from the "Nimble" server and store it.
Information is stored in the fields: first name, last name, email, description.

**The database update strategy was determined independently. Not specified in the specification.**



## Logic for Updating and Storing Information:
- Information is stored only about "person" entities.
- A person may not have an email.
- A person may not have a description.
- In the database, records with the same email for a person cannot be stored.
- The database allows storing persons with the same full name.
- A person can delete an email.
- A person can add an email.

## Upon Starting the Service:
- If the database is empty: initialization and populating of the database are performed from the Nimble Contacts.csv file.
- If information exists: connection to the database is established.

## Possible Actions with the Service:

1. **GET**  `http://{base url}/api/search`  with param: (a string you want to find occurrences of). Returns: JSON with records containing the given word.
2. **GET**  `http://{base url}/api`       Returns: JSON with all records in the database, status code.
3. **POST** `http://{base url}/api/drop`  Deletes all information in the database, status code.
4. **POST** `http://{base url}/api/update`  Updates the database from the Nimble API.
5. **POST** `http://{base url}/api/initialization`  Creates a table and populates it with data from the Nimble Contacts.csv file.

### Getting Started

#### 1. Running the Entire Project in Docker

- Clone the repository to your local computer:
 https://github.com/SergGurzhy/Nimble.git
- In the `.env` file, enter your database parameters.
- Create the database:
  ```sh
  docker run --name nimble_data --env-file .env -p 5432:5432 -d postgres
