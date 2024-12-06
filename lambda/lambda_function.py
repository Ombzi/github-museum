import logging
import json
import random
import sys
import dropbox
import re





from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, AudioItemMetadata,
    StopDirective, ClearQueueDirective, ClearBehavior)

# Initializing the logger and setting the level to "INFO"
# Read more about it here https://www.loggly.com/ultimate-guide/python-logging-basics/
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# dict of audio files
audioFiles = {}

"""
# get access_token with temp token
access_token = 'sl.BpXo4TLbZ_f7diQfLikf2Tc9yc0QcCbMGnFr15UbPEE0UEd2bJoOvuz1DUm_m10oZD5m938FOvS0YBgDPgvTMIPPaAdZ5Azw9yWJptplvOaefVtCnUNUw3pWJLANVbq26SdFIZqIALTA'
dbx = dropbox.Dropbox(access_token)
"""

# get dbx with perminent method 
dbx = dropbox.Dropbox(
app_key = "fsi4umlwm2s3fai",
app_secret = "czdutuf8yfgjzq5",
oauth2_refresh_token = "myILnPJLXCUAAAAAAAAAAU1FcyZITt8Sazd91BtPYSnlBeI5dVpkNn29bFiVUQBd"
)

#Salvador
for entry in dbx.files_list_folder('/Apps/MySkill').entries:
    # get a temporary link to the files in this directory
    link = dbx.files_get_temporary_link(entry.path_lower).link
    # remove the file extension from the name
    entry.name = re.sub(r'\..*$', '', entry.name)
    # add the link to the dict
    audioFiles[entry.name] = link

""" 
Instructions to modify the code to play the stream of your choice:

1. Replace the current url with your stream url. Make sure that it has has a valid SSL certificate and starts with 'https' and not 'http'
2. Replace the title under metadata with the name of your stream or radio. Alexa speaks out this name before the stream begings.
3. Replace the subtitle under metadata with your streams tagline. It is displayed on screen enabled devices while the skill is playing.
4. Replace the url under metadata>art>sources with an album art image of your choice. It should be in png or jpg format of the size 512x512 pixels.
5. Replace the url under metadata>backgroundImage>sources with a background image of your choice. It should be in png or jpg format of the size 1200x800 pixels.
"""

"""
# Audio stream metadata
STREAMS = [
  {
    "token": '1',
    "url": audioFiles['water'],
    "metadata": {
      "title": 'custom music',
      "subtitle": 'A subtitle for ',
      "art": {
        "sources": [
          {
            "contentDescription": 'example image',
            "url": 'https://s3.amazonaws.com/cdn.dabblelab.com/img/audiostream-starter-512x512.png',
            "widthPixels": 512,
            "heightPixels": 512
          }
        ]
      },
      "backgroundImage": {
        "sources": [
          {
            "contentDescription": 'example image',
            "url": 'https://s3.amazonaws.com/cdn.dabblelab.com/img/wayfarer-on-beach-1200x800.png',
            "widthPixels": 1200,
            "heightPixels": 800
          }
        ]
      }
    }
  }
]
"""

#Salvador 
# create an array of streams for each file in the dropbox
STREAMS = []

for title, url in audioFiles.items():
    stream = {
        "token": '1',  # You can change this token as needed
        "url": url,
        "metadata": {
            "title": title,
            "subtitle": 'A subtitle for ' + title,
            "art": {
                "sources": [
                    {
                        "contentDescription": 'example image',
                        "url": 'https://s3.amazonaws.com/cdn.dabblelab.com/img/audiostream-starter-512x512.png',
                        "widthPixels": 512,
                        "heightPixels": 512
                    }
                ]
            },
            "backgroundImage": {
                "sources": [
                    {
                        "contentDescription": 'example image',
                        "url": 'https://s3.amazonaws.com/cdn.dabblelab.com/img/wayfarer-on-beach-1200x800.png',
                        "widthPixels": 1200,
                        "heightPixels": 800
                    }
                ]
            }
        }
    }
    STREAMS.append(stream)
    

# Intent Handlers

#Salvador 
#custom intent that selects file by name
### THIS IS THE THING THAT ISN'T WORKING
class SelectFileIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SelectFileIntent")(handler_input)

    def handle(self, handler_input):
        # Extract the value of the "fileTitle" slot
        logger.info("Inside handle for SelectFileIntent")
        slots = handler_input.request_envelope.request.intent.slots
        selected_file = slots["fileTitle"].value

        stream = False
        for option in STREAMS:
            if(option["metadata"]["title"].lowe() == selected_file.lower()):
                stream = option
        
        
        return ( handler_input.response_builder
                    #.speak("Starting the {}".format(stream["metadata"]["title"]))
                    .speak("Starting the {} file".format(stream["metadata"]["title"]))
                    #.speak(str(audioFiles))
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )


class GuideIntent (AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GuideIntent")(handler_input)
        
    def handle(self, handler_input):
        selected_output = "Here are the things I can help you with: Are you looking for a staff member? Are you looking for security? Are you looking for psychology help? How can I help you?" 
        return (
            handler_input.response_builder.speak(speak_output).response
            )


"""
class SelectFileIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SelectFileIntent")(handler_input)

    def handle(self, handler_input):
        # Extract the value of the "fileTitle" slot
        logger.info("Inside handle for SelectFileIntent")
        slots = handler_input.request_envelope.request.intent.slots
        selected_file = slots["fileTitle"].value

        if selected_file == "short":
            speak_output = "short in file"
        elif selected_file == "water":
            speak_output = "water in file"
        else: 
            speak_output = "not in file"
        return (
            handler_input.response_builder.speak(speak_output).response
            )
"""

# This handler checks if the device supports audio playback
class CheckAudioInterfaceHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if handler_input.request_envelope.context.system.device:
            return handler_input.request_envelope.context.system.device.supported_interfaces.audio_player is None
        else:
            return False

    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = language_prompts["DEVICE_NOT_SUPPORTED"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )

#Salvador This is reading the water file 
# This handler starts the stream playback whenever a user invokes the skill or resumes playback.
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self,handler_input):
        speak_output = "Welcome to custom music, you can say name with custom music"
        return ( 
            handler_input.response_builder.speak(speak_output).response
                )

class ResumeStreamIntentHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return (is_request_type("PlaybackController.PlayCommandIssued")(handler_input)
                or is_intent_name("AMAZON.ResumeIntent")(handler_input)
                )
    def handle(self,handler_input):
        stream = STREAMS[0]
        return ( handler_input.response_builder
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )

# This handler handles all the required audio player intents which are not supported by the skill yet. 
class UnhandledFeaturesIntentHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return (is_intent_name("AMAZON.LoopOnIntent")(handler_input)
                or is_intent_name("AMAZON.NextIntent")(handler_input)
                or is_intent_name("AMAZON.PreviousIntent")(handler_input)
                or is_intent_name("AMAZON.RepeatIntent")(handler_input)
                or is_intent_name("AMAZON.ShuffleOnIntent")(handler_input)
                or is_intent_name("AMAZON.StartOverIntent")(handler_input)
                or is_intent_name("AMAZON.ShuffleOffIntent")(handler_input)
                or is_intent_name("AMAZON.LoopOffIntent")(handler_input)
                )
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["UNHANDLED"])
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )

# This handler provides the user with basic info about the skill when a user asks for it.
# Note: This would only work with one shot utterances and not during stream playback.
class AboutIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AboutIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = random.choice(language_prompts["ABOUT"])
        reprompt = random.choice(language_prompts["ABOUT_REPROMPT"])
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["HELP"])
        reprompt = random.choice(language_prompts["HELP_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (
            is_intent_name("AMAZON.CancelIntent")(handler_input)
            or is_intent_name("AMAZON.StopIntent")(handler_input)
            or is_intent_name("AMAZON.PauseIntent")(handler_input)
            )
    
    def handle(self, handler_input):
        return ( handler_input.response_builder
                    .add_directive(
                        ClearQueueDirective(
                            clear_behavior=ClearBehavior.CLEAR_ALL)
                        )
                    .add_directive(StopDirective())
                    .set_should_end_session(True)
                    .response
                )

class PlaybackStartedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackStarted")(handler_input)
    
    def handle(self, handler_input):
        return ( handler_input.response_builder
                    .add_directive(
                        ClearQueueDirective(
                            clear_behavior=ClearBehavior.CLEAR_ENQUEUED)
                        )
                    .response
                )

class PlaybackStoppedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ( is_request_type("PlaybackController.PauseCommandIssued")(handler_input)
                or is_request_type("AudioPlayer.PlaybackStopped")(handler_input)
            )
    
    def handle(self, handler_input):
        return ( handler_input.response_builder
                    .add_directive(
                        ClearQueueDirective(
                            clear_behavior=ClearBehavior.CLEAR_ALL)
                        )
                    .add_directive(StopDirective())
                    .set_should_end_session(True)
                    .response
                )

# This handler tries to play the stream again if the playback failed due to any reason.
class PlaybackFailedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackFailed")(handler_input)
    
    def handle(self,handler_input):
        stream = STREAMS[0]
        return ( handler_input.response_builder
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )
    

# This handler handles utterances that can't be matched to any other intent handler.
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["FALLBACK"])
        reprompt = random.choice(language_prompts["FALLBACK_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class ExceptionEncounteredRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("System.ExceptionEncountered")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Interceptors

# This interceptor is used for supporting different languages and locales. It detects the users locale,
# loads the corresponding language prompts and sends them as a request attribute object to the handler functions.

class LocalizationInterceptor(AbstractRequestInterceptor):

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        
        try:
            with open("languages/"+str(locale)+".json") as language_data:
                language_prompts = json.load(language_data)
        except:
            with open("languages/"+ str(locale[:2]) +".json") as language_data:
                language_prompts = json.load(language_data)
        
        handler_input.attributes_manager.request_attributes["_"] = language_prompts


# This interceptor logs each request sent from Alexa to our endpoint.
class RequestLogger(AbstractRequestInterceptor):

    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))

# This interceptor logs each response our endpoint sends back to Alexa.
class ResponseLogger(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))

# This exception handler handles syntax or routing errors. If you receive an error stating 
# the request handler is not found, you have not implemented a handler for the intent or 
# included it in the skill builder below
class CatchAllExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return True
    
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = language_prompts["ERROR"]
        reprompt = language_prompts["ERROR_REPROMPT"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# Skill Builder
# Define a skill builder instance and add all the request handlers,
# exception handlers and interceptors to it.

sb = SkillBuilder()
sb.add_request_handler(CheckAudioInterfaceHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SelectFileIntentHandler())
sb.add_request_handler(GuideIntent())
sb.add_request_handler(ResumeStreamIntentHandler())
sb.add_request_handler(UnhandledFeaturesIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(PlaybackStartedIntentHandler())
sb.add_request_handler(PlaybackStoppedIntentHandler())
sb.add_request_handler(PlaybackFailedIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())



lambda_handler = sb.lambda_handler()
