Wordle REST implementation in Python.

**Technologies used:**
Built with Flask, Dynamodb. Built image using Docker and uploaded to an ECR repository.  Deployed to a AWS EC2 instance.

Nginx proxying used to expose endpoint

OpenAPI used for documenting endpoints

Postman used for testing

**Database**
Found 10,000 most common english words and processed used NLTK (Natural Language Processing) to remove plurals
Ran a batch write job to update DynamoDB

![image](https://github.com/alexchung1233/Wordle-Python/assets/39063219/838ef823-e7aa-4838-9834-8dc1f58d18c3)
