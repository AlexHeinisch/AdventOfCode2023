# Advent of Code 2023 Journey

This repo will contain all my solutions to the 2023 advent of code!

## Folder Structure

Each day contains the solution to each challenge within a single python (hopefully I won't need a more complex structure), a README explaining the challenge which is directly copied from the official homepage, and a resource folder ('res') containign various input files.

## Setup

I am running poetry to manage packages needed for the challenges (tough I hope I won't be needing too many). To install the packages, first of all install poetry ´pip install poetry´. Afterwards, go to the root directory of the repository and run ´poetry install´ and afterwards ´poetry env use <your python>´ to activate the environment containing the installed packages.

## Running the Challenges

I am using the ´typer´ package to create beautiful/clean CLI programs. To run the solutions simply execute them by running the main python file. You will get info on the avaible commands there! Usually I will upload the sample and challenge inputs and provide a command to automatically process them.