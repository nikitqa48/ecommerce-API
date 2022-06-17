FROM postgres:11.5-alpine
COPY init.sql /app/init.sql/
RUN  chmod +x /app/init.sql/