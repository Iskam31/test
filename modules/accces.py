async def getAdmins (bot, message) :
    admins = await bot.get_chat_administrators(chat_id=message.chat.id)
    res = []
    for admin in admins:
        if (admin.user.last_name == None): admin.user.last_name = ''
        res.append({
          'name': ' '.join([admin.user.first_name, admin.user.last_name]),
          'id' : admin.user.id,
          'status' : admin.status
        })
    await message.reply(res)
    return res
