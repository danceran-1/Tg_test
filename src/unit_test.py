import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from bot.handlers import router

@pytest.mark.asyncio
async def test_start_command():
    # Создаем мок-объекты
    message = AsyncMock()
    message.text = "/start"
    message.from_user.id = 123
    message.answer = AsyncMock()

    with patch('bot.handlers.router.message') as mock_handler:
       
        from bot.handlers import cmd_start
        await cmd_start(message)
        
       
        message.answer.assert_called_once()
        assert "зарегистрированы" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_help_command():
    message = AsyncMock()
    message.text = "/help"
    message.answer = AsyncMock()

    from bot.handlers import show_help
    await show_help(message)

    message.answer.assert_called_once()
    assert "Список доступных команд" in message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_stats_command():
    # Мокируем Redis
    redis_mock = MagicMock()
    redis_mock.get_daily_water.return_value = 500
    redis_mock.get_weekly_water.return_value = 3500

    message = AsyncMock()
    message.text = "/stats"
    message.answer = AsyncMock()

    with patch('bot.handlers.redis_manager', redis_mock):
        from bot.handlers import get_stats
        await get_stats(message)
        
        message.answer.assert_called_once()
        assert "Ваша статистика" in message.answer.call_args[0][0]  