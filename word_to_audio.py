import argparse
import os
from random import randint

import requests
from google.cloud import texttospeech
from ibm_watson import TextToSpeechV1


def watson_cloud_tts(text, lang_list, output_path):
    # authentification with IBM_CREDENTIALS_FILE
    text_to_speech = TextToSpeechV1()
    # get voice list from IBM, watson
    voice_list = text_to_speech.list_voices().get_result()["voices"]

    # Text to speech api request
    for voice in voice_list:
        # skip not requested voice languages
        if voice["language"] not in lang_list:
            continue

        # Generate random voice characteristics
        random_rate = "default"
        random_pitch = "default"

        for i in range(10):
            ssml = (
                '''
                <prosody rate="{0}" pitch="{1}">
                    {2}
                </prosody>
                '''.format(
                    random_rate, random_pitch, text
                )
            )
            response = text_to_speech.synthesize(ssml, accept="audio/wav",
                                                 voice=voice["name"])

            file_name = "{3}_watson_{0}_{4}_{1}{2}.wav".format(
                voice["name"], random_rate,
                random_pitch, text, voice["gender"][0]
            )
            with open(output_path + "/" + file_name, "wb") as f:
                f.write(response.get_result().content)

            random_rate = str(randint(-15, 15)) + "%"
            random_pitch = str(randint(-10, 10)) + "Hz"

        print("audios in voice " + voice["name"] + " are created")


def google_cloud_tts(text, lang_list, output_path):
    # authentification from  env var GOOGLE_APPLICATION_CREDENTIALS
    client = texttospeech.TextToSpeechClient()
    # pull all voices from gcloud
    voice_list = client.list_voices()
    input_text = texttospeech.SynthesisInput(text=text)
    # Text to speech api request
    for voice in voice_list.voices:
        if voice.language_codes[0] not in lang_list:
            continue

        # Generate random voice characteristics
        random_rate = 1
        random_volume = 0
        random_pitch = 0

        for i in range(10):
            voice_config = texttospeech.VoiceSelectionParams(
                language_code=voice.language_codes[0], name=voice.name
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate=random_rate,
                pitch=random_pitch,
                volume_gain_db=random_volume,
            )

            response = client.synthesize_speech(
                input=input_text, voice=voice_config, audio_config=audio_config
            )

            gender_char = voice.ssml_gender.name[0].lower()
            file_name = "{4}_gcp_{0}_{5}_{1}r{2}v{3}p.wav".format(
                voice.name, random_rate, random_volume,
                random_pitch, text, gender_char
            )
            with open(output_path + "/" + file_name, "wb") as f:
                f.write(response.audio_content)

            random_rate = randint(75, 125) / 100
            random_volume = randint(-5, 15) / 10
            random_pitch = randint(-50, 50) / 10

        print("audios in voice {0} are created".format(voice.name))


def microsoft_tts(text, output_path, token):
    voice_list = [
        ("en-AU", "en-AU, Catherine"),
        ("en-AU", "en-AU, HayleyRUS"),
        ("en-CA", "en-CA, Linda"),
        ("en-CA", "en-CA, HeatherRUS"),
        ("en-GB", "en-GB, Susan, Apollo"),
        ("en-GB", "en-GB, HazelRUS"),
        ("en-GB", "en-GB, George, Apollo"),
        ("en-IE", "en-IE, Sean"),
        ("en-IN", "en-IN, Heera, Apollo"),
        ("en-IN", "en-IN, PriyaRUS"),
        ("en-IN", "en-IN, Ravi, Apollo"),
        ("en-US", "en-US, ZiraRUS"),
        ("en-US", "en-US, JessaRUS"),
        ("en-US", "en-US, BenjaminRUS"),
    ]

    tts_url = "https://westus.tts.speech.microsoft.com/cognitiveservices/v1"
    # Authentication
    # Text to speech api request
    for language, voice in voice_list:
        # Generate random voice characteristics
        random_rate = str(0) + "%"
        random_volume = str(0) + "%"
        random_pitch = str(0) + "Hz"

        for i in range(10):
            tts_header = {
                "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
                "Authorization": token,
                "Content-Type": "application/ssml+xml",
            }

            ssml = (
                '''
                <prosody rate="{0}" volume="{1}" pitch="{2}">
                    {3}
                </prosody>
                '''.format(
                    random_rate, random_volume, random_pitch, text
                )
            )
            tts_content = '''
            <speak version='1.0'
                xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{0}'>
                <voice
                    name='Microsoft Server Speech Text to Speech Voice ({1})'>
                    {2}
                </voice>
            </speak>'''.format(
                language, voice, ssml
            )

            tts_response = requests.post(
                tts_url, headers=tts_header, data=tts_content)

            file_name = "ms_{0}{1}{2}{3}.wav".format(
                voice.replace(
                    " ", ""), random_rate, random_volume, random_pitch
            )
            with open(output_path + "/" + file_name, "wb") as f:
                f.write(tts_response.content)

            random_rate = str(randint(-20, 20)) + "%"
            random_volume = str(randint(-20, 20)) + "%"
            random_pitch = str(randint(-15, 15)) + "Hz"

        print("audios in voice " + voice + " are created")


def main():
    parser = argparse.ArgumentParser(
        description="create a directory for each word"
    )
    parser.add_argument(
        "--words", nargs="*", help="Words to be pronounced",
        default=["albert einstein"]
    )
    parser.add_argument(
        "--lang", nargs="*", help="To generate for languages",
        default=["en-US"]
    )
    args = parser.parse_args()

    word_list = args.words
    lang_list = args.lang

    for word in word_list:
        # Create an individual directory for each keyword if not existed
        path = "generated_words/" + word.replace(" ", "")
        if not os.path.exists(path):
            os.makedirs(path)
            print(path + " directory is created!")

        # microsoft_tts(word, path, ms_token_response.text)
        google_cloud_tts(word, lang_list, path)
        watson_cloud_tts(word, lang_list, path)

        print("all audios for '" + word + "' are generated!")


if __name__ == "__main__":
    main()
