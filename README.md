# REST-API-project
Create a mini desktop app using Github REST API(https://docs.github.com/en/rest) to retrieve the contributor counts for each repositories, given the owner usernames. Repository names are sorted by contributor counts in descending order.

In order to run the application sucessfully, please install the necessary packages/libraries in requirements.txt. It is recommended to run the app in virtual environment to isolate the dependencies from others, you can run:
> python3 -m venv .venv
> 
> source .venv/bin/activate #Activate the virtual environment
> 
> pip3 install [package]

*Note: Sometimes the tkinter could not work while installed via pip3. In my case, I have to install it via other tools.I am working on iMac,and I install tkinter via brew (brew install python3-tk). See: https://stackoverflow.com/questions/4783810/install-tkinter-for-python

To run the app:
> python application.py

To exit the virtual environment:
> Deactivate
