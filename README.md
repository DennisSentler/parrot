<p align="center">
  <img width="600" height="185,005"
       src="https://raw.githubusercontent.com/castorini/parrot/master/logo/logotype%20horizontal.png">
</p>

# parrot
Keyword spotting using audio from speech synthesis services and YouTube

## Prerequisites ##
**Google**

[Google Cloud Text-To-Speech SDK Instruction](https://cloud.google.com/text-to-speech/docs/libraries)

Set authentification in variable 
```
export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"
```
## Example Use
**Generate systhesized examples for words**
```
python word_to_audio.py 
  --words [word1] [word2] ...
  --lang [de-DE] [en-US] ...
```
Create 320 different systhesized examples for each word using [Microsoft Cognitive Services](https://azure.microsoft.com/en-ca/services/cognitive-services/text-to-speech/), [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/) and [IBM Watson Text to Speech](https://www.ibm.com/watson/services/text-to-speech/).

**Split a wav file into multiple wav files with same length**
```
python split_wav_file.py [sample.wav] [length_in_second]
```

**Add silence at the beginning and end of all wav files in a directory**
```
python add_silence.py [length_of_silence_in_second] --directories [dir1] [dir2] ...
```
