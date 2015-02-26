## To install Pycogent there are some requirements, these were the steps I took:

# installed zlib (it is a data-compression library for use on virtually any computer hardware and operating system)
sudo apt-get install zlib1g-dev zlib1g

# installed the easy_install (a program to install programs)
sudo apt-get install python-setuptools

# Install SQLAlchemy (the Python SQL toolkit, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language, http://www.sqlalchemy.org/)
sudo easy_install SQLAlchemy

# Install MySQL-python (MySQL database connector for Python programming, program that allow you to explore MySQL databases in python)
sudo apt-get install python-mysqldb

# Install MySQL (https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-14-04):
sudo apt-get install mysql-server
sudo mysql_install_db

#Install PyCogent (http://pycogent.org/install.html#quick-install):
wget http://pycogent.org/_downloads/cogent-requirements.txt 
echo "MySQL-python>=1.2.2" >> cogent-requirements.txt
echo "SQLAlchemy>=0.5" >> cogent-requirements.txt
#or: printf "\nMySQL-python>=1.2.2\nSQLAlchemy>=0.5" >> cogent-requirements.txt
sudo easy_install -U pip
DONT_USE_PYREX=1 sudo pip install -r /home/gabriela/Downloads/cogent-requirements.txt

# obs: SQL is the format of the database and MySQL is the program to access it

## done!
