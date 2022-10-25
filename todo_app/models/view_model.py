from datetime import date, datetime


class ViewModel:
    show_all_done_items_threshold = 5

    def __init__(self, not_started, in_progress, done, show_all_items=False):
        self._not_started = not_started
        self._in_progress = in_progress
        self._done = done
        self._treat_all_done_items_as_high_priority = show_all_items

    @property
    def not_started(self):
        return self._not_started

    @property
    def in_progress(self):
        return self._in_progress

    @property
    def high_priority_done_items(self):
        if (self._treat_all_done_items_as_high_priority
                or len(self._done) <= self.show_all_done_items_threshold):
            return self._done
        else:
            return self.recent_done_items

    @property
    def is_hiding_done_items(self):
        return len(self.high_priority_done_items) != len(self._done)

    @property
    def has_expanded_done_items(self):
        return (
            len(self._done) > self.show_all_done_items_threshold
            and len(self.recent_done_items) < len(
                self.high_priority_done_items
            )
        )

    @property
    def recent_done_items(self):
        return list(filter(
            lambda item:
                datetime.fromisoformat(
                    item.last_status_change_datetime
                ).date() >= date.today(),
            self._done
        ))
