# simple-survey-builder
 Lightweight text-based python project to build and run methodological surveys or systematic reviews.
 
 This is a command-line text-based tool in order to streamline workflows for methodological (or other) surveys. Run *run_survey.py* to see a demo survey with sample data and a simple configuration.

### Quickstart
1. **Generate the inventory**- This is the list of files that is to be surveyed. All PDF files should be in a folder called sample-data, then the *generate_inventory_py* file can be used to generate *inventory.csv*
2. **Set up survey configuration**- change the dictionary in *config.py* to contain the question prompts, labels, and validation dictionaries. Validation dictionaries have keys with the standardized answers to the survey, and values with possible variants on those responses for the input. Questions can also be assigned numeric levels (where 0 is the highest level) in cases where it might be desirable to include multiple entries for a single pdf with partially overlapping information.
3. **Run the survey**- Use *run_survey.py* to set up (first time) or continue running the survey. This can be run in a program or directly in the IDE. Either way, it will automatically open the file and use text prompts to guide you through the survey questions.
4. **Export results**- Use *export_survey.py* in order to output the results of the survey as a .csv file for further analysis. 


