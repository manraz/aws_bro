# Filtering log files
The code will filter bro log files and output to html with the help o flask. It will output most used ip, geolocation, vendor names...
## awsbrofilter
$ sudo apt update

$ sudo apt install apache2

$ sudo apt-get install apache2 libapache2-mod-wsgi-py3

$ sudo apt-get install python3-pip

$ pip3 install virtualenv

**Inside directory aws_bro where the app is:**

$ virtualenv venv

**Activate the virtual environment**

$ . venv/bin/activate 

*Use pip to install flask or use*

$ pip install -r requirements.txt

**After installing apache2 server the 000-default.conf file needs to be configured:**

    WSGIDaemonProcess aws_bro threads=5
    WSGIScriptAlias / /var/www/html/aws_bro/app.wsgi
    WSGIProcessGroup aws_bro
    WSGIApplicationGroup %{GLOBAL}
    <Directory aws_bro>
      Order deny,allow
      Allow from all
    </Directory>
  
**Also my 000-default.conf looks like:**

    <VirtualHost *:80>

          # The ServerName directive sets the request scheme, hostname and port that
          # the server uses to identify itself. This is used when creating
          # redirection URLs. In the context of virtual hosts, the ServerName
          # specifies what hostname must appear in the request's Host: header to
          # match this virtual host. For the default virtual host (this file) this
          # value is not decisive as it is used as a last resort host regardless.
          # However, you must set it for any further virtual host explicitly.
          ServerName x.x.x.x
          ServerAdmin webmaster@localhost
          
          DocumentRoot /var/www/html
          WSGIDaemonProcess aws_bro threads=5
          WSGIProcessGroup aws_bro
          WSGIScriptAlias / /var/www/html/aws_bro/app.wsgi        
          <Directory /var/www/html/aws_bro/>
                  Order allow,deny
                  Allow from all
          </Directory>
          
        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
    </VirtualHost>

**Create a link so your app appears in /var/www/html/ :**

$ sudo ln -sT ~/aws_bro /var/www/html/aws_bro

$ sudo a2enmod wsgi

**Also restart apache after al settings**

$ sudo apache2ctl restart

**Use error.log file to debbug**

nano /var/log/apache2/error.log

**To clear the error.log use:**

sudo bash -c 'echo > /var/log/apache2/error.log'
