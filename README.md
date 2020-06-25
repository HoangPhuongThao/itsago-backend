# itsago-backend
This is a backend for Itsago app - Luggage checking using Flask Python.

**How to run the backend:**
1. To clone this repository go to the file where you want to have this project saved and write this command:
```git clone https://github.com/HoangPhuongThao/itsago-backend.git``` 

2. Now install all the packages needed for this project with command:
```pip install -r requirements.txt```.
If you don't have pip, install it first.

3. Run this code for the first time using NLTK library
```
import nltk
import ssl

try:
     _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
```

4. Run the script:
```python app.py```

5. This is only the backend of the ITSAGO application, the frontend also has to be run to get the full functionality. Link to frontend: 
ttps://github.com/jorensjongers/itsago-frontend
