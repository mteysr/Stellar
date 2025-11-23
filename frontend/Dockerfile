FROM nginx:alpine

# Copy website files
COPY index.html /usr/share/nginx/html/
COPY debug.html /usr/share/nginx/html/
COPY extension-check.html /usr/share/nginx/html/
COPY freighter-fix.html /usr/share/nginx/html/
COPY manual-test.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
