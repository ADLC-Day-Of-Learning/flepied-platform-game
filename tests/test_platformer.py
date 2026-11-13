"""Unit tests for platformer game logic in headless mode."""
import os
import pygame
import pytest
import platformer


@pytest.fixture(autouse=True)
def reset_state():
    """Ensure game state is reset before each test."""
    platformer.reset()
    yield
    platformer.reset()


def test_headless_import():
    """Ensure platformer can be imported without launching a display or entering the game loop."""
    assert hasattr(platformer, "Player")
    assert hasattr(platformer, "make_platform")
    assert hasattr(platformer, "reset")
    assert hasattr(platformer, "main")
    assert hasattr(platformer, "update")
    assert hasattr(platformer, "check_coin_collisions")
    assert hasattr(platformer, "check_flag")


def test_initial_game_state():
    """Verify game state initialization and entity counts in headless mode."""
    platformer.reset()
    assert platformer.score == 0
    assert not platformer.won
    assert len(platformer.coins) == platformer.total_coins
    assert platformer.total_coins == 6
    assert platformer.player.rect.x == 40
    assert platformer.player.rect.y == platformer.HEIGHT - 100


def test_coin_collection():
    """Verify colliding with a coin collects it and increments the score."""
    first_coin = platformer.coins[0]
    initial_count = len(platformer.coins)
    platformer.player.rect.center = first_coin.center

    platformer.check_coin_collisions()

    assert platformer.score == 1
    assert len(platformer.coins) == initial_count - 1
    assert first_coin not in platformer.coins


def test_coin_collection_guard_prevents_double_scoring():
    """Verify that coins are not collected when score reaches total_coins."""
    platformer.score = platformer.total_coins
    initial_coins = list(platformer.coins)
    platformer.player.rect.center = initial_coins[0].center

    platformer.check_coin_collisions()

    assert platformer.score == platformer.total_coins
    assert len(platformer.coins) == len(initial_coins)


def test_player_reset():
    """Verify reset restores player position, coins, score, and won status."""
    platformer.player.rect.x = 999
    platformer.player.rect.y = 999
    platformer.score = 5
    platformer.won = True
    platformer.coins.clear()

    platformer.reset()

    assert platformer.score == 0
    assert not platformer.won
    assert len(platformer.coins) == platformer.total_coins
    assert platformer.player.rect.x == 40
    assert platformer.player.rect.y == platformer.HEIGHT - 100


def test_platform_collision_ground_landing():
    """Verify landing on top of a platform stops downward movement and sets on_ground."""
    ground = platformer.make_platform(0, 500, 200, 40)
    player = platformer.Player(50, 470)
    player.vy = 8.0

    player.update([ground])

    assert player.rect.bottom == ground.top
    assert player.vy == 0
    assert player.on_ground is True


def test_platform_collision_head_collision():
    """Verify jumping into platform underside pushes player below it."""
    plat = platformer.make_platform(100, 200, 200, 20)
    # Position player right below the platform moving upward
    player = platformer.Player(150, 222)
    player.vy = -10.0

    player.update([plat])

    assert player.rect.top == plat.bottom
    assert player.vy == 0


def test_platform_collision_horizontal():
    """Verify horizontal collision aligns player with platform edges."""
    plat = platformer.make_platform(200, 300, 100, 50)

    # Move right into platform left edge
    player = platformer.Player(195, 310)
    player.update([plat], keys={
        pygame.K_d: True, pygame.K_RIGHT: False, pygame.K_LEFT: False,
        pygame.K_a: False, pygame.K_SPACE: False, pygame.K_w: False,
        pygame.K_UP: False,
    })
    assert player.rect.right == plat.left

    # Move left into platform right edge
    player = platformer.Player(305, 310)
    player.update([plat], keys={
        pygame.K_a: True, pygame.K_RIGHT: False, pygame.K_LEFT: False,
        pygame.K_d: False, pygame.K_SPACE: False, pygame.K_w: False,
        pygame.K_UP: False,
    })
    assert player.rect.left == plat.right


def test_fall_off_world_respawns():
    """Verify falling off bottom of screen triggers player reset."""
    platformer.player.rect.top = platformer.HEIGHT + 10

    platformer.update()

    assert platformer.player.rect.y == platformer.HEIGHT - 100
    assert platformer.player.rect.x == 40


def test_flag_win_condition():
    """Verify reaching the flag when all coins are collected sets won to True."""
    platformer.score = platformer.total_coins
    platformer.player.rect.center = platformer.flag.center

    platformer.check_flag()

    assert platformer.won is True


def test_draw_headless():
    """Verify draw executes without error in headless mode."""
    platformer.screen = pygame.display.set_mode((platformer.WIDTH, platformer.HEIGHT))
    platformer.font = pygame.font.Font(None, 32)
    platformer.draw()
