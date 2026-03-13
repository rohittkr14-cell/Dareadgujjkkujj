from telethon import TelegramClient, events
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    InviteToChannelRequest,
    EditAdminRequest,
    EditPhotoRequest
)
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import (
    ChatAdminRights,
    InputChatUploadedPhoto,
    MessageActionChatAddUser,
    MessageActionChatJoinedByLink,
    MessageActionChatEditPhoto,
    MessageActionChatEditTitle,
    MessageActionChatDeletePhoto
)

# API
api_id = 30071429
api_hash = "1e2942cf8ca2ddd5a86acf7bb33ae75c"

# Admin usernames
CREATEGROUP_ADMIN = "hupke"
CREATEADU_ADMIN = "abtiee"

# PFP paths
PFP1 = "pfp.jpg"
PFP2 = "pfp2.jpg"

admin_rights = ChatAdminRights(
    change_info=True,
    post_messages=True,
    edit_messages=True,
    delete_messages=True,
    ban_users=True,
    invite_users=True,
    pin_messages=True,
    add_admins=False,
    anonymous=False,
    manage_call=True
)

client = TelegramClient("session", api_id, api_hash)


async def create_mm_group(event, title, pfp, admin_id):
    try:
        result = await client(CreateChannelRequest(
            title=title,
            about="Always confirm that you are dealing with me and not with an impersonator!",
            megagroup=True
        ))

        chat = result.chats[0]

        admin = await client.get_input_entity(admin_id)
        creator = await client.get_me()

        await client(InviteToChannelRequest(chat, [admin]))

        await client(EditAdminRequest(
            channel=chat,
            user_id=admin,
            admin_rights=admin_rights,
            rank="Middleman"
        ))

        await client(EditAdminRequest(
            channel=chat,
            user_id=creator,
            admin_rights=admin_rights,
            rank="Middleman Group"
        ))

        file = await client.upload_file(pfp)
        await client(EditPhotoRequest(
            channel=chat,
            photo=InputChatUploadedPhoto(file)
        ))

        invite = await client(ExportChatInviteRequest(chat))
        await event.reply(f"✅ Group Created\n\n{invite.link}")

    except Exception as e:
        await event.reply(f"❌ Error:\n{e}")


# tents MM group
@client.on(events.NewMessage(pattern="/creategroup"))
async def tents_group(event):
    sender = await event.get_sender()

    if sender.username != CREATEGROUP_ADMIN:
        return  # ignore others

    await create_mm_group(
        event,
        "tents MM || @Middlemem",
        PFP1,
        CREATEGROUP_ADMIN
    )


# Adu MM group
@client.on(events.NewMessage(pattern="/createadu"))
async def adu_group(event):
    sender = await event.get_sender()

    if sender.username != CREATEADU_ADMIN:
        return  # ignore others

    await create_mm_group(
        event,
        "Adu MM || @Middlemem",
        PFP2,
        CREATEADU_ADMIN
    )


# Auto delete service messages
@client.on(events.NewMessage)
async def delete_service_messages(event):
    try:
        if isinstance(event.message.action, (
            MessageActionChatAddUser,
            MessageActionChatJoinedByLink,
            MessageActionChatEditPhoto,
            MessageActionChatEditTitle,
            MessageActionChatDeletePhoto
        )):
            await event.delete()
    except:
        pass


print("🔥 Auto MM Group Creator Running...")

client.start()
client.run_until_disconnected()
