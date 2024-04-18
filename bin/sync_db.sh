sudo rsync -avz -e "ssh -i /home/peanut/aws_keys/aws-key-ymd-app.pem" --rsync-path="sudo rsync" * ubuntu@ec2-52-14-0-128.us-east-2.compute.amazonaws.com:~/ymd-rag/backend/data/weaviate_data/
