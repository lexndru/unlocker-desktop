FROM ubuntu:14.04

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
# https://github.com/docker-library/python/issues/147
ENV PYTHONIOENCODING UTF-8

# install requirements
RUN apt-get update && apt-get install -y software-properties-common python-software-properties && \
	add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe" && \
	add-apt-repository -y ppa:adamwolf/kicad-trusty-backports && \
	apt-get update && \
	apt-get install -y build-essential libwxgtk3.0-dev python python-dev \
						python-pip python-virtualenv python-gdbm \
						python-wxgtk3.0 python-wxgtk3.0-dev xvfb \
						&& \
	rm -rf /var/lib/apt/lists/*

# install unlocker and initialize
RUN pip install flake8 unlocker && unlocker init && unlocker install

# run in debug mode
ENV DEBUG true

CMD ["/bin/bash"]
