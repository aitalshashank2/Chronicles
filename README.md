# Chronicles
This repository houses code for **Chronicles**, a platform where debuggers and developers unite to exterminate bugs. You are looking at the backend of the project with all the files required for dockerising it's implementation. Do visit the [Frontend](https://github.com/aitalshashank2/Chronicles-Frontend) of this project.

## Features
- Create Multiple Projects with a unique team.
- Secure Login and Registration using OAuth2.0.
- Report bugs in a project and use various in-built tags to highlight them.
- Implementation of RichText Fields for descriptions of Project and Bugs.
- Option to upload images in the description for Bug Reports.
- Real-time commenting on Bug Reports using web sockets
- Option to assign a bug report to a team member.
- Show the status of Bug Report
- Look at your Projects and the Bugs Reports assigned to you, all in one place

## Set up instructions

- Clone this repository and change directory
  ```bash
  git clone https://github.com/aitalshashank2/Chronicles.git
  cd Chronicles
  ```

- Clone the Frontend Web Application inside the `frontend/` directory
  ```bash
  cd frontend/
  git clone https://github.com/aitalshashank2/Chronicles-Frontend.git
  ```

- Copy `code/configuration/config-stencil.yml` to `code/configuration/config.yml` and populate the values.
  ```bash
  cd ../code/configuration/
  cp config-stencil.yml config.yml
  ```
  
- Build the project after returning to the base directory (containing the `docker-compose.yml` file)
  ```bash
  docker-compose build
  ```

- Run the project
  ```bash
  docker-compose up -d
  ```

- Visit **Chronicles** on [http://localhost:54330/](http://localhost:54330/)

- In order to stop the project, navigate to the base directory (containing the `docker-compose.yml` file) and run the following command
  ```bash
  docker-compose down
  ```

### Happy Coding!
