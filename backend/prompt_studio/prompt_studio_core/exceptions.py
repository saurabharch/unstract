from prompt_studio.prompt_studio_core.constants import ToolStudioErrors
from rest_framework.exceptions import APIException


class PlatformServiceError(APIException):
    status_code = 400
    default_detail = ToolStudioErrors.PLATFORM_ERROR


class ToolNotValid(APIException):
    status_code = 400
    default_detail = "Custom tool is not valid."


class IndexingAPIError(APIException):
    status_code = 500
    default_detail = "Error while indexing file"


class AnswerFetchError(APIException):
    status_code = 500
    default_detail = "Error occured while fetching response for the prompt"


class DefaultProfileError(APIException):
    status_code = 500
    default_detail = (
        "Default LLM profile is not configured."
        "Please set an LLM profile as default to continue."
    )


class EnvRequired(APIException):
    status_code = 404
    default_detail = "Environment variable not set"


class OutputSaveError(APIException):
    status_code = 500
    default_detail = "Unable to store the output."


class ToolDeleteError(APIException):
    status_code = 500
    default_detail = "Failed to delete the error"


class NoPromptsFound(APIException):
    status_code = 404
    default_detail = "No prompts available to process"


class PermissionError(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action."


class EmptyPromptError(APIException):
    status_code = 422
    default_detail = "Prompt(s) cannot be empty"
