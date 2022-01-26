FROM ubuntu:20.04

# If you would rather work from inside a docker container, this should get you going.
#
# Build:
# docker build --tag apod .
# 
# Run
# docker run  --rm -it -p "8000:8000" apod
# 
# Or mount this directory for local editing goodness:
# docker run  --rm --interactive --tty --publish "8000:8000" --mount type=bind,source=`pwd`,target=/opt/outside apod
#
# When you runserver inside the container, be sure to listen on 0.0.0.0:8000, and not just 127.0.0.1.


RUN apt update && apt upgrade --yes
RUN DEBIAN_FRONTEND="noninteractive" TZ="Etc/UTC" apt install --yes tzdata
RUN apt install --yes \
    dumb-init \
    tzdata \
    python3.9 \
    python3-pip


RUN mkdir /opt/outside
WORKDIR /opt/outside

# Copy in requirements and just enough project to install into the python environment.
COPY requirements.txt .
COPY src/setup.py src/setup.py
COPY src/outside/__init__.py src/outside/__init.py
RUN pip install -r requirements.txt

# Then copy over the rest of the code.
COPY . .


# Move everything off of PID 1.
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Default to a bash shell.
CMD ["/bin/bash"]
