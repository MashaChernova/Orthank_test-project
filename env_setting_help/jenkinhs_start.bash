#bash/bin

sudo docker run -d -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home_2:/var/jenkins_home myjenkins6


$ docker run --rm --entrypoint=cat jodogne/orthanc:1.12.9 /etc/orthanc/orthanc.json > /tmp/orthanc.json



