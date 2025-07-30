import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from bot.handlers import router
from bot.handlers import get_chat_id,get_translate,show_help,handle_water_on
from aiogram.types import Message

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


@pytest.mark.asyncio
async def test_get_chat_id():
 
    message = AsyncMock()
    message.text = "/myid"
    message.chat = AsyncMock()
    message.chat.id = 123456789  
    message.answer = AsyncMock()

    await get_chat_id(message)

    message.answer.assert_called_once()
    args, kwargs = message.answer.call_args
    expected_text = f"Ваш chat_id: {message.chat.id}. Нужен для входа на сайт"
    assert expected_text == args[0]


@pytest.mark.asyncio
async def test_get_translate():
    message = AsyncMock(spec=Message)
    message.text = "/translate"
    message.answer = AsyncMock()

    await get_translate(message)

    assert message.answer.call_count == 2

    first_call_args = message.answer.call_args_list[0][0][0]
    second_call_args = message.answer.call_args_list[1][0][0]

    assert "ℹ️ You are already registered in the system." == first_call_args
    assert "What do you want to do?" == second_call_args

    second_call_kwargs = message.answer.call_args_list[1][1]
    assert 'reply_markup' in second_call_kwargs

@pytest.mark.asyncio
async def test_show_help():
    message = AsyncMock(spec=Message)
    message.text = "/help"
    message.answer = AsyncMock()

    await show_help(message)

    message.answer.assert_called_once()

    sent_text = message.answer.call_args[1]['text']
    assert "Список доступных команд" in sent_text
    assert "/start - Начать работу с ботом" in sent_text

    assert message.answer.call_args[1]['parse_mode'] == "HTML"

    assert 'reply_markup' in message.answer.call_args[1]


@pytest.mark.asyncio
@patch("bot.handlers.update_water")
@patch("bot.handlers.redis_manager")
@patch("bot.handlers.get_move_keyboard", new_callable=AsyncMock)
async def test_handle_water_on(mock_get_move_keyboard, mock_redis_manager, mock_update_water):
    message = AsyncMock(spec=Message)
    
    message.from_user = AsyncMock()
    message.from_user.id = 123
    
    message.answer = AsyncMock()

    mock_get_move_keyboard.return_value = "keyboard_mock"
    await handle_water_on(message)

    mock_update_water.assert_called_once_with(123, True)
    mock_redis_manager.save_water_stats.assert_called_once()
    mock_get_move_keyboard.assert_awaited_once_with(123)
    message.answer.assert_awaited_once_with("Полив включен", reply_markup="keyboard_mock")