# 0. Use python:latest as base image
FROM python:latest

# Set working directory
WORKDIR /root

# 1. Clone the repository
RUN git clone https://github.com/abetlen/llama-cpp-python.git

# Navigate into the cloned repository
WORKDIR /root/llama-cpp-python

# 2. Checkout to the latest commit
RUN git checkout 7403e002b8e033c0a34e93fba2b311e2118487fe

# 3. Clone git submodules recursively
RUN git submodule update --init --recursive

# 4. Install the package
RUN pip install .

# 5. Copy gen.py to /root
COPY gen.py /root/

# Set working directory back to /root
WORKDIR /root

# 6. Run gen.py when the container is started
CMD ["python", "gen.py"]
