Translation-Agenda
This repository serves as a hub for projects related to Translation Tools and Automation. It currently contains two main projects:

        * Translation Agenda (Original Project)

        * HP Translations (New Project)
***
1. Translation Agenda (Original Project)
Overview
The "Translation Agenda" is a browser-based tool designed to function as a lightweight translation memory (TM) and terminology management system. It provides a simple web interface for users to create, store, edit, search, and manage translation segments directly within their browser. This project is ideal for quick reference, personal glossaries, or small-scale TM needs, offering immediate access to linguistic data without external software.

Core Functionalities (Powered by app.js)
The app.js JavaScript file drives the interactive functionalities of this project:

        * Segment Management (CRUD Operations): Allows users to Create new translation entries (Title, Original Text, Translation), Read all stored entries, Update existing entries (by populating input fields for editing), and Delete unwanted segments.

        * Local Storage Persistence: All translation data is automatically saved and retrieved from the browser's local storage. This ensures that entries persist across browser sessions, providing continuous access to the user's custom translation memory.

        * Dynamic Search & Filtering: Features a real-time search functionality that filters translation segments based on keywords in the title, original text, or translation. Results are dynamically displayed on the page.

        * Interactive User Interface: Handles form submissions, button clicks (edit, delete), and updates the display of translation results without requiring page reloads, providing a smooth user experience.
***
2. HP Translations (New Project)
Overview
The HP Translations project is a new addition to this Translation-Agenda repository, focusing on automation and file preparation for localization projects, specifically for Trados Studio, by leveraging the iFixit API.

It contains a set of Python scripts designed to significantly streamline the translation workflow for technical content, such as HP product documentation, often found on the iFixit platform. The primary goal is to automate the entire process of obtaining, meticulously filtering, and extracting translatable text from complex, nested JSON structures, transforming them into a clean, ready-to-translate format for CAT tools like Trados Studio.

Evolution of the Scripts
This project has undergone an iterative development process, with each script version refining the data extraction and preparation for Trados Studio. This evolution highlights a methodical approach to solving challenges posed by API data and specific translation requirements:

        * Initial Versions (download.py, downloadDevicePage.py, download_guide_from_ids_guias_wo_prereqs.py):

                * Focus: Early scripts managed the initial downloading of guide and device page JSON data from the iFixit API.

                * Refinement: These versions progressively improved by, for instance, filtering out "prerequisites guides" which often contained duplicate or irrelevant content for translation, thereby making the initial text output cleaner (.txt format).

        * Current Core Script (download_extract_guides_slim.py): This is the most refined version, orchestrating intelligent fetching and precise content preparation. Building on lessons learned from previous iterations, this script provides the most accurate and Trados-ready output by:

                * Batch JSON Guide Download via iFixit API:

                    * Reads a list of unique guide_ids from a specified ids_guias.txt file.

                    * Programmatically fetches the full, raw JSON data for each guide from the iFixit API (https://www.ifixit.com/api/2.0/guides/) using the requests library.

                    * Includes robust error handling for network issues, invalid API responses, and JSON decoding errors.

                    * Features a resume capability, skipping guides for which a .txt output file already exists, enabling efficient re-runs for large batches.

                * Advanced Recursive Text Extraction & Filtering:

                    * Employs a sophisticated recursive function to navigate through highly nested and varied JSON structures.

                    * Intelligently filters out non-translatable metadata: Utilizes extensive exclusion lists for JSON keys (e.g., id, guid, thumbnail, image dimensions, rendered keys, specific prerequisites blocks, flags, revision, url, type, keywords, etc.). This ensures only relevant, translatable strings are captured.

                    * Elimination of Duplicate and Irrelevant Content: Crucially, this version specifically addresses and removes undesired double content and data not visible in the iFixit.com Guide View's translation interface, ensuring translators work only with the necessary and visible text.

                    * Preserves Original Content Fidelity: Unlike some processors that might strip HTML/Markdown, this script extracts the raw text content, including any embedded formatting (HTML or Markdown), ensuring the translator receives the full context for accurate rendering in Trados Studio.

                * Clean, Trados-Ready Text Output:

                    * Consolidates all extracted and filtered translatable strings from each guide into a single, dedicated .txt file (e.g., trados_guide_XXXX.txt).

                    * Each extracted segment is separated by a double newline (\n\n), creating distinct paragraphs or segments that are ideal for import and segmentation within Trados Studio or other CAT tools, minimizing pre-segmentation effort.

Purpose
This project dramatically reduces the manual time, tedious effort, and potential for human error typically involved in preparing large-volume technical translation projects, especially those originating from semi-structured API data. By automating the fetching, precise filtering, and text extraction, this solution empowers translators to focus more on the linguistic quality and nuance of the translation itself, rather than on cumbersome file engineering, data cleanup, or manual copy-pasting.
***
How to Navigate This Repository
        * Access the Translation-Agenda/ folder to explore the original translation memory project.

        * Access the HP Translations/ folder to find the iFixit automation scripts for Trados Studio.
***
Setup and Environment
To run the HP Translations Python scripts, ensure you have the following environment configured:

        * Python Version: The scripts are developed and tested with Python 3.8 or newer. It's highly recommended to use a recent stable version of Python 3.

        * Required Libraries: The scripts rely on the requests library for making HTTP requests to the iFixit API.

                * You can install this library using pip, Python's package installer:

                Bash

                pip install requests
                * Virtual Environment (Recommended): For best practices, it's advisable to set up a virtual environment to manage dependencies for your project. This prevents conflicts with other Python projects on your system.

                Bash

                python3 -m venv venv        # Create a virtual environment named 'venv'
                source venv/bin/activate    # Activate the virtual environment (Linux/macOS)
                # For Windows (Command Prompt): venv\Scripts\activate.bat
                # For Windows (PowerShell): venv\Scripts\Activate.ps1
                pip install requests        # Install dependencies within the active environment
                Remember to activate the virtual environment (source venv/bin/activate) each time you work on the project in a new terminal session.


***
Author
Udo Antonio Baingo

