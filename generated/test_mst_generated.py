import pytest

class MusicScaleTrainer:
    def __init__(self):
        self.scales = {
            "C Major": ["C", "D", "E", "F", "G", "A", "B"],
            "G Major": ["G", "A", "B", "C", "D", "E", "F#"],
        }
        self.score = 0

    def get_scale(self, scale_name):
        return self.scales.get(scale_name, None)

    def input_scale(self, scale_name, user_input):
        correct_scale = self.get_scale(scale_name)
        return correct_scale == user_input.split()

    def update_score(self, correct):
        if correct:
            self.score += 1
        return self.score

    def display_menu(self):
        return "1. C Major\n2. G Major\n3. Exit"


def test_class_initialization():
    trainer = MusicScaleTrainer()
    assert trainer.scales is not None
    assert trainer.score == 0


def test_scale_data_access_valid():
    trainer = MusicScaleTrainer()
    assert trainer.get_scale("C Major") == ["C", "D", "E", "F", "G", "A", "B"]


def test_scale_data_access_invalid():
    trainer = MusicScaleTrainer()
    assert trainer.get_scale("A Minor") is None


def test_user_input_handling_correct():
    trainer = MusicScaleTrainer()
    assert trainer.input_scale("C Major", "C D E F G A B") is True


def test_user_input_handling_incorrect():
    trainer = MusicScaleTrainer()
    assert trainer.input_scale("C Major", "C D E F G A") is False


def test_score_tracking_increase():
    trainer = MusicScaleTrainer()
    trainer.update_score(True)
    assert trainer.score == 1


def test_score_tracking_no_increase():
    trainer = MusicScaleTrainer()
    trainer.update_score(False)
    assert trainer.score == 0


def test_menu_display():
    trainer = MusicScaleTrainer()
    expected_menu = "1. C Major\n2. G Major\n3. Exit"
    assert trainer.display_menu() == expected_menu


def test_edge_case_empty_scale():
    trainer = MusicScaleTrainer()
    assert trainer.get_scale("") is None


def test_edge_case_nonexistent_scale():
    trainer = MusicScaleTrainer()
    assert trainer.get_scale("Nonexistent Scale") is None


def test_edge_case_score_negative():
    trainer = MusicScaleTrainer()
    trainer.update_score(False)  # Should not decrease score but simulating edge case
    assert trainer.score == 0  # Test should be valid as no decrement is implemented