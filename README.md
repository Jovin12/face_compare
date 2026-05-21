

## Setup
``` 
pip install streamlit opencv-python deepface pillow numpy
```

## USAGE
Use this if you are only hosting a single app with all the necessary functionalities
``` 
streamlit run streamlit_app.py
```

Version2: Version 2 is setup such that it is not a single file. \
The hierachy is diveded as streamlit_app_Version2 -- Is only the ui for the frontend
Backend -- Calls the comprea-faces, crop_license and take_img. 

The reson for this split, it is setup such that, you can use the backend python files as a standalone and only change the fronend ui, instead of streamlit. 

```
streamlit run .\streamlit_app_Version2.py
```

## Results
![alt text](image.png)