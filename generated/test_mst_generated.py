import pytest

class MusicScaleTrainer:
    def __init__(self, scales=None):
        self.scales = scales or ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.score = 0
        self.current_scale = None

    def get_scale(self, index):
        if 0 <= index < len(self.scales):
            return self.scales[index]
        raise IndexError("Scale index out of range")

    def input_scale(self, user_input):
        if user_input in self.scales:
            self.current_scale = user_input
            return True
        return False

    def update_score(self, points):
        if points < 0:
            raise ValueError("Points cannot be negative")
        self.score += points

    def display_menu(self):
        return "1. Start\n2. View Score\n3. Exit"

@pytest.fixture
def scale_trainer():
    return MusicScaleTrainer()

def test_initialization_with_default_scales(scale_trainer):
    assert scale_trainer.scales == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert scale_trainer.score == 0

def test_initialization_with_custom_scales():
    custom_scales = ['C#', 'D#', 'E#']
    trainer = MusicScaleTrainer(custom_scales)
    assert trainer.scales == custom_scales

def test_get_scale_valid_index(scale_trainer):
    assert scale_trainer.get_scale(0) == 'C'
    assert scale_trainer.get_scale(2) == 'E'

def test_get_scale_invalid_index(scale_trainer):
    with pytest.raises(IndexError):
        scale_trainer.get_scale(10)

def test_input_scale_valid(scale_trainer):
    assert scale_trainer.input_scale('C') is True
    assert scale_trainer.current_scale == 'C'

def test_input_scale_invalid(scale_trainer):
    assert scale_trainer.input_scale('X') is False
    assert scale_trainer.current_scale is None

def test_update_score_positive(scale_trainer):
    scale_trainer.update_score(10)
    assert scale_trainer.score == 10

def test_update_score_negative(scale_trainer):
    with pytest.raises(ValueError):
        scale_trainer.update_score(-5)

def test_display_menu(scale_trainer):
    expected_menu = "1. Start\n2. View Score\n3. Exit"
    assert scale_trainer.display_menu() == expected_menu

def test_edge_case_empty_scales():
    trainer = MusicScaleTrainer(scales=[])
    with pytest.raises(IndexError):
        trainer.get_scale(0)
    assert trainer.input_scale('C') is False