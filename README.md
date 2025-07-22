Translation-Agenda
This repository serves as a hub for projects related to Translation Tools and Automation. It currently contains two main projects:

Translation Agenda (Original Project)

HP Translations (New Project)

1. Translation Agenda (Original Project)
Overview
The original "Translation Agenda" project was developed to generate a translation memory within a browser environment. It offered a web-based interface to manage and visualize translation segments, facilitating the creation and consultation of terminology or translation databases directly in the browser.

Key Features (Examples)
Creation and editing of translation memory entries.

Searching and filtering of translated segments.

Exporting translation memories in common formats.

2. HP Translations (New Project)
Overview
The HP Translations project is a new addition to this repository, focusing on automation and file preparation for localization projects, specifically for Trados Studio, by leveraging the iFixit API.

It contains a set of scripts designed to optimize the translation workflow for technical content, such as HP product documentation, which can be found on the iFixit platform. The primary goal is to automate the process of obtaining and processing JSON files, transforming them into a format ready for work in CAT (Computer-Assisted Translation) tools like Trados Studio.

What the Scripts Do (Key Functionalities)
Inside the HP Translations/ folder, you'll find scripts with the following functionalities:

Download JSON Files via iFixit API: Scripts to programmatically access the iFixit API and download JSON files containing product data (e.g., manuals, repair guides, specifications) relevant to translation projects.

JSON Cleanup/Preprocessing: Automations to process the downloaded JSON files. This includes:

Content Filtering: Removing irrelevant or redundant data that does not need to be translated.

Extracting Translatable Text: Isolating the actual translatable text from the JSON structure and fields.

Data Normalization: Standardizing formats and structures to ensure consistency.

Preparation for Trados Studio: The ultimate goal is to transform the pre-processed JSON data into a format (such as segmented TXT files, or even a simplified intermediate format like XLIFF/XML, depending on your implementation) that can be easily imported into Trados Studio, allowing for efficient and consistent translation.

Purpose
This project aims to reduce the manual time and effort in preparing high-volume translation projects, especially those involving semi-structured data from APIs. By automating the download and preprocessing, translators can focus more on translation quality and less on the file engineering stage.

