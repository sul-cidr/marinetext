Command line script to parse plain text files and write a csv file that identifies marine species within each file.

## Install

Create a virtual environment and run:

`pip install -r requirements.txt`

## Run

Make sure that all plain text files are in one directory.

```Usage: ent_cli.py [OPTIONS]

  Small program to extract sets of named entities from texts
  based on a defined dictionary.

Options:
  --taxon_file TEXT  tsv file containing taxon data
  --text_dir TEXT    name of directory containing all plain text
                     files to be processed
  --output TEXT      filename for saving the filename and entity
                     data
  --help             Show this message and exit.
```

Sample command:

`python ent_cli.py --taxon_file="WoRMS/taxon.txt" --text_dir=allpapers --output=entities.csv`
