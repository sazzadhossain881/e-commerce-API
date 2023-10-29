Project Name: e-commerce api

App name: core

Project Description:

###Backend:

1.A user can login and registration.

2.admin can add update and delete product.

3.user can see product feature and description.


Project Features:

I have dockerize python(django) application for this project and installed the required packages, which i have shared in

requirements.txt file.

I have used Django Rest Framework for creating the API's.

I have used Postgresql database for this project.

I have used Django ORM for database operations.

I have used Django Admin for creating the admin panel.

I have used Django Serializer for creating the serializers.

I have used Django Rest Framework Spectacular for creating the API documentation.

I have used PyJWT for creating the token based authentication.

I have used Pytest for creating the tests.

I have used Postman for testing the API's.

Steps to run the project:

1.Clone the project from the git repository. Even you can download the zip file from the git repository. (For your ease: I have

included .env file)

git clone https://github.com/sazzadhossain881/e-commerce-API.git

4.Run the following commands:

1. <pre>docker build .</pre>

2. <pre>docker-compose build</pre>

3. <pre>docker-compose run --rm app sh -c "python manage.py makemigrations"</pre>

4. <pre>docker-compose run --rm app sh -c "python manage.py migrate"</pre>

5. <pre>docker-compose run --rm app sh -c "python manage.py createsuperuser"</pre>

6. <pre>docker-compose up</pre>

Now, you have to authenticate yourself before doing any operation. To do that, hit the login endpoint and pass the email and password in the body. You will get a  token in the response. Copy token and paste it in the authorize section of ModHeader Extensions. Now, you can perform any operation.

url: http://127.0.0.1:8000/api/users/login

You can also see the admin dashboard using the following url:

url: http://127.0.0.1:8000/admin/

You can also run the tests using the following command:

docker-compose run --rm app sh -c "python manage.py test"

Database Schema:

This implementation has 3 main models: Product, Category and Stock.

Product stores information about the product name, price, brand etc.

Category stores information about the product category name like phone, laptop.

Stock stores the information about how much product are available.
