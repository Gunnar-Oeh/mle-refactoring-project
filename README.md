# Refactoring Project

Please do not fork this repository, but use this repository as a template for your refactoring project. Make Pull Requests to your own repository even if you work alone and mark the checkboxes with an `x`, if you are done with a topic in the pull request message.

## Project for today

The task for today you can find in the [project-for-today.md](./project-for-today.md) file.

## Questions:

1. What are the steps you took to complete the project?
    - Cleaned up [King County Notebook](./King_County.ipynb) from unneeded Code to keep only the commands of the Data-Cleaning process. Result in [King_County_refactoring.ipynb](./King_County_refactoring.ipynb)
    - Created [data_cleaning_functions.py](./src/data_cleaning_functions.py) where Data-Cleaning steps are defined as functions.
    - Tested these in [test_functions.ipynb](./test_functions.ipynb) (no unit testing) to at least remove syntax and name errors.
    -  Created [custom_transformers.py](./src/custom_transformers.py) where Data-Cleaning steps are defined as classes inherited from sklearns BaseEstimator and TransformerMixin
    -  Created [data_cleaning_pipeline.py](./src/data_cleaning_pipeline.py) where classes from [custom_transformers.py](./src/custom_transformers.py) are combined into an sklearn-Pipeline using Pipeline() and CustomTransformer().
    - Tested these in [test_pipeline.ipynb](./test_pipeline.ipynb) (no unit testing) to at least remove syntax and name errors. Unclear wether the pipeline works as expected.
2. What are the challenges you faced?
  - defining Transformers where the fit method was actually needed and values needed to be stored for .transform()
  - Constructing the Pipeline with the Imputing of a few columns taking Place before the transforming of all columns. Could not have worked
  - Finding Syntax and Naming Errors in [data_cleaning_pipeline.py](./src/data_cleaning_pipeline.py) and [custom_transformers.py](./src/custom_transformers.py) to get the pipeline to run at least without errors
3. What would you do differently if you had more time?
  - Include actual functions for spatial data handling and calculations to use for the functions which calculated distances.
  - Unit Test the Transformers to check wether these return the expected results


## Setup

The necessary libraries are listed in the [requirements.txt](./requirements.txt) file. You can install them with the following command:

```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
