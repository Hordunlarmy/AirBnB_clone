# AirBnB Clone

AirBnB Clone is a project that aims to replicate the basic functionality of the Airbnb web application, focusing on property rental and management. This project provides a command-line interface (CLI) for managing property listings, users, and bookings.

## Command Interpreter

The Command Interpreter is a command-line tool that allows users to interact with the AirBnB Clone application. You can use the command interpreter to create, read, update, and delete property listings, users, and bookings. It provides a set of commands to perform various operations, such as listing properties, searching for properties, creating users, making bookings, and more.

## Getting Started

To get started with the AirBnB Clone Command Interpreter, follow these steps:

1. Clone the GitHub repository:

   ```bash
   git clone https://github.com/yourusername/AirBnB_clone.git


How to Use
The Command Interpreter accepts a variety of commands, such as:

create - Create a new object (property, user, booking, etc.).
show - Display details of a specific object.
update - Update the attributes of an object.
destroy - Delete an object.
all - List all objects of a specific type.
quit - Exit the Command Interpreter.
For detailed instructions on how to use each command, you can type help <command> in the Command Interpreter.


Examples
Here are some example commands to give you an idea of how to use the Command Interpreter:

To create a new property listing:

lua
Copy code
(hbnb) create Place name="Cozy Cabin" price=100
To list all properties:

scss
Copy code
(hbnb) all Place
To update the price of a property:

scss
Copy code
(hbnb) update Place 1234 price 120
To quit the Command Interpreter:

scss
Copy code
(hbnb) quit
