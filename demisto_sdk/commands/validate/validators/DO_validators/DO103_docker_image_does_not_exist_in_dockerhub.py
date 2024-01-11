from __future__ import annotations

from typing import Iterable, List, Union

from demisto_sdk.commands.content_graph.objects.integration import Integration
from demisto_sdk.commands.content_graph.objects.script import Script
from demisto_sdk.commands.validate.validators.base_validator import (
    BaseValidator,
    ValidationResult,
)

ContentTypes = Union[Integration, Script]


class DockerImageDoesNotExistInDockerhubValidator(BaseValidator[ContentTypes]):
    error_code = "DO103"
    description = "Validate that the given content item's docker-image actually exists in dockerhub"
    error_message = "The {0} docker-image does not exist in dockerhub"
    related_field = "Docker image"
    is_auto_fixable = False

    def is_valid(self, content_items: Iterable[ContentTypes]) -> List[ValidationResult]:
        invalid_content_items = []
        for content_item in content_items:
            if not content_item.is_javascript:
                docker_image_object = content_item.docker_image_object
                if (
                    not docker_image_object.is_valid
                    or not self.dockerhub_client.is_docker_image_exist(
                        docker_image_object.name, tag=docker_image_object.tag
                    )
                ):
                    invalid_content_items.append(
                        ValidationResult(
                            validator=self,
                            message=self.error_message.format(
                                content_item.docker_image
                            ),
                            content_object=content_item,
                        )
                    )

        return invalid_content_items
