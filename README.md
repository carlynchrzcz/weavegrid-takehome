# App description
The application is a REST API to display file information from a portion of the user’s file system. The user will specify a root directory when launching the application. All directories from the root on downward are then browsable using the REST API.

# Running the app
Run the following script to build and run the app using Docker:

```
run_app.sh <root_path>
```

The `root_path` is an absolute path to the portion of the file system that the REST API may explore. If no path is specified, it will default to the current working directory.

The app can be accessed at http://localhost:5000.

# Api Documentation
## GET /{path}
### Description
An endpoint to display information about a file contained in the  `root_path` directory.
If the specified path is a regular file, the API will respond with the contents of the file. If the specified path is a directory, the API will respond with a list of the files in the directory, including their name, owner, size, and permissions.

### Parameters
| Name   | Description |
| ------ | ----------- |
| path   | The path (relative to the specified `root_path`) of the file to be retrieved |

### Responses

#### When a Regular File is Provided
**Status: 200**

The API will respond with a string containing the contents of the file.

#### When a Directory is Provided
**Status: 200**

The API will respond with a list of objects representing all the files in the directory.

Each object contains the following keys:

| Key         | Description |
| ------      | ----------- |
| name        | The name of the file |
| owner       | The username of the owner of the file |
| size        | The size of the file in bytes |
| permissions | The octal representation of the file permissions |

#### When an Invalid Path is Provided
**Status: 404**

The API will respond with

```
{ "message": "File not found" }
```

# Additional Information
## Time Spent on Exercise

I spent about **3 hours** writing and Dockerizing the application. I hadn't used Flask before (but wanted to try it since I know that's what the company uses!), so this step took some additional time.

I spent about **1 hour** on testing and documentation.

Total time: **4 hours**
