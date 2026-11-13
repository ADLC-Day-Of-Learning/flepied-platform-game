"""Pytest fixtures for headless Pygame test execution."""
import os
import pygame
import pytest

# Set dummy drivers before any SDL initialization occurs
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"


@pytest.fixture(autouse=True)
def headless_pygame(monkeypatch):
    """Ensure SDL uses dummy video and audio drivers for headless testing."""
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    yield
    pygame.quit()
