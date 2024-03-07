import aioschedule, asyncio
from utils.functions.get_bot_and_db import get_bot_and_db


async def update_rating():
    bot, db = get_bot_and_db()
    users_ids = db.get_users_ids()

    for user_id in users_ids:
        db.rating_to_null(tg_id=user_id)

    return


async def scheduler():
    aioschedule.every().monday.at("00:00").do(update_rating) # 12:00


    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)


async def main_schedule():
    await asyncio.create_task(scheduler())


if __name__ == '__main__':
    asyncio.run(main_schedule())