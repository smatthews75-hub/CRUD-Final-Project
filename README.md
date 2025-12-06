# CRUD Mini Database Final Project
### A python CLI application for university issued final project

## Presented by Team 3 : 
- Stephen Matthews (252404175)
- Dearryl Jeremiah Mawuntu (252410907)
- Wilson Leonardo (252502509)
- Chiara Clover Gunawan (252404486)
---

# The Purpose of this Final Project
This project aims to demonstrate the implementation **Create, Read, Update, and Delete** operations in a mini database application using Python. The CRUD operations are built around CSV files as the data storage format, allowing for manipulation and retrieval of data as dictionaries in the program. The project is designed to showcase the basic concepts of a CRUD system, including data management, user interaction, and file handling.  

The python version used in production of this project's source code is `Python 3.12.2`, though strictly adhering to the scope of material covered in lectures from IBDA1011.  

A quick explanation on how to use this program's modular CSV file handling feature is available in the `Explanations.ipynb` file included in this repository.

## Requirements to run this program
1. The minimum stable version of Python to run this program is predicted to be `Python 3.10` and above, likely due to the use of the csv module. This is based on automated analysis of this source code with `vermin 1.6.0` results shown below:
```bash
Minimum required versions: 3.10
Incompatible versions:     2
```

# Priority Features
1. CREATE
> Create new data entries to the program and the ability to write changes to the CSV file.
2. READ
> Read and display data entries from the CSV file in a user-friendly format.
3. UPDATE
> Update existing data entries in the program and write changes back to the CSV file.
4. DELETE
> Delete data entries from the program and update the CSV file accordingly.
---

# Additional Features
Although this project is not as innovative as expected from a final project, we have implemented some additional features to enhance the user experience and functionality of the CRUD mini database application. These features include:
1. Modular CSV Handling
> The program is designed to handle different CSV files by allowing users to specify the file path and fields to treat as main dictionary keys and which fields to be arranged in groups. This modular approach enables users to work with various datasets without modifying the core source code.
2. Grouped Data Display
> The program supports grouping related fields together when displaying data entries. This feature improves readability and organization of the output, making it easier for users to understand the relationships between different data fields.
3. Minimalist and modular source code
> The source code is kept minimal and straightforward, involving only one import of the csv module, focusing on the essential CRUD operations while maintaining clarity.