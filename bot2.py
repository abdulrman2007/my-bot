from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import json
import os

# التوكن الثاني
TOKEN = "8099050765:AAHDzPVK4bGFmEUfbp0FR-VE41HuKNybDZw"

# إعدادات إعادة التشغيل التلقائي
import signal
import sys

def restart_handler(signum, frame):
    """إعادة تشغيل البوت تلقائياً عند الخطأ"""
    print("⚠️ حدث خطأ، جاري إعادة التشغيل...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

UNIVERSITY_URL = "https://sabu.edu.ly/website/login.php"

# ملف التخزين
DATA_FILE = "bot_data2.json"

# الأدمن
ADMIN_ID = None


# =====================================================
# نظام التخزين
# =====================================================

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "subjects": {
            "first_math": "رياضيات I",
            "first_computer": "علم الحاسب I",
            "first_english": "اللغة الإنجليزية I",
            "first_arabic": "اللغة العربية I",
            "first_statistics": "الإحصاء I",
            "first_physics": "الفيزياء I",
            "second_math": "رياضيات II",
            "second_english": "اللغة الإنجليزية II",
            "second_arabic": "اللغة العربية II",
            "second_it": "مقدمة في تقنية المعلومات II",
            "second_logic": "الدوائر المنطقية II",
        },
        "questions": {},
        "videos": {},
        "notes": {},
        "exams": "لا توجد جداول مضافة حاليًا.",
        "portal_link": UNIVERSITY_URL,
        "contact_info": """
الاسم: عبدالرحمن ارحومة
الهاتف: 0927668335
البريد الإلكتروني: Am7324277@gmail.com
""",
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


DATA = load_data()


# =====================================================
# القائمة الرئيسية
# =====================================================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📚 الفصل الأول", callback_data="first_term"),
            InlineKeyboardButton("📘 الفصل الثاني", callback_data="second_term"),
        ],
        [
            InlineKeyboardButton("📝 بنك الأسئلة", callback_data="question_bank"),
            InlineKeyboardButton("🎥 المواد الدراسية", callback_data="study_materials"),
        ],
        [
            InlineKeyboardButton("🧮 حاسبة الدرجات", callback_data="grades"),
            InlineKeyboardButton("📅 جداول الامتحانات", callback_data="exams"),
        ],
        [
            InlineKeyboardButton("📢 الإعلانات", callback_data="announcements"),
            InlineKeyboardButton("🌐 منظومة الجامعة", url=DATA["portal_link"]),
        ],
        [
            InlineKeyboardButton("🆘 المساعدة", callback_data="help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_button(callback_data="main_menu"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 العودة", callback_data=callback_data)]
    ])


# =====================================================
# لوحة الإدارة
# =====================================================

def admin_menu():
    keyboard = [
        [
            InlineKeyboardButton("➕ إضافة مادة", callback_data="admin_add_subject"),
            InlineKeyboardButton("🗑️ حذف مادة", callback_data="admin_delete_subject"),
        ],
        [
            InlineKeyboardButton("➕ إضافة سؤال", callback_data="admin_add_question"),
            InlineKeyboardButton("🗑️ حذف سؤال", callback_data="admin_delete_question"),
        ],
        [
            InlineKeyboardButton("➕ إضافة فيديو", callback_data="admin_add_video"),
            InlineKeyboardButton("🗑️ حذف فيديو", callback_data="admin_delete_video"),
        ],
        [
            InlineKeyboardButton("➕ إضافة ملاحظة PDF", callback_data="admin_add_note"),
            InlineKeyboardButton("🗑️ حذف ملاحظة", callback_data="admin_delete_note"),
        ],
        [
            InlineKeyboardButton("📅 جدول الامتحانات", callback_data="admin_set_exams"),
        ],
        [
            InlineKeyboardButton("🔗 رابط المنظومة", callback_data="admin_set_portal"),
        ],
        [
            InlineKeyboardButton("📞 معلومات التواصل", callback_data="admin_set_contact"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# =====================================================
# أمر البدء
# =====================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.first_name or "الطالب"

    welcome_text = f"""
مرحبًا {username} 👋

أهلًا وسهلًا بك في بوت A⚜️A_Bot 🤖⚜️

أنا بوتك الذكي، صُممت لمساعدتك خلال دراستك في الفصل الدراسي الأول والثاني.

يمكنك من خلالي الوصول إلى:
• المواد الدراسية
• بنك الأسئلة
• الفيديوهات التعليمية
• الشيتات والمذكرات
• الاختبارات التدريبية
• حاسبة الدرجات
• جداول الامتحانات
• الإعلانات والتنبيهات
• منظومة الجامعة

اختر الخدمة التي تريدها من القائمة التالية:
"""
    await update.message.reply_text(welcome_text)
    await update.message.reply_text(
        "🏠 القائمة الرئيسية:",
        reply_markup=main_menu()
    )


# =====================================================
# أمر الأدمن
# =====================================================

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ADMIN_ID
    user = update.effective_user
    ADMIN_ID = user.id
    await update.message.reply_text(
        "⚙️ لوحة التحكم:",
        reply_markup=admin_menu()
    )


def is_admin(user_id):
    return ADMIN_ID is not None and user_id == ADMIN_ID


# =====================================================
# قوائم الفصول
# =====================================================

def get_subjects_by_term(term):
    subjects = {}
    for key, name in DATA["subjects"].items():
        if key.startswith(term):
            subjects[key] = name
    return subjects


def term_menu(term):
    if term == "first":
        title = "📚 الفصل الدراسي الأول"
        questions_callback = "first_questions"
        subjects_callback = "first_subjects"
    else:
        title = "📘 الفصل الدراسي الثاني"
        questions_callback = "second_questions"
        subjects_callback = "second_subjects"

    keyboard = [
        [InlineKeyboardButton("📝 بنك الأسئلة", callback_data=questions_callback)],
        [InlineKeyboardButton("📚 المواد الدراسية", callback_data=subjects_callback)],
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")],
    ]
    return title, InlineKeyboardMarkup(keyboard)


def subjects_menu(subjects, back_callback):
    keyboard = []
    for callback_data, subject_name in subjects.items():
        keyboard.append([InlineKeyboardButton(subject_name, callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    return InlineKeyboardMarkup(keyboard)


def subject_menu(subject_id, back_callback):
    keyboard = [
        [InlineKeyboardButton("🎥 الفيديوهات", callback_data=f"videos_{subject_id}")],
        [
            InlineKeyboardButton("📄 الشيتات", callback_data=f"sheets_{subject_id}"),
            InlineKeyboardButton("📚 المذكرات", callback_data=f"notes_{subject_id}"),
        ],
        [InlineKeyboardButton("📝 بنك الأسئلة", callback_data=f"bank_{subject_id}")],
        [InlineKeyboardButton("✅ اختبار تدريبي", callback_data=f"quiz_{subject_id}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_content_for_subject(content_type, subject_id):
    items = {}
    for key, value in DATA.get(content_type, {}).items():
        if isinstance(value, dict) and value.get("subject") == subject_id:
            items[key] = value
        elif isinstance(value, str) and subject_id in key:
            items[key] = value
    return items


def format_list_items(items, title):
    if not items:
        return f"📂 لا يوجد {title} حالياً."
    text = f"📂 {title}:\n\n"
    for key, info in items.items():
        if isinstance(info, dict):
            display_name = info.get("name", key)
            text += f"• {display_name}\n"
        else:
            text += f"• {info}\n"
    return text


# =====================================================
# معالجة الأزرار
# =====================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # القائمة الرئيسية
    if data == "main_menu":
        await query.edit_message_text("🏠 القائمة الرئيسية:", reply_markup=main_menu())

    # لوحة الأدمن
    elif data == "admin_menu":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        await query.edit_message_text("⚙️ لوحة التحكم:", reply_markup=admin_menu())

    # ==================== إدارة المواد ====================
    elif data == "admin_add_subject":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        context.user_data["admin_step"] = "add_subject_name"
        await query.edit_message_text(
            "➕ **إضافة مادة جديدة**\n\n"
            "أرسل اسم المادة بالصيغة التالية:\n\n"
            "`first_physics: الفيزياء I`\n\n"
            "استخدم `first_` للفصل الأول و `second_` للفصل الثاني.",
            reply_markup=back_button("admin_menu"),
            parse_mode="Markdown"
        )

    elif data == "admin_delete_subject":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        subjects = DATA["subjects"]
        if not subjects:
            await query.edit_message_text("لا توجد مواد لحذفها.", reply_markup=back_button("admin_menu"))
            return
        keyboard = [[InlineKeyboardButton(name, callback_data=f"del_subject_{key}")]
                     for key, name in subjects.items()]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_menu")])
        await query.edit_message_text(
            "🗑️ **حذف مادة**\n\nاختر المادة لحذفها:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ==================== إدارة الأسئلة ====================
    elif data == "admin_add_question":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        subjects = DATA["subjects"]
        keyboard = [[InlineKeyboardButton(name, callback_data=f"add_q_subject_{key}")]
                     for key, name in subjects.items()]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_menu")])
        await query.edit_message_text(
            "➕ **إضافة سؤال**\n\nاختر المادة:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "admin_delete_question":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        questions = DATA.get("questions", {})
        if not questions:
            await query.edit_message_text("لا توجد أسئلة لحذفها.", reply_markup=back_button("admin_menu"))
            return
        keyboard = [[InlineKeyboardButton(str(key)[:40], callback_data=f"del_question_{key}")]
                     for key in questions.keys()]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_menu")])
        await query.edit_message_text(
            "🗑️ **حذف سؤال**\n\nاختر السؤال لحذفه:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ==================== إدارة الفيديوهات ====================
    elif data == "admin_add_video":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        subjects = DATA["subjects"]
        keyboard = [[InlineKeyboardButton(name, callback_data=f"add_v_subject_{key}")]
                     for key, name in subjects.items()]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_menu")])
        await query.edit_message_text(
            "➕ **إضافة فيديو**\n\nاختر المادة:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "admin_delete_video":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        videos = DATA.get("videos", {})
        if not videos:
            await query.edit_message_text("لا توجد فيديوهات لحذفها.", reply_markup=back_button("admin_menu"))
            return
        keyboard = [[InlineKeyboardButton(str(key)[:40], callback_data=f"del_video_{key}")]
                     for key in videos.keys()]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_menu")])
        await query.edit_message_text(
            "🗑️ **حذف فيديو**\n\nاختر الفيديو لحذفه:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ==================== إدارة الملاحظات PDF ====================
    elif data == "admin_add_note":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        subjects = DATA["subjects"]
        keyboard = [[InlineKeyboardButton(name, callback_data=f"add_n_subject_{key}")]
                     for key, name in subjects.items()]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_menu")])
        await query.edit_message_text(
            "➕ **إضافة ملاحظة PDF**\n\nاختر المادة:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "admin_delete_note":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        notes = DATA.get("notes", {})
        if not notes:
            await query.edit_message_text("لا توجد ملاحظات لحذفها.", reply_markup=back_button("admin_menu"))
            return
        keyboard = []
        for key, info in notes.items():
            display_name = info.get("name", key) if isinstance(info, dict) else key
            keyboard.append([InlineKeyboardButton(display_name[:40], callback_data=f"del_note_{key}")])
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="admin_menu")])
        await query.edit_message_text(
            "🗑️ **حذف ملاحظة PDF**\n\nاختر الملاحظة لحذفها:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ==================== إعدادات أخرى ====================
    elif data == "admin_set_exams":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        context.user_data["admin_step"] = "set_exams"
        await query.edit_message_text(
            "📅 **تعديل جدول الامتحانات**\n\nأرسل النص الجديد:",
            reply_markup=back_button("admin_menu"),
            parse_mode="Markdown"
        )

    elif data == "admin_set_portal":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        context.user_data["admin_step"] = "set_portal"
        await query.edit_message_text(
            "🔗 **تعديل رابط المنظومة**\n\nأرسل الرابط الجديد:",
            reply_markup=back_button("admin_menu"),
            parse_mode="Markdown"
        )

    elif data == "admin_set_contact":
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        context.user_data["admin_step"] = "set_contact"
        await query.edit_message_text(
            "📞 **تعديل معلومات التواصل**\n\nأرسل المعلومات الجديدة:",
            reply_markup=back_button("admin_menu"),
            parse_mode="Markdown"
        )

    # ==================== حذف فعلي ====================
    elif data.startswith("del_subject_"):
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        subject_key = data.replace("del_subject_", "")
        if subject_key in DATA["subjects"]:
            del DATA["subjects"][subject_key]
            save_data(DATA)
            await query.edit_message_text(
                f"✅ تم حذف المادة.",
                reply_markup=back_button("admin_menu")
            )
        else:
            await query.edit_message_text("❌ المادة غير موجودة.", reply_markup=back_button("admin_menu"))

    elif data.startswith("del_question_"):
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        question_key = data.replace("del_question_", "")
        if question_key in DATA["questions"]:
            del DATA["questions"][question_key]
            save_data(DATA)
            await query.edit_message_text(
                f"✅ تم حذف السؤال.",
                reply_markup=back_button("admin_menu")
            )
        else:
            await query.edit_message_text("❌ السؤال غير موجود.", reply_markup=back_button("admin_menu"))

    elif data.startswith("del_video_"):
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        video_key = data.replace("del_video_", "")
        if video_key in DATA["videos"]:
            del DATA["videos"][video_key]
            save_data(DATA)
            await query.edit_message_text(
                f"✅ تم حذف الفيديو.",
                reply_markup=back_button("admin_menu")
            )
        else:
            await query.edit_message_text("❌ الفيديو غير موجود.", reply_markup=back_button("admin_menu"))

    elif data.startswith("del_note_"):
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        note_key = data.replace("del_note_", "")
        if note_key in DATA["notes"]:
            del DATA["notes"][note_key]
            save_data(DATA)
            await query.edit_message_text(
                f"✅ تم حذف الملاحظة.",
                reply_markup=back_button("admin_menu")
            )
        else:
            await query.edit_message_text("❌ الملاحظة غير موجودة.", reply_markup=back_button("admin_menu"))

    # ==================== اختيار مادة لإضافة سؤال/فيديو/ملاحظة ====================
    elif data.startswith("add_q_subject_"):
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        subject_key = data.replace("add_q_subject_", "")
        context.user_data["admin_step"] = "add_question"
        context.user_data["admin_subject"] = subject_key
        await query.edit_message_text(
            f"➕ **إضافة سؤال لـ {DATA['subjects'][subject_key]}**\n\n"
            "أرسل اسم السؤال، ثم أرسل الملف (PDF/صورة/نص):",
            reply_markup=back_button("admin_menu"),
            parse_mode="Markdown"
        )

    elif data.startswith("add_v_subject_"):
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        subject_key = data.replace("add_v_subject_", "")
        context.user_data["admin_step"] = "add_video"
        context.user_data["admin_subject"] = subject_key
        await query.edit_message_text(
            f"➕ **إضافة فيديو لـ {DATA['subjects'][subject_key]}**\n\n"
            "أرسل اسم الفيديو، ثم أرسل ملف الفيديو:",
            reply_markup=back_button("admin_menu"),
            parse_mode="Markdown"
        )

    elif data.startswith("add_n_subject_"):
        if not is_admin(update.effective_user.id):
            await query.edit_message_text("⛔ هذا الأمر للأدمن فقط.")
            return
        subject_key = data.replace("add_n_subject_", "")
        context.user_data["admin_step"] = "add_note"
        context.user_data["admin_subject"] = subject_key
        await query.edit_message_text(
            f"➕ **إضافة ملاحظة PDF لـ {DATA['subjects'][subject_key]}**\n\n"
            "أرسل اسم الملاحظة، ثم أرسل ملف PDF:",
            reply_markup=back_button("admin_menu"),
            parse_mode="Markdown"
        )

    # ==================== قائمة المواد حسب الفصل ====================
    elif data == "first_term":
        title, keyboard = term_menu("first")
        await query.edit_message_text(f"{title}\n\nاختر القسم المطلوب:", reply_markup=keyboard)

    elif data == "second_term":
        title, keyboard = term_menu("second")
        await query.edit_message_text(f"{title}\n\nاختر القسم المطلوب:", reply_markup=keyboard)

    elif data == "first_subjects":
        subjects = get_subjects_by_term("first")
        await query.edit_message_text(
            "📚 مواد الفصل الدراسي الأول\n\nاختر المادة:",
            reply_markup=subjects_menu(subjects, "first_term")
        )

    elif data == "second_subjects":
        subjects = get_subjects_by_term("second")
        await query.edit_message_text(
            "📘 مواد الفصل الدراسي الثاني\n\nاختر المادة:",
            reply_markup=subjects_menu(subjects, "second_term")
        )

    elif data == "first_questions":
        subjects = get_subjects_by_term("first")
        await query.edit_message_text(
            "📝 بنك أسئلة الفصل الأول\n\nاختر المادة:",
            reply_markup=subjects_menu(subjects, "first_term")
        )

    elif data == "second_questions":
        subjects = get_subjects_by_term("second")
        await query.edit_message_text(
            "📝 بنك أسئلة الفصل الثاني\n\nاختر المادة:",
            reply_markup=subjects_menu(subjects, "second_term")
        )

    elif data == "question_bank":
        keyboard = [
            [InlineKeyboardButton("الفصل الأول", callback_data="first_questions")],
            [InlineKeyboardButton("الفصل الثاني", callback_data="second_questions")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "📝 بنك الأسئلة\n\nاختر الفصل الدراسي:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "study_materials":
        keyboard = [
            [InlineKeyboardButton("الفصل الأول", callback_data="first_subjects")],
            [InlineKeyboardButton("الفصل الثاني", callback_data="second_subjects")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "🎥 المواد الدراسية\n\nاختر الفصل الدراسي:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # اختيار مادة
    elif data in DATA["subjects"]:
        subject_id = data
        subject_name = DATA["subjects"][subject_id]
        await query.edit_message_text(
            f"📚 {subject_name}\n\nاختر المحتوى المطلوب:",
            reply_markup=subject_menu(subject_id, "first_subjects" if "first" in subject_id else "second_subjects")
        )

    # محتوى المادة
    elif data.startswith("videos_"):
        subject_id = data.replace("videos_", "")
        subject_name = DATA["subjects"].get(subject_id, subject_id)
        videos = get_content_for_subject("videos", subject_id)
        text = format_list_items(videos, f"🎥 فيديوهات {subject_name}")
        await query.edit_message_text(text, reply_markup=back_button(f"subject_{subject_id}"))

    elif data.startswith("sheets_"):
        subject_id = data.replace("sheets_", "")
        subject_name = DATA["subjects"].get(subject_id, subject_id)
        notes = get_content_for_subject("notes", subject_id)
        text = format_list_items(notes, f"📄 شيتات {subject_name}")
        await query.edit_message_text(text, reply_markup=back_button(f"subject_{subject_id}"))

    elif data.startswith("notes_"):
        subject_id = data.replace("notes_", "")
        subject_name = DATA["subjects"].get(subject_id, subject_id)
        notes = get_content_for_subject("notes", subject_id)
        text = format_list_items(notes, f"📚 مذكرات {subject_name}")
        await query.edit_message_text(text, reply_markup=back_button(f"subject_{subject_id}"))

    elif data.startswith("bank_"):
        subject_id = data.replace("bank_", "")
        subject_name = DATA["subjects"].get(subject_id, subject_id)
        questions = get_content_for_subject("questions", subject_id)
        text = format_list_items(questions, f"📝 بنك أسئلة {subject_name}")
        await query.edit_message_text(text, reply_markup=back_button(f"subject_{subject_id}"))

    elif data.startswith("quiz_"):
        subject_id = data.replace("quiz_", "")
        subject_name = DATA["subjects"].get(subject_id, subject_id)
        await query.edit_message_text(
            f"✅ الاختبار التدريبي لـ {subject_name}\n\nهذا القسم جاهز لاستقبال الاختبارات.",
            reply_markup=back_button(f"subject_{subject_id}")
        )

    elif data.startswith("subject_"):
        subject_id = data.replace("subject_", "")
        subject_name = DATA["subjects"].get(subject_id, subject_id)
        back_cb = "first_subjects" if "first" in subject_id else "second_subjects"
        await query.edit_message_text(
            f"📚 {subject_name}\n\nاختر المحتوى المطلوب:",
            reply_markup=subject_menu(subject_id, back_cb)
        )

    # حاسبة الدرجات
    elif data == "grades":
        context.user_data.clear()
        context.user_data["grade_step"] = "final"
        await query.message.reply_text(
            """
🧮 حاسبة الدرجات

طريقة الحساب:

• النهائي: 60 درجة
• النصفي: 30 درجة
• أعمال الفصل: 10 درجات

أرسل درجة الامتحان النهائي من 60:
"""
        )

    # جداول الامتحانات
    elif data == "exams":
        await query.edit_message_text(
            f"📅 جداول الامتحانات\n\n{DATA['exams']}",
            reply_markup=back_button()
        )

    # الإعلانات
    elif data == "announcements":
        await query.edit_message_text(
            "📢 الإعلانات والتنبيهات\n\nلا توجد إعلانات جديدة حالياً.",
            reply_markup=back_button()
        )

    # المساعدة
    elif data == "help":
        await query.edit_message_text(
            f"🆘 المساعدة والتواصل\n\n{DATA['contact_info']}",
            reply_markup=back_button()
        )

    else:
        await query.edit_message_text(
            """
📂 هذا القسم جاهز لاستقبال المحتوى.

يمكنك إضافة:
• الفيديوهات
• الصور
• ملفات PDF
• الشيتات
• المذكرات
• بنك الأسئلة
• الاختبارات التدريبية
""",
            reply_markup=back_button()
        )


# =====================================================
# حاسبة الدرجات
# =====================================================

async def grade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("grade_step")
    if not step:
        return

    try:
        value = float(update.message.text.replace(",", "."))
    except ValueError:
        await update.message.reply_text("يرجى إدخال رقم صحيح فقط.")
        return

    limits = {"final": 60, "midterm": 30, "coursework": 10}

    if value < 0 or value > limits[step]:
        await update.message.reply_text(f"أدخل درجة بين 0 و {limits[step]}.")
        return

    context.user_data.setdefault("grades", {})
    context.user_data["grades"][step] = value

    if step == "final":
        context.user_data["grade_step"] = "midterm"
        await update.message.reply_text("أرسل درجة الامتحان النصفي من 30:")
    elif step == "midterm":
        context.user_data["grade_step"] = "coursework"
        await update.message.reply_text("أرسل درجة أعمال الفصل من 10:")
    elif step == "coursework":
        grades = context.user_data["grades"]
        total = grades["final"] + grades["midterm"] + grades["coursework"]

        if total >= 85:
            evaluation = "ممتاز"
        elif total >= 75:
            evaluation = "جيد جداً"
        elif total >= 65:
            evaluation = "جيد"
        elif total >= 50:
            evaluation = "مقبول"
        else:
            evaluation = "يحتاج إلى تحسين"

        await update.message.reply_text(
            f"""
✅ تم حساب الدرجة

النهائي: {grades["final"]}/60
النصفي: {grades["midterm"]}/30
أعمال الفصل: {grades["coursework"]}/10

المجموع: {total}/100
التقييم التقريبي: {evaluation}
""",
            reply_markup=main_menu()
        )
        context.user_data.clear()


# =====================================================
# معالجة إضافة العناصر من الأدمن
# =====================================================

async def admin_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    step = context.user_data.get("admin_step")
    if not step:
        return

    text = update.message.text.strip()

    if step == "add_subject_name":
        if ":" in text:
            key, name = text.split(":", 1)
            key = key.strip()
            name = name.strip()
            DATA["subjects"][key] = name
            save_data(DATA)
            context.user_data.pop("admin_step", None)
            await update.message.reply_text(
                f"✅ تم إضافة المادة: {name}",
                reply_markup=back_button("admin_menu")
            )
        else:
            await update.message.reply_text(
                "❌ الصيغة غير صحيحة. استخدم:\n\n`first_physics: الفيزياء I`",
                reply_markup=back_button("admin_menu"),
                parse_mode="Markdown"
            )

    elif step == "set_exams":
        DATA["exams"] = text
        save_data(DATA)
        context.user_data.pop("admin_step", None)
        await update.message.reply_text("✅ تم تحديث جدول الامتحانات.", reply_markup=back_button("admin_menu"))

    elif step == "set_portal":
        DATA["portal_link"] = text
        save_data(DATA)
        context.user_data.pop("admin_step", None)
        await update.message.reply_text("✅ تم تحديث رابط المنظومة.", reply_markup=back_button("admin_menu"))

    elif step == "set_contact":
        DATA["contact_info"] = text
        save_data(DATA)
        context.user_data.pop("admin_step", None)
        await update.message.reply_text("✅ تم تحديث معلومات التواصل.", reply_markup=back_button("admin_menu"))

    elif step in ("add_question", "add_video", "add_note"):
        context.user_data["admin_item_name"] = text
        if step == "add_question":
            await update.message.reply_text(
                f"الآن أرسل ملف السؤال (PDF أو صورة) للمادة: {DATA['subjects'].get(context.user_data['admin_subject'], '')}",
                reply_markup=back_button("admin_menu")
            )
        elif step == "add_video":
            await update.message.reply_text(
                f"الآن أرسل ملف الفيديو للمادة: {DATA['subjects'].get(context.user_data['admin_subject'], '')}",
                reply_markup=back_button("admin_menu")
            )
        elif step == "add_note":
            await update.message.reply_text(
                f"الآن أرسل ملف PDF للمادة: {DATA['subjects'].get(context.user_data['admin_subject'], '')}",
                reply_markup=back_button("admin_menu")
            )


# =====================================================
# معالجة الملفات المرسلة من الأدمن
# =====================================================

async def admin_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    step = context.user_data.get("admin_step")
    if not step or "add_" not in step:
        return

    item_name = context.user_data.get("admin_item_name", "غير محدد")
    subject_key = context.user_data.get("admin_subject", "")
    item_key = f"{subject_key}_{len(DATA.get(step.replace('add_', ''), {}))}"

    if step == "add_question":
        file_id = None
        if update.message.document:
            file_id = update.message.document.file_id
        elif update.message.photo:
            file_id = update.message.photo[-1].file_id

        if file_id:
            DATA["questions"][item_key] = {
                "name": item_name,
                "file_id": file_id,
                "subject": subject_key
            }
            save_data(DATA)
            context.user_data.pop("admin_step", None)
            context.user_data.pop("admin_item_name", None)
            context.user_data.pop("admin_subject", None)
            await update.message.reply_text(
                f"✅ تم إضافة السؤال: {item_name}",
                reply_markup=back_button("admin_menu")
            )
        else:
            await update.message.reply_text("❌ لم يتم استلام ملف صالح.", reply_markup=back_button("admin_menu"))

    elif step == "add_video":
        file_id = None
        if update.message.video:
            file_id = update.message.video.file_id
        elif update.message.document:
            file_id = update.message.document.file_id

        if file_id:
            DATA["videos"][item_key] = {
                "name": item_name,
                "file_id": file_id,
                "subject": subject_key
            }
            save_data(DATA)
            context.user_data.pop("admin_step", None)
            context.user_data.pop("admin_item_name", None)
            context.user_data.pop("admin_subject", None)
            await update.message.reply_text(
                f"✅ تم إضافة الفيديو: {item_name}",
                reply_markup=back_button("admin_menu")
            )
        else:
            await update.message.reply_text("❌ لم يتم استلام ملف فيديو صالح.", reply_markup=back_button("admin_menu"))

    elif step == "add_note":
        file_id = None
        if update.message.document:
            file_id = update.message.document.file_id

        if file_id:
            DATA["notes"][item_key] = {
                "name": item_name,
                "file_id": file_id,
                "subject": subject_key
            }
            save_data(DATA)
            context.user_data.pop("admin_step", None)
            context.user_data.pop("admin_item_name", None)
            context.user_data.pop("admin_subject", None)
            await update.message.reply_text(
                f"✅ تم إضافة الملاحظة PDF: {item_name}",
                reply_markup=back_button("admin_menu")
            )
        else:
            await update.message.reply_text("❌ لم يتم استلام ملف PDF صالح.", reply_markup=back_button("admin_menu"))


# =====================================================
# تشغيل البوت
# =====================================================

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_text_handler))
    application.add_handler(MessageHandler(
        filters.Document.ALL | filters.VIDEO | filters.PHOTO,
        admin_file_handler
    ))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        grade_handler
    ))

    while True:
        try:
            print("تم تشغيل بوت A⚜️A_Bot (النسخة 2) بنجاح")
            application.run_polling()
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            print("⏳ جاري إعادة التشغيل خلال 5 ثوان...")
            import time
            time.sleep(5)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, restart_handler)
    main()
