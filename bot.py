İmport telebot
from telebot import types

TOKEN = '8898418863:AAHmz34BET0LTf9xOs4rOzjxadYN26lkG7o'
bot = telebot.TeleBot(TOKEN)

users = {}
ADMIN_USERNAME = "miracc_65"
NORMAL_HC_FILE_ID = None 
VIP_HC_FILE_ID = None 

transfer_state = {}
temp_admin_files = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    
    if user_id not in users:
        users[user_id] = {"balance": 0, "ref": 0, "username": username}

    user = users[user_id]
    if username:
        user["username"] = username

    if username and username.lower() == ADMIN_USERNAME.lower():
        user["balance"] = 4000

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🎁 Puan Kazan (Davet Et) 🚀')
    btn2 = types.KeyboardButton('💰 Bakiyem 💎')
    btn3 = types.KeyboardButton('⚡ Ultra Hızlı HC Dosyası Al 🌐')
    btn4 = types.KeyboardButton('👑 VIP HC Dosyası Al 🔥')
    btn5 = types.KeyboardButton('💸 Puan Gönder 🤝')
    btn6 = types.KeyboardButton('🛠 7/24 Destek 📞')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    if username and username.lower() == ADMIN_USERNAME.lower():
        bot.send_message(
            message.chat.id, 
            "👑🔥 **Hoş geldin Patron (`@miracc_65`)!** 🔥👑\n\n"
            "✨ Hesabına **4000 Puan** başarıyla tanımlandı! 🚀💯💥",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    bot.send_message(
        message.chat.id, 
        "🚀🌐 **Ultra Hızlı İnternet Botuna Hoş Geldin!** 🌐🚀\n\n"
        "🔥 Kesintisiz, sınırsız ve en yüksek hızda deneyim yaşamak için aşağıdaki menüyü kullanabilirsin! 👇✨",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    username = message.from_user.username or ""
    
    if username.lower() == ADMIN_USERNAME.lower():
        file_id = message.document.file_id
        temp_admin_files[message.chat.id] = file_id
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📥 Normal Olarak Kaydet ✅ 💥", callback_data="save_normal"),
            types.InlineKeyboardButton("👑 VIP Olarak Kaydet 💎 🔥", callback_data="save_vip")
        )
        
        bot.reply_to(
            message, 
            "📂✨ **Dosya Alındı Patron!** 🎯\n\nBu dosyayı hangi kategoriye kaydetmek istersin? Aşağıdan seç 👇🚀", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )
    else:
        bot.reply_to(message, "❌ **Bu işlem sadece yöneticiye aittir!** ⛔")

@bot.callback_query_handler(func=lambda call: call.data in ["save_normal", "save_vip"])
def save_file_callback(call):
    global NORMAL_HC_FILE_ID, VIP_HC_FILE_ID
    chat_id = call.message.chat.id
    
    if chat_id not in temp_admin_files:
        bot.answer_callback_query(call.id, "❌ Süre aşımı! Lütfen dosyayı tekrar gönder. ⚠️", show_alert=True)
        return
        
    file_id = temp_admin_files[chat_id]
    
    if call.data == "save_normal":
        NORMAL_HC_FILE_ID = file_id
        bot.answer_callback_query(call.id, "✅ Başarıyla Normal Dosya olarak kaydedildi! 🚀")
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"✅🎉 **Normal Dosya Başarıyla Kaydedildi!** 🎯💥\n\n📌 *ID:* `{NORMAL_HC_FILE_ID}`",
            parse_mode="Markdown"
        )
    elif call.data == "save_vip":
        VIP_HC_FILE_ID = file_id
        bot.answer_callback_query(call.id, "👑💎 Başarıyla VIP Dosya olarak kaydedildi! 🔥")
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"👑💎 **VIP Dosyası Başarıyla Kaydedildi!** 🎯🔥\n\n📌 *VIP ID:* `{VIP_HC_FILE_ID}`",
            parse_mode="Markdown"
        )
    
    del temp_admin_files[chat_id]

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    
    if user_id not in users:
        users[user_id] = {"balance": 0, "ref": 0, "username": username}
        
    user = users[user_id]
    if username:
        user["username"] = username

    if username and username.lower() == ADMIN_USERNAME.lower():
        if user["balance"] < 4000:
            user["balance"] = 4000

    text = message.text.strip()
    
    if user_id in transfer_state and "target" in transfer_state[user_id]:
        target_username = transfer_state[user_id]["target"]
        try:
            amount = int(text)
        except ValueError:
            bot.send_message(message.chat.id, "❌ **Lütfen geçerli bir sayı (puan miktarı) yaz!** Örn: `50` ⚠️", parse_mode="Markdown")
            return
            
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ **Gönderilecek miktar 0'dan büyük olmalıdır!** ⚠️")
            return
            
        if user["balance"] < amount:
            bot.send_message(message.chat.id, "❌ **Yetersiz bakiye!** Göndermek istediğin kadar puanın yok. 💸😢")
            del transfer_state[user_id]
            return
            
        target_id = None
        for uid, udata in users.items():
            if udata["username"].lower() == target_username.lower():
                target_id = uid
                break
                
        if not target_id:
            bot.send_message(message.chat.id, "❌ **Bu kullanıcı botu daha önce hiç başlatmamış veya bulunamadı!** 🔍⚠️")
            del transfer_state[user_id]
            return
            
        if user_id == target_id:
            bot.send_message(message.chat.id, "❌ **Kendine puan gönderemezsin!** 😄🎉")
            del transfer_state[user_id]
            return
            
        user["balance"] -= amount
        users[target_id]["balance"] += amount
        
        bot.send_message(message.chat.id, f"✅ **Başarıyla @{target_username} adlı kullanıcıya {amount} Puan gönderildi!** 💸🎉🚀", parse_mode="Markdown")
        
        try:
            bot.send_message(target_id, f"🎉🎁 **Sana @{username or 'Birisi'} tarafından {amount} Puan gönderildi!** 💰🚀✨", parse_mode="Markdown")
        except:
            pass
            
        del transfer_state[user_id]
        return

    if text.startswith('@'):
        target_username = text.replace("@", "")
        transfer_state[user_id] = {"target": target_username}
        bot.send_message(
            message.chat.id, 
            f"🎯 **Hedef Kullanıcı:** `@{target_username}` 👤\n\n"
            f"💰 **Şimdi bu kullanıcıya göndermek istediğin puan miktarını rakam olarak yaz** (Örn: `50`): 👇✨",
            parse_mode="Markdown"
        )
        return

    if text == '💰 Bakiyem 💎' or text == '💰 Bakiyem':
        bot.send_message(
            message.chat.id, 
            f"📊💼 **Hesap Bilgilerin:** 🌟\n\n"
            f"💰 Güncel Puanın: **{user['balance']} Puan** 🚀🔥\n"
            f"👥 Davet Ettiğin Kişi: **{user['ref']}** 🎯",
            parse_mode="Markdown"
        )
        
    elif text == '🎁 Puan Kazan (Davet Et) 🚀' or text == '🎁 Puan Kazan (Davet Et)':
        bot_info = bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        bot.send_message(
            message.chat.id, 
            f"🎁🔥 **Puan Kazanma Sistemi** 🔥🎁\n\n"
            f"✨ Arkadaşlarını davet ederek bolca puan topla, dosyayı bedavaya kap! 🚀💯\n\n"
            f"🔗 **Sana Özel Davet Linkin:**\n`{ref_link}` 🎯",
            parse_mode="Markdown"
        )
        
    elif text == '💸 Puan Gönder 🤝' or text == '💸 Puan Gönder':
        bot.send_message(
            message.chat.id, 
            "💸🤝 **Puan Transferi** 🤝💸\n\n"
            "Başka bir kullanıcıya puan göndermek çok kolay! ⚡\n"
            "👉 Sadece sohbet kısmına göndermek istediğin kişinin kullanıcı adını yaz (Örn: `@kullaniciadi`) 👇✨",
            parse_mode="Markdown"
        )
        
    elif text == '⚡ Ultra Hızlı HC Dosyası Al 🌐' or text == '⚡ Ultra Hızlı HC Dosyası Al':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 Normal Dosya İndir (50 Puan) 💥🚀", callback_data="buy_hc")
        )
        bot.send_message(
            message.chat.id, 
            "🌐⚡ **HTTP Custom Normal Yapılandırma** ⚡🌐\n\n"
            "✨ *Paket Özellikleri:*\n"
            "• 🚀 Hızlı & Stabil Bağlantı 📶\n"
            "• 💥 HTTP Custom ile Uyumlu 🎯\n\n"
            "💳 **Gereken Tutar:** **50 Puan** 💎🔥", 
            reply_markup=markup,
            parse_mode="Markdown"
        )

    elif text == '👑 VIP HC Dosyası Al 🔥' or text == '👑 VIP HC Dosyası Al':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👑💎 VIP Dosya İndir (100 Puan) 🔥💯", callback_data="buy_vip_hc")
        )
        bot.send_message(
            message.chat.id, 
            "👑💎 **HTTP Custom VIP Özel Yapılandırma** 💎👑\n\n"
            "✨ *VIP Paket Özellikleri:*\n"
            "• 🚀 Sınırsız Hız & En Düşük Ping 🌐\n"
            "• 🔒 Özel Hat, Asla Kopma Yapmaz! ⚡\n\n"
            "💳 **Gereken Tutar:** **100 Puan** 🎯🔥", 
            reply_markup=markup,
            parse_mode="Markdown"
        )
        
    elif text == '🛠 7/24 Destek 📞' or text == '🛠 7/24 Destek':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💬 Yetkiliye Hemen Yaz 🚀🔥", url=f"https://t.me/{ADMIN_USERNAME}"))
        bot.send_message(message.chat.id, "🛠🤝 **Herhangi bir sorun, soru veya yardıma ihtiyacın olduğunda aşağıdaki butondan destek alabilirsin!** 👇✨", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["buy_hc", "buy_vip_hc"])
def callback_query(call):
    global NORMAL_HC_FILE_ID, VIP_HC_FILE_ID
    user_id = call.from_user.id
    username = call.from_user.username or ""
    
    if user_id not in users:
        users[user_id] = {"balance": 0, "ref": 0, "username": username}
        
    user = users[user_id]
    
    if call.data == "buy_hc":
        cost = 50
        if user["balance"] >= cost:
            user["balance"] -= cost
            bot.answer_callback_query(call.id, "✅ Ödeme onaylandı, normal dosya gönderiliyor! 🚀💥")
            
            caption_text = (
                "🎉🎉🎊 **Tebrikler! Dosyanız Başarıyla Gönderildi.** 🚀🔥\n\n"
                "📁 Dosya Adı: `Chat . Gpt . hc`\n"
                "⚡ Hız Durumu: Ultra Hızlı & Düşük Ping 🌐\n"
                "📱 Uygulama: HTTP Custom üzerinde sorunsuz çalışır! ✅\n\n"
                "İyi günlerde kullan, bağlantının tadını çıkar! 💥🎯"
            )
            
            if NORMAL_HC_FILE_ID:
                bot.send_document(call.message.chat.id, NORMAL_HC_FILE_ID, caption=caption_text, parse_mode="Markdown")
            else:
                bot.send_message(call.message.chat.id, "❌ **Normal dosya henüz yüklenmemiş!** ⚠️")
        else:
            bot.answer_callback_query(call.id, f"❌ Yetersiz puan! Gereken: {cost} Puan. ⚠️", show_alert=True)
            
    elif call.data == "buy_vip_hc":
        cost = 100
        if user["balance"] >= cost:
            user["balance"] -= cost
            bot.answer_callback_query(call.id, "👑💎 Ödeme onaylandı, VIP dosya gönderiliyor! 🔥💯")
            
            caption_text = (
                "👑🔥 **Tebrikler! VIP Dosyanız Başarıyla Gönderildi.** 💎🚀✨\n\n"
                "📁 Dosya Adı: `VİP DOSYA ∞ 🌐 .hc`\n"
                "⚡ Hız Durumu: Sınırsız Hız & Ultra Düşük Ping 🌐\n"
                "🔒 Uygulama: Özel Hat / HTTP Custom Uyumlu! ✅\n\n"
                "İyi günlerde kullan patron! 🎯"
            )
            
            if VIP_HC_FILE_ID:
                bot.send_document(call.message.chat.id, VIP_HC_FILE_ID, caption=caption_text, parse_mode="Markdown")
            else:
                bot.send_message(call.message.chat.id, "❌ **VIP dosya henüz yüklenmemiş!** ⚠️")
        else:
            bot.answer_callback_query(call.id, f"❌ Yetersiz puan! VIP dosya için gereken: {cost} Puan. ⚠️", show_alert=True)

if __name__ == '__main__':
    print("Bot hatasız çalışıyor ve aktif! 🚀🔥")
    bot.infinity_polling()
