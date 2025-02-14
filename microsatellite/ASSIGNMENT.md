# Week 3 - Database Assignment

## Set Up Instructions

> **NOTE:** You must have Docker installed and Docker Desktop is running.

1. Make sure you are at microsatellites directory in the command line. You can check where you are with `pwd`. You can change directories with `cd`. If you're at `sci-tech-projects`, `cd microsatellites` will do.

2. Run `make start-backend`. This is a command I define in the Makefile that will ease the process of setting up the database.

3. Connect to database (mysql docker container)
`docker exec -it mysql mysql -u root -p`

1. It will ask for your password. Enter `my-secret-pw`. 
> **NOTE:** you will not see the password as you type it. It's intended.

## Database Query Instructions

5. You are now in your mysql container's environment AND logged into the database. Show all databases by running the following query:
    ```
    SHOW DATABASES;
    ```

6. Use biology database by running the following query:
    ```
    USE BIOLOGY;
    ```

7. Show tables in biology database by running the following query:

    ```
    SHOW TABLES;
    ```

8. Display all rows from microsatellites by running the following query:
    ```
    SELECT * FROM microsatellites;
    ```

## Assignment Instructions

Now that you have the database set up and you have seen the data in the microsatellites table, you will perform the following tasks:

1. Show only name and base from microsatellites

2. Remove Ricardo from microsatellites

3. Insert new row of data

Run each query in the mysql container, screenshot the output for each query, and copy the query you used in a file named `queries.sql`.

Submit `queries.sql` and the screenshots (expecting three) of the output for each query. 

# Resources

- [Selecting specific values from a table](https://www.w3schools.com/sql/sql_select.asp) 
- [Removing a row](https://www.w3schools.com/sql/sql_delete.asp) 
- [Inserting a row](https://www.w3schools.com/sql/sql_insert.asp)
