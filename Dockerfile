FROM ruby:latest
RUN gem install jekyll bundler
COPY blog /blog/
RUN cd blog \
         && bundler install 
WORKDIR /blog
CMD jekyll serve