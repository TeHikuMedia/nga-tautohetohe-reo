import re
import json
import yaml
import shlex
import subprocess

token = yaml.load(open('credentials.yaml', 'r'), Loader=yaml.FullLoader)['corpora']['token']
data = yaml.load(open('metadata.yaml', 'r'), Loader=yaml.FullLoader)

print(data)

def post_text_to_corpora(data, token):

    print("\n\nData:", data)

    cmd = f'''curl \
        --location \
        --request POST \
        'https://koreromaori.com/api/text/' \
        --header 'Authorization: Token {token}' \
        --form 'description="{data["description"]}"' \
        --form 'dialect="{data["dialect"]}"' \
        --form 'notes="{data["notes"]}"' \
        --form 'primary_language="{data["primary_language"]}"' \
        --form 'secondary_language="{data["secondary_language"]}"' \
        --form 'copyright={json.dumps(data["copyright"])}' \
        --form 'config={json.dumps(data["config"])}' \
        --form 'source={json.dumps(data["source"])}' \
        --form 'original_file=@"{data["original_file"]}"' \
        --form 'cleaned_file=@"{data["cleaned_file"]}"'
    '''

    print("\nRunning command:", re.sub('\s{2,}', ' ', cmd), '\n')
    subprocess.run(shlex.split(cmd), check=True)

post_text_to_corpora(data, token)

print('\n\n' + '=' * 30)

