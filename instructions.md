# Instructions

* Use Python
* Provide comments about your decision process - Why have you chosen your approach? We are more interested in your thought process than the best possible result.
* Properly document your code.
* The output of the task should be a zip file containing the .py or .ipynb files allowing full reproducibility of your results.
* Send output to the same e-mail you have received this assignment from.

# Git task

1. Write a Python script which utilizes githubs api - https://api.github.com/events.

    * The function/class takes GitHub repo url, GitHub API key and offset value, which determines the amount of minutes of git history on the input we are interested in.
    * Use only following events: PushEvent , PullRequestEvent, IssueCommentEvent, WatchEvent
    * Required functionality:

        * a) Count number of events by their type.
        * b) Calculate average time between 2 consecutive events of the same type
        * c) Visualize number of events per type through time.
        * d) Calculate the average length of commit messages.

    * Outputs of individual functionalities above (a - d) should be returned in a markdown file
        * Be sure to include visualization from c)
    * Provide proper documentation of your code and use git during development process.

2. Using your tool developed in the 1st step, analyze `pandas` git repo 20 day history and comment on the results.
