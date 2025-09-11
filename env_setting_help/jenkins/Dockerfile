FROM jenkins/jenkins

USER root

RUN apt update && apt install -y  python3 python3-pip python3-pytest
RUN apt install -y python3-selenium pipx
RUN pipx install selenium --include-deps 
RUN pip install allure-pytest --break-system-packages  
RUN pip install pytest-xdist --break-system-packages
RUN pip install requests --break-system-packages
USER jenkins
