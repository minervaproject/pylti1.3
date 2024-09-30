import json

from parameterized import parameterized

from pylti1p3.lineitem import LineItem
from .base import TestServicesBase


class TestLineItem(TestServicesBase):
    # pylint: disable=import-outside-toplevel

    @parameterized.expand(
        [
            ("none", None),
            ("none", "https://this.has.to.be.ignored"),
        ]
    )
    def test_submission_type_none(self, _type, url):
        # Arrange
        lineitem = LineItem()
        assert lineitem.get_submission_type() is None

        # Act
        lineitem.set_submission_type(_type, url)

        # Assert
        assert lineitem.get_submission_type()['type'] == _type
        assert 'url' not in lineitem.get_submission_type()

    def test_submission_type_external_tool(self):
        # Arrange
        lineitem = LineItem()
        assert lineitem.get_submission_type() is None

        # Act
        lineitem.set_submission_type("external_tool", "https://this.is.external.tool.com/lti/launch")

        # Assert
        assert lineitem.get_submission_type()['type'] == "external_tool"
        assert lineitem.get_submission_type()['external_tool_url'] == "https://this.is.external.tool.com/lti/launch"

    @parameterized.expand(
        [
            ("external_tool", None),
            ("some-other-type", "https://this.is.external.tool.com/lti/launch"),
        ]
    )
    def test_submission_types_validation_error(self, _type, url):
        # Arrange
        lineitem = LineItem()
        assert lineitem.get_submission_type() is None

        # Act
        self.assertRaises(Exception, lineitem.set_submission_type, _type, url)

    def test_get_value(self):
        # Arrange
        lineitem = LineItem()
        lineitem.set_id("123")
        lineitem.set_score_maximum(50)
        lineitem.set_label("Test Label")
        lineitem.set_resource_id("1")
        lineitem.set_resource_link_id("2")
        lineitem.set_tag("test-tag")
        lineitem.set_start_date_time("2021-01-01T00:00:00Z")
        lineitem.set_end_date_time("2021-01-02T00:00:00Z")
        lineitem.set_grades_released(False)
        lineitem.set_submission_review(
            ["completed", "not_reviewed"],
            label="Test Label",
            url="https://this.is.external.tool.com/lti/launch",
            custom={"key": "value"},
        )
        lineitem.set_submission_type("external_tool", "https://this.is.external.tool.com/lti/launch")

        # Act
        value = lineitem.get_value()

        # Assert
        assert value == json.dumps({
            "id": "123",
            "scoreMaximum": 50,
            "label": "Test Label",
            "resourceId": "1",
            "resourceLinkId": "2",
            "tag": "test-tag",
            "startDateTime": "2021-01-01T00:00:00Z",
            "endDateTime": "2021-01-02T00:00:00Z",
            "gradesReleased": False,
            "submissionReview": {
                "reviewableStatus": ["completed", "not_reviewed"],
                "label": "Test Label",
                "url": "https://this.is.external.tool.com/lti/launch",
                "custom": {"key": "value"},
            },
            "https://canvas.instructure.com/lti/submission_type": {
                "type": "external_tool",
                "external_tool_url": "https://this.is.external.tool.com/lti/launch",
            },
        })

    @parameterized.expand([
        (True, True),
        (False, False),
        ("true", ValueError),
        ("false", ValueError),
        (1, ValueError),
        (0, ValueError),
        (None, ValueError),
    ])
    def test_grades_released(self, input_value, expected):
        # Arrange
        lineitem = LineItem()

        # Act & Assert
        if expected is ValueError:
            with self.assertRaises(ValueError):
                lineitem.set_grades_released(input_value)
        else:
            lineitem.set_grades_released(input_value)
            self.assertEqual(lineitem.get_grades_released(), expected)
