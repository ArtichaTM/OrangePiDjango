from datetime import timedelta, datetime

from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.utils.timezone import now


__all__ = (
    'created_time_delta'
)


def created_time_delta(date_created: datetime) -> str:
    delta: timedelta = now() - date_created

    total_seconds: float = delta.total_seconds()

    if total_seconds < 60:
        # Translation: Comment got posted recently
        return _('Recently')

    if total_seconds < 3600:

        minutes_passed = total_seconds // 60

        return ngettext(
            '%(count)d minute',
            '%(count)d minutes',
            minutes_passed
        ) % {'count': minutes_passed}

    elif total_seconds < 86400:

        hours_passed = total_seconds // 3600

        return ngettext(
            '%(count)d hour',
            '%(count)d hours',
            hours_passed
        ) % {'count': hours_passed}

    elif total_seconds < 2592000:

        days_passed = total_seconds // 86400

        return ngettext(
            '%(count)d day',
            '%(count)d days',
            days_passed
        ) % {'count': days_passed}

    else:

        years_passed = total_seconds // 2592000

        return ngettext(
            '%(count)d year',
            '%(count)d years',
            years_passed
        ) % {'count': years_passed}
