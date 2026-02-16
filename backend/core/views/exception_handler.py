from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework import status

from core.responses import format_api_response
from core.exceptions import ServiceError


def _empty_errors():
    return {"fields": {}, "non_field": [], "detail": []}


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _item(message, code=None):
    if isinstance(message, ErrorDetail):
        return {"message": str(message), "code": str(message.code or code or "error")}

    return {"message": str(message), "code": str(code or getattr(message, "code", None) or "error")}


def errors_from_api_exception(exc):
    """
    Convert APIException.get_full_details() into:
    { "fields": {...}, "non_field": [...], "detail": [...] }
    """
    full = exc.get_full_details()
    out = _empty_errors()

    # leaf: {"message": "...", "code": "..."}
    if isinstance(full, dict) and "message" in full and "code" in full and len(full.keys()) <= 3:
        out["detail"].append(_item(full.get("message"), full.get("code")))
        return out

    # list -> non_field
    if isinstance(full, list):
        for x in full:
            if isinstance(x, dict) and "message" in x:
                out["non_field"].append(_item(x.get("message"), x.get("code")))
            else:
                out["non_field"].append(_item(x))
        return out

    # dict -> fields / non_field_errors / detail
    if isinstance(full, dict):
        for key, val in full.items():
            items = []
            for x in _as_list(val):
                if isinstance(x, dict) and "message" in x:
                    items.append(_item(x.get("message"), x.get("code")))
                else:
                    items.append(_item(x))

            if key == "non_field_errors":
                out["non_field"].extend(items)
            elif key == "detail":
                out["detail"].extend(items)
            else:
                out["fields"][key] = out["fields"].get(key, []) + items

        # 极少见兜底
        if not out["fields"] and not out["non_field"] and not out["detail"]:
            out["detail"].append(_item("Request failed", "error"))

        return out

    # unknown type fallback
    out["detail"].append(_item(str(full), "error"))
    return out


def errors_from_drf_response_data(data):
    """
    For Http404 / PermissionDenied
    """
    out = _empty_errors()

    if isinstance(data, dict):
        if "detail" in data:
            for x in _as_list(data["detail"]):
                out["detail"].append(_item(x))
            return out

        for key, val in data.items():
            items = [_item(x) for x in _as_list(val)]
            if key == "non_field_errors":
                out["non_field"].extend(items)
            else:
                out["fields"][key] = out["fields"].get(key, []) + items

        if not out["fields"] and not out["non_field"] and not out["detail"]:
            out["detail"].append(_item("Request failed", "error"))
        return out

    # list -> non_field
    if isinstance(data, list):
        out["non_field"] = [_item(x) for x in data]
        return out

    # scalar -> detail
    out["detail"].append(_item(data))
    return out


def errors_from_service_error(exc):
    out = _empty_errors()
    out["detail"].append(_item(getattr(exc, "detail", str(exc)), getattr(exc, "code", "service_error")))
    return out


def pick_message(errors, fallback="Request failed"):
    if errors["detail"]:
        return errors["detail"][0]["message"]
    if errors["non_field"]:
        return errors["non_field"][0]["message"]
    for field, items in errors["fields"].items():
        if items:
            return items[0]["message"]
    return fallback


def custom_exception_handler(exc, context):
    """
    Standardize All handled exceptions into standard API response format,
    while keeping errors = {fields, non_field, detail}.
    """
    request = context.get("request")

    drf_response = drf_exception_handler(exc, context)

    # 1) ServiceError
    if drf_response is None and isinstance(exc, ServiceError):
        errors = errors_from_service_error(exc)
        message = pick_message(errors, fallback=getattr(exc, "detail", "Request failed"))
        return format_api_response(
            success=False,
            message=message,
            code=getattr(exc, "code", "service_error"),
            data=None,
            errors=errors,
            request=request,
            status_code=getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST),
        )

    # 2) DRF unhandled, nor ServiceError: let Django handle it (500)
    if drf_response is None:
        return None

    # 3) DRF handled: distinguish APIException vs Http404/PermissionDenied
    if isinstance(exc, APIException):
        errors = errors_from_api_exception(exc)
        code = getattr(exc, "default_code", "error")
    else:
        # Http404 / PermissionDenied: use drf_response.data to build errors
        errors = errors_from_drf_response_data(drf_response.data)
        code = "error"

    message = pick_message(errors, fallback="Request failed")

    return format_api_response(
        success=False,
        message=message,
        code=code,
        data=None,
        errors=errors,
        request=request,
        status_code=drf_response.status_code,
    )
