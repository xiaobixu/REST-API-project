#Import necessary libraries
import requests
import json

import tkinter as tk
from tkinter import filedialog, Text
import threading as Tr

# Sorting dictionary by contributor counts in descending order
def sort_dic(dic):
    # Sort the dictionary by values in descending order
    sorted_dic = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_dic

class GetContributors():

    #Initiate
    def __init__(self):
        # Create main window and the title
        self.window = tk.Tk()
        self.window.title("Welcome to GitHub Repository Analysis app!")

        # Create label and entry widget for owner input
        self.lbl1 = tk.Label(self.window, text="Enter the owner name that you are interested (e.g. PowerShell):")
        self.lbl1.grid(row=0, column=0)

        self.entry_owner = tk.Entry(self.window, fg="black", bg="white", width=80)
        self.entry_owner.grid(row=0, column=1)

        # Create label and entry widget for authentication token
        self.lbl2 = tk.Label(self.window, text="Enter your own GitHub username for authentication:")
        self.lbl2.grid(row=1, column=0)

        self.entry_user = tk.Entry(self.window, fg="black", bg="white", width=80)
        self.entry_user.grid(row=1, column=1)

        # Create label and entry widget for username input for authentication use
        self.lbl3 = tk.Label(self.window, text="Enter your own git token key:")
        self.lbl3.grid(row=2, column=0)

        self.entry_token = tk.Entry(self.window, fg="black", bg="white", width=80)
        self.entry_token.grid(row=2, column=1)

        # Create Search button widget and define size and action
        self.btn = tk.Button(self.window, text="Search", padx=10, pady=5, fg="white", command=self.threading)
        self.btn.grid(row=3, column=0)

        # Create label to show the processing status
        self.lbl4 = tk.Label(self.window, width=50, text="Status", bg="light blue")
        self.lbl4.grid(row=3, column=1)

        # Create text widget and specify size
        self.T = tk.Text(self.window, height=50, width=100, bg="#263D42", fg="white")
        self.T.grid(row=4, columnspan=2)

        self.window.mainloop()

    # Define the function to retrieve each repository's contributor counts, given the owner's name
    def get_contributor(self, owner, git_user, git_token):
        url = "https://api.github.com/users/{username}/repos".format(username=owner)
        response = requests.get(url, auth=(git_user, git_token))
        repos = response.json()
        # If there are multiple pages in the respons, iterate through the links
        while 'next' in response.links.keys():
            response = requests.get(response.links['next']['url'], auth=(git_user, git_token))
            repos.extend(response.json())  # Append the page to the previous one
        repo_contributors = {}  # Create dictionary to hold repository and its contributor counts
        # Read the contributor from each repo, and store the number under each repo name
        for item in repos:
            contri_url = item["contributors_url"]  # Get the url to the contributors' information
            contributors = requests.get(contri_url, auth=(git_user, git_token)).json()
            repo_contributors[item['name']] = len(contributors)
        sorted_repos = sort_dic(repo_contributors)
        return sorted_repos

    def threading(self):
        t1 = Tr.Thread(target=self.myClick)
        t1.start()

    def myClick(self):
        self.T.delete("1.0", tk.END) #Clear the previous results
        self.lbl4.config(text = "Processing")
        self.T.insert(tk.INSERT, "Processing... Please wait :)") #Adding waiting status
        results = self.get_contributor(self.entry_owner.get(),self.entry_user.get(),self.entry_token.get())
        self.T.delete("1.0", tk.END) #Clear the waiting status
        self.T.insert(tk.INSERT, "Contributor count for each repository (sorted in descending order by contributor counts:\n")
        for i in results:
            self.T.insert(tk.INSERT, "{repo} : {number}\n".format(repo=i[0],number=i[1]))
        self.lbl4.config(text = "Done!")

if __name__ == "__main__":
    GetContributors()

