aws ecr get-login-password --region us-east-2 | sudo docker login --username AWS --password-stdin 654654539021.dkr.ecr.us-east-2.amazonaws.com
sudo docker build -t 654654539021.dkr.ecr.us-east-2.amazonaws.com/wordle-repo:latest .
sudo docker push 654654539021.dkr.ecr.us-east-2.amazonaws.com/wordle-repo:latest


