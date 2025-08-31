# create a webserver
# 1. use an fedora base image
# 2. install webserver: dnf -y install httpd
# 3. copy the tar file and extract in the relevant path: 
#    ADD website.tar.gz /var/www/html/
# 4. Start the webserver: 
#     CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
# 5. pass in parameters to the webserver: 
#     EXPOSE "-D" and "FOREGROUND"
# 6. call the image challenge2
# 7. run on port 80


FROM fedora:latest
RUN dnf -y install httpd
ADD webserver.tar.gz /var/www/html/
CMD ["-D", "FOREGROUND"]
ENTRYPOINT [ "/usr/sbin/httpd" ]
EXPOSE 80
# docker build -t challenge2 .
# docker run -d -p 80:80 challenge2
