import click
import glob
import pandas as pd
import spacy
from spacy_lookup import Entity


def extract_taxon_names(fn):
    taxon = pd.read_csv(fn, sep="\t")
    return taxon["scientificName"].to_list()


def create_nlp_pipe():
    return spacy.load("en_core_web_md")


def modify_nlp_pipe(nlp, taxon_names, label):
    entity = Entity(keywords_list=taxon_names, label=label)
    nlp.add_pipe(entity)
    nlp.remove_pipe("ner")


def extract_filenames_and_texts(text_dir):
    fns = []
    texts = []
    for fn in glob.glob(text_dir + "/*.txt"):
        fns.append(fn.split("/")[1])
        with open(fn, "r") as f:
            texts.append(f.read())
    return fns, texts


def extract_ents_from_texts(nlp, texts):
    docs = list(nlp.pipe(texts))
    ent_sets = [set([ent.text.lower() for ent in doc.ents]) for doc in docs]
    return ent_sets


def build_ent_df(fns, ent_sets):
    data = {"filename": fns, "ents": ent_sets}
    return pd.DataFrame(data=data)


def save_ent_df(fn, ent_df):
    ent_df.to_csv(fn)


@click.command()
@click.option("--taxon_file", help="tsv file containing taxon data")
@click.option(
    "--text_dir",
    help="name of directory containing all plain text files to be processed",
)
@click.option("--output", help="filename for saving the filename and entity data")
def main(taxon_file, text_dir, output):
    """Small program to extract sets of named entities from texts based on a defined dictionary."""
    sci_names = extract_taxon_names(taxon_file)
    nlp = create_nlp_pipe()
    modify_nlp_pipe(nlp, sci_names, "Marine")
    fns, texts = extract_filenames_and_texts(text_dir)
    ent_sets = extract_ents_from_texts(nlp, texts)
    ent_df = build_ent_df(fns, ent_sets)
    save_ent_df(output, ent_df)


if __name__ == "__main__":
    main()
