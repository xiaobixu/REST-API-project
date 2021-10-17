#Import necessary libraries
import requests
import json

import tkinter as tk
from tkinter import filedialog, Text
import os

#Define variable to hold the results
results ={}

#Define the function to retrieve each repository's contributor counts, given the owner's name
def get_contributor(owner,git_user,git_token):
    url = "https://api.github.com/users/{username}/repos".format(username =owner)
    response = requests.get(url, auth=(git_user,git_token))
    repos = response.json()
    #If there are multiple pages in the respons, iterate through the links
    while 'next' in response.links.keys():
        response = requests.get(response.links['next']['url'], auth=(git_user,git_token))
        repos.extend(response.json()) #Append the page to the previous one
    repo_contributors = {} #Create dictionary to hold repository and its contributor counts
    #Read the contributor from each repo, and store the number under each repo name
    for item in repos:
        contri_url = item["contributors_url"] #Get the url to the contributors' information
        contributors = requests.get(contri_url,auth=(git_user,git_token)).json()
        repo_contributors[item['name']] = len(contributors)
    return repo_contributors

def myClick():
    T.delete("1.0", tk.END) #Clear the previous results 
    results = get_contributor(entry_owner.get(),entry_user.get(),entry_token.get())
    result = results.items()
    T.insert(tk.INSERT, "Contributor count for each repository:\n")
    for item in result:
        T.insert(tk.INSERT, "{repo} : {number}\n".format(repo=item[0],number=item[1]))
    T.insert(tk.END, "That is all!")
    
window = tk.Tk()
window.title("Welcome to GitHub Repository Analysis app!")

#Create label and entry widget for owner input
lbl1 =tk.Label(window, text="Enter the owner name that you are interested (e.g. PowerShell):")
lbl1.pack()

entry_owner = tk.Entry(window, fg="black", bg="white", width=30)
entry_owner.pack()

#Create label and entry widget for authentication token
lbl2 =tk.Label(window, text="Enter the username of your own GitHub username:")
lbl2.pack()

entry_user = tk.Entry(window, fg="black", bg="white", width=30)
entry_user.pack()

#Create label and entry widget for username input for authentication use
lbl3 =tk.Label(window, text="Enter your own token key:")
lbl3.pack() 

entry_token = tk.Entry(window, fg="black", bg="white", width=100)
entry_token.pack()

#Create button widget and define size and action
btn = tk.Button(window, text="Search", padx=10, pady=5, fg="white", command=myClick)
btn.pack()

#Create text widget and specify size
T = tk.Text(window, height=50, width=50,bg="#263D42")
T.pack()

window.mainloop()