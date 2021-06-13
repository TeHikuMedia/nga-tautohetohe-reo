import re
import json
import yaml
import shlex
import click
import logging
import subprocess


def post_text_to_corpora(data, auth):

    logging.info(f"Data: {data}")

    cmd = f'''curl \
        --location \
        --request POST \
        '{auth["api_url"]}' \
        --header 'referrer: ' \
        --header 'Authorization: Token {auth["token"]}' \
        --form 'description="{data["description"]}"' \
        --form 'dialect="{data["dialect"]}"' \
        --form 'notes="{data["notes"]}"' \
        --form 'primary_language="{data["primary_language"]}"' \
        --form 'secondary_language="{data["secondary_language"]}"' \
        --form 'copyright={json.dumps(data["copyright"])}' \
        --form 'config={json.dumps(data["config"])}' \
        --form 'source.author={json.dumps(data["source"]["author"])}' \
        --form 'source.description={json.dumps(data["source"]["description"])}' \
        --form 'source.source_name={json.dumps(data["source"]["source_name"])}' \
        --form 'source.source_type={json.dumps(data["source"]["source_type"])}' \
        --form 'source.source_url={json.dumps(data["source"]["source_url"])}' \
        --form 'original_file=@"{data["original_file"]}"' \
        --form 'cleaned_file=@"{data["cleaned_file"]}"'
    '''

    logging.info(' '.join(["\nRunning command:", re.sub('\s{2,}', ' ', cmd), '\n']))
    subprocess.run(shlex.split(cmd), check=True)


@click.command()
@click.option("--metadata", default="corpus", help="Directory of corpus files")
@click.option("--credentials", default="credentials.yaml", help="YAML file containing corpora API credentials")
@click.option("--log_level", default="INFO", help="Log level (default: INFO)")
def main(metadata, credentials, log_level):

    # Set logger config
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    auth = yaml.load(open(credentials, 'r'), Loader=yaml.FullLoader)["corpora"]
    data = yaml.load(open(metadata, 'r'), Loader=yaml.FullLoader)

    post_text_to_corpora(data, auth)


if __name__ == "__main__":
    main()
