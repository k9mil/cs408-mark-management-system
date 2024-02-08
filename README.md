# 📚 Mark Management System [TERZ05]

Mark Management System is a platform that streamlines data aggregation and presentation, aiding exam boards in efficient decision-making. See below for a non-exhaustive list of features that the system contains.

## Features
- **User Login/Registration System**: A secure authentication system enabling administrators to set up accounts and users to log in with their credentials.
- **Personalised Dashboard**: Each user is provided with a tailored dashboard, with custom cards including information such as student performance metrics which contain data such as the mean, median, mode and pass rate, a list of taught classes, and an overview of classes.
- **Marks Upload**: Allows the ability to upload student marks for the classes you teach with robust validation to ensure accuracy and integrity of data.
- **Class System**: Allows administrators to create classes, assign lecturers to classes and modify class details. These classes serve as a core part of the application as they are connected to degrees, students and marks.
- **Role System**: Different user roles exist throughout the application, such as administrators and lecturers, each with tailored permissions and controls.
- **Settings**: Customizable settings allow for users of the site to edit their personal details, such as their first name, last name or password.
- **JWT Tokens**: Ensures safety & security by storing key data in JWT tokens which is used as an additional layer of authentication and verification.
- **Modals**: Help and support can be found throughout the page, with a dedicated page with useful information, alongside Modals which contain tips are scattered throughout the system.

and much more!

## Installation

If you wish to run this web application locally, [Python](https://www.python.org/) will be **necessary** for you to be able to run this system.

1. Clone the repository.
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

## Usage

As of right now, a registration system does not exist on the frontend. To be able to use the system, you will have to create the account via an endpoint, which is an unprotected route.

For more information on the API usage, head over to:
- OpenAPI: `/docs`
- ReDoc: `/redoc`

After the account is created, you can login on the frontend and use the system!

## Contact

If you have any questions, feel free reach out to: `kamil.zak.2021@uni.strath.ac.uk`.