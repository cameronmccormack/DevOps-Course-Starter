import pytest
from datetime import datetime
from freezegun import freeze_time

from todo_app.models.view_model import ViewModel
from todo_app.models.item import Item
from todo_app.models.status import Status


@pytest.fixture
def item_not_started():
    return Item(
        "not_started_id",
        "Test Not Started Name",
        datetime(2021, 1, 1, 9).isoformat(),
        Status.NOT_STARTED
    )


@pytest.fixture
def item_in_progress():
    return Item(
        "in_progress_id",
        "Test In Progress Name",
        datetime(2021, 1, 1, 9).isoformat(),
        Status.IN_PROGRESS
    )


@pytest.fixture
def item_done_today():
    return Item(
        "done_today_id",
        "Test Done Today Name",
        datetime(2021, 1, 2, 9).isoformat(),
        Status.DONE
    )


@pytest.fixture
def item_done_before_today():
    return Item(
        "done_before_today_id",
        "Test Done Before Today Name",
        datetime(2021, 1, 1, 9).isoformat(),
        Status.DONE
    )


@pytest.fixture
def view_model_without_items():
    return ViewModel([], [], [])


@pytest.fixture
def view_model_with_two_completed_items(
    item_not_started,
    item_in_progress,
    item_done_before_today,
    item_done_today
):
    return ViewModel(
        [item_not_started],
        [item_in_progress],
        [item_done_before_today, item_done_today]
    )


@pytest.fixture
def view_model_with_six_completed_items_hiding_old(
    item_not_started,
    item_in_progress,
    item_done_before_today,
    item_done_today
):
    return ViewModel(
        [item_not_started],
        [item_in_progress],
        [item_done_before_today, item_done_today] * 3
    )


@pytest.fixture
def view_model_with_six_completed_items_showing_old(
    item_not_started,
    item_in_progress,
    item_done_before_today,
    item_done_today
):
    return ViewModel(
        [item_not_started],
        [item_in_progress],
        [item_done_before_today, item_done_today] * 3,
        show_all_items=True
    )


@freeze_time("2021-01-02")
class TestViewModel:
    def test_view_model_with_no_items(self, view_model_without_items):
        model = view_model_without_items
        assert model.not_started == []
        assert model.in_progress == []
        assert model.recent_done_items == []
        assert model.high_priority_done_items == []
        assert model.is_hiding_done_items is False

    def test_view_model_with_few_completed_items(
        self,
        view_model_with_two_completed_items,
        item_not_started,
        item_in_progress,
        item_done_today,
        item_done_before_today
    ):
        model = view_model_with_two_completed_items
        assert model.not_started == [item_not_started]
        assert model.in_progress == [item_in_progress]
        assert model.recent_done_items == [item_done_today]
        assert model.high_priority_done_items == [
            item_done_before_today,
            item_done_today
        ]
        assert model._treat_all_done_items_as_high_priority is False
        assert model.is_hiding_done_items is False

    def test_view_model_with_many_done_items_showing_default(
        self,
        view_model_with_six_completed_items_hiding_old,
        item_not_started,
        item_in_progress,
        item_done_today,
        item_done_before_today
    ):
        model = view_model_with_six_completed_items_hiding_old
        assert model.not_started == [item_not_started]
        assert model.in_progress == [item_in_progress]
        assert model.recent_done_items == [item_done_today] * 3
        assert model.high_priority_done_items == [item_done_today] * 3
        assert model._treat_all_done_items_as_high_priority is False
        assert model.is_hiding_done_items is True

    def test_view_model_with_many_done_items_showing_all(
        self,
        view_model_with_six_completed_items_showing_old,
        item_not_started,
        item_in_progress,
        item_done_today,
        item_done_before_today
    ):
        model = view_model_with_six_completed_items_showing_old
        assert model.not_started == [item_not_started]
        assert model.in_progress == [item_in_progress]
        assert model.recent_done_items == [item_done_today] * 3
        assert model.high_priority_done_items == (
            [item_done_before_today, item_done_today] * 3
        )
        assert model._treat_all_done_items_as_high_priority is True
        assert model.is_hiding_done_items is False
