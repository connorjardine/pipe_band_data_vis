# pipe_band_data_vis
Repository for my Pipe Band data visualisations. All data is taken from RSPBA contest summaries from 2003-2018.

current state of the application can be found at www.pipebanddata.uk

Please note that it is currently in a work in progress state. Some bugs may persist.

# Technology

The project is built around a NoSQL Cloud MongoDB Database. Flask and Python is used as middleware.

# Installation

1. Clone the app.
2. Set up a Python Virtual Environment (https://docs.python.org/3/tutorial/venv.html)
3. Activate the Virtual Environment
'''<your-env>\Scripts\activate''' on windows, or '''source tutorial-env/bin/activate''' on Mac/Linux
4. Pip install requirements.txt using:
'''pip install -r requirements.txt'''
5.). On Windows:
  '''set FLASK_APP=app.py'''
  '''set FLASK_ENV=development'''
  or linux:
  '''export FLASK_APP=app.py'''
  '''export FLASK_ENV=development'''
  then finally, '''flask run'''

6. Navigate to (http://127.0.0.1:5000/)
  
  
