import json
import typing as t
import typing_extensions as te
from .exception import LtiException


TSubmissionReview = te.TypedDict(
    "TSubmissionReview",
    {
        # Required data
        "reviewableStatus": list,
        # Optional data
        "label": str,
        "url": str,
        "custom": t.Dict[str, str],
    },
    total=False,
)

TSubmissionType = te.TypedDict(
    "TSubmissionType",
    {
        "type": str,
        "external_tool_url": str,
    },
    total=False,
)

CANVAS_SUBMISSION_TYPE = "https://canvas.instructure.com/lti/submission_type"

TLineItem = te.TypedDict(
    "TLineItem",
    {
        "id": str,
        "scoreMaximum": int,
        "label": str,
        "resourceId": str,
        "tag": str,
        "resourceLinkId": str,
        "startDateTime": str,
        "endDateTime": str,
        "gradesReleased": bool,
        "submissionReview": TSubmissionReview,
        CANVAS_SUBMISSION_TYPE: TSubmissionType,
    },
    total=False,
)


class LineItem:
    _id: t.Optional[str] = None
    _score_maximum: t.Optional[float] = None
    _label: t.Optional[str] = None
    _resource_id: t.Optional[str] = None
    _resource_link_id: t.Optional[str] = None
    _tag: t.Optional[str] = None
    _start_date_time: t.Optional[str] = None
    _end_date_time: t.Optional[str] = None
    _grades_released: t.Optional[bool] = None
    _submission_review: t.Optional[TSubmissionReview] = None
    _submission_type: t.Optional[TSubmissionType] = None

    def __init__(self, lineitem: t.Optional[TLineItem] = None):
        if not lineitem:
            lineitem = {}
        self._id = lineitem.get("id")
        self._score_maximum = lineitem.get("scoreMaximum")
        self._label = lineitem.get("label")
        self._resource_id = lineitem.get("resourceId")
        self._resource_link_id = lineitem.get("resourceLinkId")
        self._tag = lineitem.get("tag")
        self._start_date_time = lineitem.get("startDateTime")
        self._end_date_time = lineitem.get("endDateTime")
        self._grades_released = lineitem.get("gradesReleased")
        self._submission_review = lineitem.get("submissionReview")
        self._submission_type = lineitem.get(CANVAS_SUBMISSION_TYPE)

    def get_id(self) -> t.Optional[str]:
        return self._id

    def set_id(self, value: str) -> "LineItem":
        self._id = value
        return self

    def get_label(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#label
        """
        return self._label

    def set_label(self, value: str) -> "LineItem":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#label
        """
        self._label = value
        return self

    def get_score_maximum(self) -> t.Optional[float]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#scoremaximum
        """
        return self._score_maximum

    def set_score_maximum(self, value: float) -> "LineItem":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#scoremaximum
        """
        if not isinstance(value, (int, float)):
            raise LtiException(
                "Invalid scoreMaximum value: score must be integer or float"
            )
        if value <= 0:
            raise LtiException(
                "Invalid scoreMaximum value: score must be non null value, strictly greater than 0"
            )

        self._score_maximum = value
        return self

    def get_resource_id(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#tool-resource-identifier-resourceid
        """
        return self._resource_id

    def set_resource_id(self, value: str) -> "LineItem":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#tool-resource-identifier-resourceid
        """
        self._resource_id = value
        return self

    def get_resource_link_id(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0#resourcelinkid-and-binding-a-line-item-to-a-resource-link
        """
        return self._resource_link_id

    def set_resource_link_id(self, value: str) -> "LineItem":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0#resourcelinkid-and-binding-a-line-item-to-a-resource-link
        """
        self._resource_link_id = value
        return self

    def get_tag(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#tag
        """
        return self._tag

    def set_tag(self, value: str) -> "LineItem":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#tag
        """
        self._tag = value
        return self

    def get_start_date_time(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#startdatetime
        """
        return self._start_date_time

    def set_start_date_time(self, value: str) -> "LineItem":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#startdatetime
        """
        self._start_date_time = value
        return self

    def get_end_date_time(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#enddatetime
        """
        return self._end_date_time

    def set_end_date_time(self, value: str) -> "LineItem":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#enddatetime
        """
        self._end_date_time = value
        return self

    def set_grades_released(self, value):
        if not isinstance(value, bool):
            raise ValueError("grades_released must be a boolean value")
        self._grades_released = value
        return self

    def get_grades_released(self):
        return getattr(self, '_grades_released', None)

    def get_submission_review(self) -> t.Optional[TSubmissionReview]:
        return self._submission_review

    def set_submission_review(
        self,
        reviewable_status: t.List,
        label: t.Optional[str] = None,
        url: t.Optional[str] = None,
        custom: t.Optional[t.Dict[str, str]] = None,
    ) -> "LineItem":
        if not isinstance(reviewable_status, list):
            raise Exception('Invalid "reviewable_status" argument')

        self._submission_review: TSubmissionReview = {
            "reviewableStatus": reviewable_status
        }
        if label:
            self._submission_review["label"] = label
        if url:
            self._submission_review["url"] = url
        if custom:
            self._submission_review["custom"] = custom

        return self
    
    def get_submission_type(self) -> t.Optional[TSubmissionType]:
        return self._submission_type

    def set_submission_type(self, _type: str, external_tool_url: t.Optional[str]) -> "LineItem":
        """This is a Canvas extension to support creating assignments linked to the external tools."""
        if _type not in ["none", "external_tool"]:
            raise Exception('Invalid "type" argument. Must be "none" or "external_tool"')
        if _type == "none":
            self._submission_type = TSubmissionType(type=_type)
        else:
            if not external_tool_url:
                raise Exception('"external_tool_url" field is missing. Must be provided for "external_tool" type')
            self._submission_type = TSubmissionType(type=_type, external_tool_url=external_tool_url)

        return self

    def get_value(self) -> str:
        """
        Prepare the line item data in the format required by the LTI-AGS specification.

        The final dictionary is then converted to a JSON string and then sent via the API.
        Any missing values are not included in the final JSON string. According to the LTI-AGS specification,
        any missing fields will be interpreted as empty, and will be cleared from the line item in the LMS.
        https://www.imsglobal.org/spec/lti-ags/v2p0/#updating-a-line-item
        https://www.imsglobal.org/spec/lti-ags/v2p0/openapi/#/default
        """
        data = {
            "id": self._id,
            "scoreMaximum": self._score_maximum,
            "label": self._label,
            "resourceId": self._resource_id,
            "resourceLinkId": self._resource_link_id,
            "tag": self._tag,
            "startDateTime": self._start_date_time,
            "endDateTime": self._end_date_time,
            "gradesReleased": self._grades_released,
            "submissionReview": self._submission_review,
            CANVAS_SUBMISSION_TYPE: self._submission_type,
        }
        return json.dumps({k: v for k, v in data.items() if v})
