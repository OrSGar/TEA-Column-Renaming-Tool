<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<p align="center">
    <a href="https://tea.texas.gov/">
        <img src="README_Resources/TEA_Logo.png" alt="Logo" width="180" height="90">
    </a>

<h3 align="center">TEA Column Renaming Tool</h3>

<p align="center">
        Renaming tool for Texas Education Agency Public Datasets
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#project-background">Project Background</a>
      <ul>
        <li><a href="#project-inception">Inception</a></li>
        <li><a href="#about-the-project">About</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#using-the-tool">Using the Tool</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Project Background

### Project Inception 
For my groups capstone project with [Correlation One's](https://www.correlation-one.com/) [DS4A](https://www.correlation-one.com/data-science-for-all-empowerment) training program, we decided
to analyze the effect of COVID-19 on Round Rock ISD students. Through our data analysis of student performance metrics in a variety of teaching formats (in person, hybrid, etc) we would have provided suggestions
to the school district on what they can do to help improve student academic performances.

Since the Texas Education Agency created their information management system in 1980, the data they have gathered across 1,200 districts and charters in Texas have been 
available to the public. To learn more about TEA and their datasets, visit their reports and data homepage: [TEA Reports](https://tea.texas.gov/reports-and-data)

A common issue we found when collecting data from TEA were the names of the dataset columns. An example of a column from a dataset is shown below:

![columns-screenshot]

Before proceeding with analysis, we needed to convert these columns to their respective `key:value` mappings across a variety of datasets. For one file alone this 
could be feasible simply by referencing the descriptions provided by TEA after each download (shown below).

![reference-screenshot]

![reference-website]

Since the team planned to use several datasets with different attributes across different school years, doing this by hand for each dataset would prove to be tedious. 
To speed up the data gathering phase, I decided to build this tool that could be used by each team member for datasets they downloaded from TEA. 

Some requirements going into the project were as follows:

* In a format everyone was familiar with for usability
* Powerful enough to be used in a variety of use cases 
* Can be incorporated into any data analysis notebook

### About the Project

For the implementation, I decided a web scraper would be the best in this situation. Since every variable description website is in the same format, it only made sense
to scrape the mappings and convert them to JSON. 

Correlation One's DS4A program provides data analysis training for people that come from a variety of backgrounds, including non-technical ones. With this in mind, I decided to take an 
object-oriented approach to the tools source code. This helped with abstraction and decomposition of the tool to help me during development and to help the user not worry about
how it works. 

The tool works in 3 major steps:
1. The user defines the variables they want to use (dataset reference link, and replacement words)
2. User define website is scraped to get the descriptions and saves the results to JSON format in the local directory `Generated Keys`.
3. Users are able to replace words in the descriptions to shorten the length of the column name (removing redundant words, changing genders to their short versions)
4. The new processed JSON keys are stored in local directory `Processed Keys`.

The source code for the project can be found in the [`KeyProcessor.py`](https://github.com/OrSGar/TEA-Column-Key-Converter-/blob/main/KeyProcessor.py) file. 

### Built With
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

<!-- GETTING STARTED -->
## Using the Tool

To use the tool, I suggest downloading the [`KeyProcessor.py`](https://github.com/OrSGar/TEA-Column-Key-Converter-/blob/main/KeyProcessor.py) and [`KeyConverterTool.pynb`](https://github.com/OrSGar/TEA-Column-Key-Converter/blob/main/Key%20Converter%20Tool.ipynb) files. 

### Prerequisites

* Python 3.9 (version I used, not sure if it works with other versions)
* Jupyter Notebook
* BeautifulSoup4 package

<!-- USAGE EXAMPLES -->
## Usage

A usage example can be found within the Converter Tool Example.pynb

<!-- CONTACT -->
## Contact

For any questions, suggestions, or issues regarding this tool please feel free to reach out to me directly;

Orlando Garcia - orlando.s.gar@gmail.com

Project Link: [https://github.com/OrSGar/TEA-Column-Key-Converter](https://github.com/OrSGar/TEA-Column-Renaming-Tool)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements 

Special thanks to [othneildrew](https://github.com/othneildrew) and his README [template](https://github.com/othneildrew/Best-README-Template). 

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[columns-screenshot]: README_Resources/columns_original.JPG
[reference-screenshot]: README_Resources/reference_screenshot.png
[reference-website]: README_Resources/reference_website.JPG
[ds4a]: https://www.correlation-one.com/data-science-for-all-empowerment
[tea-data-statement]: https://tea.texas.gov/reports-and-data
[key-processor]: https://github.com/OrSGar/TEA-Column-Key-Converter-/blob/main/KeyProcessor.py