# 📚 Mark Management System [TERZ05]

Mark Management System is a platform that streamlines data aggregation and presentation, aiding exam boards in efficient decision-making. Additionally, the system aims to make the process of uploading marks more enjoyable, by automating some laborious and time-intensive tasks. See below for a non-exhaustive list of features that the system contains.

## Features

- **User Login/Registration System**: A secure authentication system enabling administrators to set up accounts and users to log in with their credentials.
- **Personalised Dashboard**: Each user is provided with a tailored dashboard, with custom cards including information such as student performance metrics which contain data such as the mean, median, mode and pass rate, a list of taught classes, and an overview of classes.
- **Unique Graphs**: On each dashboard, amongst other pages, there are Bar Graphs present which offer unique insights into the performance of students.
- **Data Upload**: Allows the ability to upload student marks for the classes you teach with robust validation to ensure accuracy and integrity of data. Additionally, allows the upload of academic misconduct, or personal circumstances of students.
- **Data Conversion**: Instead of leaving the laborious process of converting files from MyPlace to the Marks Management System format, or from the Marks Management System format to the format Pegasus expects, the system does that for you.
- **Class System**: Allows administrators to create classes, assign lecturers to classes and modify class details. These classes serve as a core part of the application as they are connected to degrees, students and marks.
- **Role System**: Different user roles exist throughout the application, such as administrators and lecturers, each with tailored permissions and controls.
- **Settings**: Customisable settings allow for users of the site to edit their personal details, such as their first name, last name or password.
- **JWT Tokens**: Ensures safety & security by storing key data in JWT tokens which is used as an additional layer of authentication and verification.
- **Modals**: Help and support can be found throughout the page, with a dedicated page with useful information, alongside Modals which contain tips are scattered throughout the system.

and much more, such as individual Student Profiles, Class Profiles and Error Pages!

## Installation

To install the Mark Management System locally, here are the prerequisites:

- Python >= 3.10.9
- Node >= 16
- Vite >= 5.0.11
- PostgreSQL >= 14.10
- Git >= 2.37.1

_note that lower versions may work with the system, however, these are the versions that the system was built with._

Any further dependencies will be installed as part of the setting up process.

1. Start by cloning the repository.

   ```
   $ git clone https://github.com/k9mil/cs408-mark-management-system.git
   $ cd cs408-mark-management-system
   ```

2. Initialize a virtual environment for packages (ensure that you are in the /backend directory!).

   ```
   [PowerShell]
   > python -m venv venv
   > venv/Scripts/activate

   [Bash]
   $ python -m venv venv
   $ source venv/bin/activate
   ```

3. Install the dependencies.

   ```
   $ pip install -r requirements.txt
   ```

4. With the dependencies now being installed, you now have to modify a few configuration attributes.

Head over to the `config.py` file located at `/backend/api`, where you will see that `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY` and `DATABASE_URL` take their values from environment variables. It is important to note that `JWT_SECRET_KEY` and `JWT_REFRESH_SECRET_KEY` can theoretically be anything for the site to be run locally, but the `DATABASE_URL` (in the `DevelopmentConfig` class) will have to point to your instance of Postgres.

The environment variables can either be set on your local machine, or hardcoded in the `config.py` file.

This means, that you will have to create a Postgres database (the tables are automatically generated for you), and point the server correctly to your instance. See the [PostgreSQL documentation](https://www.postgresql.org/docs/current/sql-createdatabase.html) or [StackOverflow](https://stackoverflow.com/questions/30641512/create-database-from-command-line-in-postgresql) for information on how to create a Postgres database.

The `DATABASE_URL` is usually structured as follows:

```
postgresql://postgres:admin@localhost:5432/mms
```

Where the components of this Database URL being as follows:

- `postgres` is the username for the database.
- `admin` is a sample password for the user.
- `localhost` is the hostname where the Postgres is running.
- `5432` is the port number on which Postgres is listening for connections (5432 is the default port).
- `mms` is the specific database to which the application will connect.

5. Run the FastAPI backend.

   ```
   $ python asgi.py
   ```

To run the frontend, you'll need to ensure that you have [Node](https://nodejs.org/en) on your local machine. Assuming the repository has already been cloned, follow the following steps:

1. Install the necessary packages.

   ```
   $ npm i
   ```

2. Run the Vite + React frontend.
   ```
   $ npm run dev
   ```

## Sample Data Generation

This system contains a file inside /backend/scripts, which is called `db_base_values.py`. After setting up the dependencies and going through the installation process outlined above, you can run the file to generate some sample data, including roles, users, classes, students, degrees and some marks.

The system will generate two types of users, an administrator and a lecturer which you can access with these details:

- `admin@mms.com` with the password `12345678`
- `lecturer@mms.com` with the password `12345678`

You may also want to generate some sample marks data for the system, head over to [scripts](https://github.com/k9mil/cs408-mark-management-system/tree/main/mark-management-system/scripts) which contains a useful, customisable Mark Generation Script written in Python alongside documentation.

Additionally, some sample files have been provided to showcase the types of fields that are required for each upload or conversion type, which can be found in `/scripts/manual_test_files`.

## Testing

This system contains a large amount of integration tests, which have been written in `pytest` due to its direct compatibility with FastAPI. In order to run the integration test suite, a mocked database (in other words, another PostgreSQL database) has to be setup first in order for the test suite to be ran. Please ensure that `MMS_DATABASE_URL_TEST` is a valid environment variable pointing to the mocked database.

As before, you have to modify either the environment variable, or hardcode it in the `config.py` file, in the `TestingConfig` class. In the case that is not set up, the testing will default to using the primary database, meaning some tests can fail (if there is pre-existing data in the table), therefore, please ensure that the testing database is set up correctly.

Once you have ensured that the environment variable is set up, you can run the test suite by heading over to the `/tests` directory, in which you can run the entire test suite by running:

```
pytest
```

If you wish to run tests on only a single file, you can achieve so by running:

```
pytest <file_name>.py
```

## Usage

As mentioned before, you can either run the script which generates some default data, or alternatively, you can create an account (and anything else) via the API which can be accessed by either:

- OpenAPI: `/docs`
- ReDoc: `/redoc`

At the moment the system does not support a registration system, so if you want to create an account yourself you will have to use the endpoints (or access the database directly!).

## Documentation

In the backend, a mixture of OpenAPI + ReDoc endpoint documentation and loose [Google Style Comments](https://google.github.io/styleguide/pyguide.html) are used. As mentioned before, OpenAPI can be conveniently accessed by /docs, and ReDoc can be accessed by /redoc, giving you, the user the choice!

For the frontend, a good chunk of the components are from [shadcn/UI](https://ui.shadcn.com/), therefore no component documentation takes place. However, some functions are commented based on the [TSDoc](https://tsdoc.org/) standard for additional clarity.

Additionally, each page is recreated inside [Figma](https://www.figma.com/), which not only allows for quick prototyping, but also serves as additional documentation of the entire frontend of the system.

## Demo

If you wish to use the system — without going through the trouble of setting it up yourself, feel free to visit the [hosted variant](http://16.171.10.73) of Marks Management System.

The details of the accounts provided earlier also work for the site.

## Contact

For any questions, feel free reach out to: `kamil.zak.2021@uni.strath.ac.uk`.
