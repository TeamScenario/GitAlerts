import sys, re
from logging import basicConfig, getLogger, INFO
from flask import Flask, request, jsonify
from html import escape
from requests import get, post
from os import environ
import config

from telegram.ext import (
      CommandHandler,
      Updater,
      CallbackContext,
)

from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update,
    ParseMode,
)

server = Flask(__name__)

basicConfig(level=INFO)
log = getLogger()

ENV = bool(environ.get('ENV', False))

if ENV:
    BOT_TOKEN = environ.get('BOT_TOKEN', None)
    PROJECT_NAME = environ.get('PROJECT_NAME', None)
    ip_addr = environ.get('APP_URL', None)
    HEROKU_APPNAME = environ.get("HEROKU_APPNAME", "gitalertbot")
    GIT_REPO_URL = environ.get('GIT_REPO_URL', "https://github.com/TeamScenario/GitAlerts")
else:
    BOT_TOKEN = config.BOT_TOKEN
    PROJECT_NAME = config.PROJECT_NAME
    ip_addr = get('https://api.ipify.org').text
    GIT_REPO_URL = config.GIT_REPO_URL
    HEROKU_APPNAME = config.HEROKU_APPNAME

updater = Updater(token=BOT_TOKEN, workers=1)
dispatcher = updater.dispatcher

log.info("If you need more help, join @ScenarioXsupport in Telegram.")

xa = bytearray.fromhex("54 65 61 6D 53 63 65 6E 61 72 69 6F 2F 47 69 74 41 6C 65 72 74 73").decode()
axx = bytearray.fromhex("43 6F 64 65 72 58").decode()
xxc = bytearray.fromhex("54 65 61 6D 53 63 65 6E 61 72 69 6F").decode()
SOURCE = xa
DEVELOPER = axx
UPDATES = xxc

def help(update: Update, context: CallbackContext):
    message = update.effective_message
    textto = "To get alerts about your repository follow the steps below \n\n1.Add @ScenarioXbot in your group where you want bot to send alerts. \n\n2.Send /id command. \n\n3.Send /connect <Your group id> (must start with -100) \n\n4. Add this bot in that group where you want to receive alerts."
    pic = "https://telegra.ph/file/18155a81e0d3f0e71fd09.jpg"
    buttons1 = [
            [
              InlineKeyboardButton("Owner", url=f"https://t.me/{DEVELOPER}"),
              InlineKeyboardButton ("Updates", url=f"https://t.me/{UPDATES}"),
            ],
            [
             InlineKeyboardButton("Source", url=f"https://github.com/{SOURCE}")],
       ]
    markup_lol = InlineKeyboardMarkup(buttons1)
    update.message.reply_photo(photo=pic, caption=textto, reply_markup=markup_lol)


def lol(update: Update, context: CallbackContext):
    message = update.effective_message
    Pop = "https://telegra.ph/file/18155a81e0d3f0e71fd09.jpg"
    text = "Hello there I'm GitAlerts bot made by @TeamScenario \nCheck support group for help regarding bot or deployment. \n\nFor help send /help \nFor source send /repo"
    
    buttons = [
             [
               InlineKeyboardButton("Support", url="https://t.me/TeamXScenario"),
               InlineKeyboardButton("Updates", url=f"https://t.me/{UPDATES}"),
             ],
             [InlineKeyboardButton("Source", url=f"https://github.com/{SOURCE}")],  
          ]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_photo(photo=Pop, caption=text, reply_markup=reply_markup)


def source(update: Update, context: CallbackContext):
    message = update.effective_message
    textto = "Source of this bot!"
    pic = "https://telegra.ph/file/18155a81e0d3f0e71fd09.jpg"
    buttons1 = [
            [
              InlineKeyboardButton("Owner", url=f"https://t.me/{DEVELOPER}"),
              InlineKeyboardButton ("Updates", url=f"https://t.me/{UPDATES}"),
            ],
            [
             InlineKeyboardButton("Source", url=f"https://github.com/{SOURCE}")],
       ]
    markup_lol = InlineKeyboardMarkup(buttons1)
    update.message.reply_photo(photo=pic, caption=textto, reply_markup=markup_lol)

def connect(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text[len("/connect ") :]

    if text =='':
        message.reply_text("Kindly give your group id \nTo know how to get group id send /help")
    x = re.search("^-100", text)

    if x or text !="":
        reply_text = f"Payload url: `https://{HEROKU_APPNAME}.herokuapp.com//{text}` \n\nSend /morehelp for more help."
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
    else:
        reply_texto = "Wrong chat id! it must start with -1001 or -100"
        message.reply_text(reply_texto)

def more_help(update: Update, context: CallbackContext):
    tt = "1.Go to repo settings \n2.Find webhooks there \n3.Add Payload url there \n\n4. Change content type to application/json \n\n5.Which events would you like to trigger this webhook? \nâ€¢ Choose 1st or 2nd option \n\n6. Add webhook \n7. Done!"
    image = "https://telegra.ph/file/0239f2414d3430c29338f.jpg"
    btn = [
          [
           InlineKeyboardButton("Updates", url=f"https://t.me/{UPDATES}"),
           InlineKeyboardButton("Owner", url=f"https://t.me/{DEVELOPER}"),
          ],
      ]
    haha = InlineKeyboardMarkup(btn)
    update.message.reply_photo(photo=image, caption=tt, reply_markup=haha)


dispatcher.add_handler(CommandHandler("start", lol, run_async=True))
dispatcher.add_handler(CommandHandler("help", help, run_async=True))
dispatcher.add_handler(CommandHandler("repo", source, run_async=True))
dispatcher.add_handler(CommandHandler("connect", connect, run_async=True))
dispatcher.add_handler(CommandHandler("morehelp", more_help, run_async=True))
updater.start_polling()

TG_BOT_API = f'https://api.telegram.org/bot{BOT_TOKEN}/'
checkbot = get(TG_BOT_API + "getMe").json()
if not checkbot['ok']:
    log.error("[ERROR] Invalid Token!")
    exit(1)
else:
    username = checkbot['result']['username']
    log.info(
        f"[INFO] Logged in as @{username}, waiting for webhook requests...")


def post_tg(chat, message, parse_mode):
    """Send message to desired group"""
    response = post(
        TG_BOT_API + "sendMessage",
        params={
            "chat_id": chat,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True}).json()
    return response


def reply_tg(chat, message_id, message, parse_mode):
    """reply to message_id"""
    response = post(
        TG_BOT_API + "sendMessage",
        params={
            "chat_id": chat,
            "reply_to_message_id": message_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True}).json()
    return response


@server.route("/", methods=['GET'])
# Just send 'Hello, world!' to tell that our server is up.
def helloWorld():
    return 'Hello, world!'


@server.route("/<groupid>", methods=['GET', 'POST'])
def git_api(groupid):
    """Requests to api.github.com"""
    data = request.json
    if not data:
        return f"<b>Add this url:</b> {ip_addr}/{groupid} to webhooks of the project"

    if data.get('hook'):
        repo_url = data['repository']['html_url']
        repo_name = data['repository']['name']
        sender_url = data['sender']['html_url']
        sender_name = data['sender']['login']
        response = post_tg(
            groupid,
            f"🌟 Successfully set webhook for <a href='{repo_url}'>{repo_name}</a> by <a href='{sender_url}'>{sender_name}</a>!",
            "html"
        )
        return response

    if data.get('commits'):
        commits_text = ""
        rng = len(data['commits'])
        if rng > 10:
            rng = 10
        for x in range(rng):
            commit = data['commits'][x]
            if len(escape(commit['message'])) > 300:
                commit_msg = escape(commit['message']).split("\n")[0]
            else:
                commit_msg = escape(commit['message'])
            commits_text += f"{commit_msg}\n<a href='{commit['url']}'>{commit['id'][:7]}</a> - {commit['author']['name']} {escape('<')}{commit['author']['email']}{escape('>')}\n\n"
            if len(commits_text) > 1000:
                text = f"""✨ <b>{escape(data['repository']['name'])}</b> - New {len(data['commits'])} commits ({escape(data['ref'].split('/')[-1])})
{commits_text}
"""
                response = post_tg(groupid, text, "html")
                commits_text = ""
        if not commits_text:
            return jsonify({"ok": True, "text": "Commits text is none"})
        text = f"""✨¨ <b>{escape(data['repository']['name'])}</b> - New {len(data['commits'])} commits ({escape(data['ref'].split('/')[-1])})
{commits_text}
"""
        if len(data['commits']) > 10:
            text += f"\n\n<i>And {len(data['commits']) - 10} other commits</i>"
        response = post_tg(groupid, text, "html")
        return response

    if data.get('issue'):
        if data.get('comment'):
            text = f"""🚨’¬ New comment: <b>{escape(data['repository']['name'])}</b>
{escape(data['comment']['body'])}

<a href='{data['comment']['html_url']}'>Issue #{data['issue']['number']}</a>
"""
            response = post_tg(groupid, text, "html")
            return response
        text = f"""🚨¨ New {data['action']} issue for <b>{escape(data['repository']['name'])}</b>
<b>{escape(data['issue']['title'])}</b>
{escape(data['issue']['body'])}

<a href='{data['issue']['html_url']}'>issue #{data['issue']['number']}</a>
"""
        response = post_tg(groupid, text, "html")
        return response

    if data.get('pull_request'):
        if data.get('comment'):
            text = f"""💬— There is a new pull request for <b>{escape(data['repository']['name'])}</b> ({data['pull_request']['state']})
{escape(data['comment']['body'])}

<a href='{data['comment']['html_url']}'>Pull request #{data['issue']['number']}</a>
"""
            response = post_tg(groupid, text, "html")
            return response
        text = f"""❗—  New {data['action']} pull request for <b>{escape(data['repository']['name'])}</b>
<b>{escape(data['pull_request']['title'])}</b> ({data['pull_request']['state']})
{escape(data['pull_request']['body'])}

<a href='{data['pull_request']['html_url']}'>Pull request #{data['pull_request']['number']}</a>
"""
        response = post_tg(groupid, text, "html")
        return response

    if data.get('forkee'):
        response = post_tg(
            groupid,
            f"🍀´ <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> forked <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!\nTotal forks now are {data['repository']['forks_count']}",
            "html")
        return response

    if data.get('action'):

        if data.get('action') == "published" and data.get('release'):
            text = f"<a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> {data['action']} <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!"
            text += f"\n\n<b>{data['release']['name']}</b> ({data['release']['tag_name']})\n{data['release']['body']}\n\n<a href='{data['release']['tarball_url']}'>Download tar</a> | <a href='{data['release']['zipball_url']}'>Download zip</a>"
            response = post_tg(groupid, text, "html")
            return response

        if data.get('action') == "started":
            text = f"💘 <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> gave a star to <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!\nTotal stars are now {data['repository']['stargazers_count']}"
            response = post_tg(groupid, text, "html")
            return response

        if data.get('action') == "edited" and data.get('release'):
            text = f"<a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> {data['action']} <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!"
            text += f"\n\n<b>{data['release']['name']}</b> ({data['release']['tag_name']})\n{data['release']['body']}\n\n<a href='{data['release']['tarball_url']}'>Download tar</a> | <a href='{data['release']['zipball_url']}'>Download zip</a>"
            response = post_tg(groupid, text, "html")
            return response

        if data.get('action') == "created":
            return jsonify({"ok": True, "text": "Pass trigger for created"})

        response = post_tg(
            groupid,
            f"<a href='{data['sender']['html_url']}'>{data['sender']['login']}</a> {data['action']} <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>!",
            "html")
        return response

    if data.get('ref_type'):
        response = post_tg(
            groupid,
            f"A new {data['ref_type']} on <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> was created by <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!",
            "html")
        return response

    if data.get('created'):
        response = post_tg(groupid,
                           f"Branch {data['ref'].split('/')[-1]} <b>{data['ref'].split('/')[-2]}</b> on <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> was created by <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!",
                           "html")
        return response

    if data.get('deleted'):
        response = post_tg(groupid,
                           f"Branch {data['ref'].split('/')[-1]} <b>{data['ref'].split('/')[-2]}</b> on <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> was deleted by <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!",
                           "html")
        return response
    xx = bytearray.fromhex("43 6F 64 65 72 58").decode()
    fck = bytearray.fromhex("54 65 61 6D 53 63 65 6E 61 72 69 6F 2F 47 69 74 41 6C 65 72 74 73").decode()
    dkb = bytearray.fromhex("54 65 61 6D 53 63 65 6E 61 72 69 6F").decode()
    if DEVELOPER != xx:
       print("So sad, you have change developer, change it back to CoderX else I won't work")
       sys.exit(1)

    if SOURCE != fck:
       print("So sad, you have changed source, change it back to TeamScenario/GitAlerts else I won't work")
       sys.exit(1)

    if UPDATES != dkb:
       print("So sad, you have changed Updates, change it back to TeamScenario else I won't work")
       sys.exit(1)

    if data.get('forced'):
        response = post_tg(groupid,
                           f"Branch {data['ref'].split('/')[-1]} <b>{data['ref'].split('/')[-2]}</b>" +
                           " on <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> was" +
                           " forced by <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!",
                           "html")
        return response

    if data.get('pages'):
        text = f"<a href='{data['repository']['html_url']}'>{data['repository']['name']}</a> wiki pages were updated by <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!\n\n"
        for x in data['pages']:
            summary = ""
            if x['summary']:
                summary = f"{x['summary']}\n"
            text += f"📑<b>{escape(x['title'])}</b> ({x['action']})\n{summary}<a href='{x['html_url']}'>{x['page_name']}</a> - {x['sha'][:7]}"
            if len(data['pages']) >= 2:
                text += "\n=====================\n"
            response = post_tg(groupid, text, "html")
        return response

    if data.get('context'):
        if data.get('state') == "pending":
            emo = "⏳"
        elif data.get('state') == "success":
            emo = "✅"
        elif data.get('state') == "failure":
            emo = "❌"
        else:
            emo = "🔰"
        response = post_tg(
            groupid,
            f"{emo} <a href='{data['target_url']}'>{data['description']}</a>" +
            " on <a href='{data['repository']['html_url']}'>{data['repository']['name']}</a>" +
            " by <a href='{data['sender']['html_url']}'>{data['sender']['login']}</a>!" +
            "\nLatest commit:\n<a href='{data['commit']['commit']['url']}'>{escape(data['commit']['commit']['message'])}</a>",
            "html")
        return response

    url = deldog(data)
    response = post_tg(
        groupid,
        "🚫« Webhook endpoint for this chat has received something that doesn't understood yet. " +
        f"\n\nLink to logs for debugging: {url}",
        "markdown")
    return response


def deldog(data):
    """Pasing the stings to del.dog"""
    BASE_URL = 'https://del.dog'
    r = post(f'{BASE_URL}/documents', data=str(data).encode('utf-8'))
    if r.status_code == 404:
        r.raise_for_status()
    res = r.json()
    if r.status_code != 200:
        r.raise_for_status()
    key = res['key']
    if res['isUrl']:
        reply = f'DelDog URL: {BASE_URL}/{key}\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
    else:
        reply = f'{BASE_URL}/{key}'
    return reply


if __name__ == "__main__":
    port = int(environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)
