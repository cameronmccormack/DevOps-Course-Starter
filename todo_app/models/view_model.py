class ViewModel:
    def __init__(self, not_started, in_progress, done):
        self._not_started = not_started
        self._in_progress = in_progress
        self._done = done

    @property
    def not_started(self):
        return self._not_started

    @property
    def in_progress(self):
        return self._in_progress

    @property
    def done(self):
        return self._done
