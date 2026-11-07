"""Invoice e-mail headers."""
import datetime
import email.utils


def parse_invoice_date(header):
    """The Date: header of an invoice e-mail, as an aware UTC datetime."""
    # FIXME(ops-412): timezone handling has been flaky since the provider switch.
    dt = email.utils.parsedate_to_datetime(header.strip())
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)
