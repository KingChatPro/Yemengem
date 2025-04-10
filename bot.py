from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
import random

# إعدادات التوكن واللعبة
TOKEN = "ضع_توكن_البوت_هنا"
GAME_URL = "https://github.com/KingChatPro/Yemengem/new/main"  # رابط اللعبة على GitHub Pages

# تفعيل السجلات لمراقبة الأخطاء
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# إضافة خاصية leaderboard للمنافسة بين اللاعبين
players_scores = {}

# دالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_text = f"مرحباً {user.first_name}! أهلاً بك في لعبة بناء المنازل."
    keyboard = [
        [InlineKeyboardButton("ابدأ بناء المنزل", url=GAME_URL)],
        [InlineKeyboardButton("إظهار ترتيب اللاعبين", callback_data='leaderboard')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# دالة leaderboard لعرض ترتيب اللاعبين
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaderboard_text = "ترتيب اللاعبين:\n"
    sorted_players = sorted(players_scores.items(), key=lambda x: x[1], reverse=True)
    for index, (player, score) in enumerate(sorted_players[:10], 1):
        leaderboard_text += f"{index}. {player}: {score} نقاط\n"
    
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(leaderboard_text)

# دالة تحديث النقاط (يتم استدعاؤها في اللعبة عند إتمام المهمة)
async def update_score(user_id: int, score: int):
    if user_id in players_scores:
        players_scores[user_id] += score
    else:
        players_scores[user_id] = score

# دالة عند انتهاء اللعبة أو إتمام مهمة
async def end_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    score = random.randint(10, 100)  # تخيل أن النقاط تتولد بناءً على أداء اللعبة
    await update_score(user_id, score)
    
    await update.message.reply_text(f"تهانينا! لقد انتهيت من بناء المنزل وحصلت على {score} نقاط!")

# إضافة أوامر جديدة للـ help والمساعدة
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    أهلاً بك في لعبة بناء المنازل! إليك بعض الأوامر التي يمكنك استخدامها:
    - /start: لبدء اللعبة.
    - /leaderboard: لعرض ترتيب اللاعبين.
    - /end_game: لإتمام اللعبة وحساب النقاط.
    """
    await update.message.reply_text(help_text)

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("end_game", end_game))
    app.add_handler(CallbackQueryHandler(leaderboard, pattern='leaderboard'))

    print("بوت 'Yemen gem' قيد التشغيل...")
    print("تم! تهانينا على البوت الجديد. يمكنك الوصول إليه عبر الرابط: t.me/Yemsengem_bot")
    print("يمكنك الآن إضافة وصف وصورة للبروفايل الخاصة بالبوت.")
    print("لا تنسى إضافة قسم الوصف واسم المستخدم بشكل جيد عند الانتهاء.")
    print("استخدم هذا التوكن للوصول إلى واجهة الـ API:")
    print(TOKEN)
    print("احتفظ بتوكن البوت بشكل آمن لأنه يمكن لأي شخص استخدامه للتحكم في البوت.")
    print("لمزيد من المعلومات حول واجهة API للبوت، يمكنك زيارة: https://core.telegram.org/bots/api")

    app.run_polling()
