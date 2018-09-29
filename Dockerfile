FROM ubuntu:14.04

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
# https://github.com/docker-library/python/issues/147
ENV PYTHONIOENCODING UTF-8

# install requirements
RUN apt-get update && \
	apt-get install -y python python-dev python-pip python-virtualenv python-gdbm && \
	rm -rf /var/lib/apt/lists/* \
	apt-get install build-essentials python-wxgtk3 python-wxgtk3.0-dev

# install unlocker and initialize
RUN pip install flake8 unlocker && unlocker init && unlocker install

# run in debug mode
ENV DEBUG true

CMD ["/bin/bash"]
