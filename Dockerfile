FROM python:latest


# Install python stuff

RUN \
    python3 -mpip install --upgrade pip && \
    python3 -mpip install virtualenv

RUN \
    virtualenv proteins  && \
    ls && \
    ls proteins/bin && \
    . ./proteins/bin/activate

RUN \
    python3 -mpip install cython && \
    python3 -mpip install pybind11 wheel


RUN \
    python3 -mpip install numpy  && \
    python3 -mpip install pyarrow && \
    python3 -m pip install --upgrade Pillow && \
    python3 -mpip install pandas altair matplotlib


RUN \
    python3 -mpip install streamlit
