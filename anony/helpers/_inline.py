# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic


from pyrogram import types

from anony import app, config, lang
from anony.core.lang import lang_codes

# ==========================================================
#         PREMIUM CUSTOM EMOJI IDs (টেলিগ্রাম প্রিমিয়াম ইমোজি আইডি)
# ==========================================================
# এখানে আপনি আপনার নিজস্ব কাস্টম ইমোজি আইডিগুলো বসিয়ে দিতে পারেন। 
# আইডিগুলো এখানে সরাসরি সংখ্যা (int) হিসেবে দেওয়া হয়েছে, যাতে কোনো এরর না আসে।
EMOJI_REWIND    = 5467554900741544602  # ⏪ Rewind
EMOJI_PAUSE     = 5467554900741544599  # ⏸ Pause
EMOJI_PLAY      = 5467554900741544610  # ▶ Play
EMOJI_SEEK      = 5467554900741544605  # ⏩ Seek
EMOJI_SHUFFLE   = 5467554900741544601  # 🔀 Shuffle
EMOJI_SKIP      = 5467554900741544604  # ⏭ Skip
EMOJI_REPLAY    = 5467554900741544603  # 🔄 Replay
EMOJI_VOLUME    = 5467554900741544600  # 🔊 Volume
EMOJI_REPEAT    = 5467554900741544606  # 🔁 Repeat
EMOJI_EFFECTS   = 5890925363067886150  # ✨ Effects
EMOJI_CLOSE     = 6257795658401456292  # ❌ Close

# স্টার্ট ও হেল্প কিবোর্ড বাটনের জন্য প্রিমিয়াম ইমোজি আইডি
EMOJI_ADD_GROUP = 5226945370684140473  # ➕ Add to Group
EMOJI_CHANNEL   = 5927290155378414084  # 📢 Channel
EMOJI_GROUP     = 6237668007133321493  # 💬 Group
EMOJI_OWNER     = 6122921006563597496  # 👨‍💻 Bot Owner
EMOJI_BACK      = 5467554900741544614  # ◀️ Back


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup

    # style এবং icon_custom_emoji_id সাপোর্ট করার জন্য কাস্টম মেথড
    def ikb(
        self, 
        text: str, 
        callback_data: str = None, 
        url: str = None, 
        style: str = None, 
        icon_custom_emoji_id: str = None,
        **kwargs
    ) -> types.InlineKeyboardButton:
        params = {"text": text}
        if callback_data:
            params["callback_data"] = callback_data
        if url:
            params["url"] = url
        if style:
            params["style"] = style
            
        if icon_custom_emoji_id:
            # আইডি স্ট্রিং আকারে আসলেও কোড যেন ক্র্যাশ না করে, তাই সেফটি হিসেবে এটিকে integer-এ কনভার্ট করে নেওয়া হচ্ছে।
            try:
                params["icon_custom_emoji_id"] = int(icon_custom_emoji_id)
            except (ValueError, TypeError):
                params["icon_custom_emoji_id"] = icon_custom_emoji_id
            
        params.update(kwargs)
        
        # যদি আপনার বটের পাইথনের লাইব্রেরি নতুন Bot API ফিচার সাপোর্ট না করে, 
        # তবে এটি ক্র্যাশ না করে স্বয়ংক্রিয়ভাবে সাধারণ বাটনে ব্যাকআপ নিয়ে রান করবে।
        try:
            return types.InlineKeyboardButton(**params)
        except TypeError:
            fallback = {"text": text}
            if callback_data:
                fallback["callback_data"] = callback_data
            if url:
                fallback["url"] = url
            if "copy_text" in kwargs:
                fallback["copy_text"] = kwargs["copy_text"]
            return types.InlineKeyboardButton(**fallback)

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, callback_data="cancel_dl")]])

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        playing: bool = True,  # প্লেয়ার স্টেট ট্র্যাক করার জন্য
        remove: bool = False,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        
        # ১. প্রগ্রেস বার বা স্ট্যাটাস বার (টাইমার)
        if status:
            keyboard.append(
                [self.ikb(text=status, callback_data=f"controls status {chat_id}", style="primary")]
            )
        elif timer:
            keyboard.append(
                [self.ikb(text=timer, callback_data=f"controls status {chat_id}", style="primary")]
            )

        if not remove:
            # প্লে/পজ অবস্থার ওপর ভিত্তি করে আইকন ও আইডি ডাইনামিক নির্ধারণ
            pause_text = "Pause" if playing else "Play"
            pause_action = "pause" if playing else "resume"
            pause_emoji_id = EMOJI_PAUSE if playing else EMOJI_PLAY

            # Row 1: Rewind, Pause/Play, Seek
            keyboard.append(
                [
                    self.ikb(text="Rewind", callback_data=f"controls rewind {chat_id}", style="primary", icon_custom_emoji_id=EMOJI_REWIND),
                    self.ikb(text=pause_text, callback_data=f"controls {pause_action} {chat_id}", style="success", icon_custom_emoji_id=pause_emoji_id),
                    self.ikb(text="Seek", callback_data=f"controls seek {chat_id}", style="primary", icon_custom_emoji_id=EMOJI_SEEK),
                ]
            )
            # Row 2: Shuffle, Skip, Replay
            keyboard.append(
                [
                    self.ikb(text="Shuffle", callback_data=f"controls shuffle {chat_id}", style="primary", icon_custom_emoji_id=EMOJI_SHUFFLE),
                    self.ikb(text="Skip", callback_data=f"controls skip {chat_id}", style="primary", icon_custom_emoji_id=EMOJI_SKIP),
                    self.ikb(text="Replay", callback_data=f"controls replay {chat_id}", style="primary", icon_custom_emoji_id=EMOJI_REPLAY),
                ]
            )
            # Row 3: Volume, Repeat, Effects
            keyboard.append(
                [
                    self.ikb(text="Volume", callback_data=f"controls volume {chat_id}", style="primary", icon_custom_emoji_id=EMOJI_VOLUME),
                    self.ikb(text="Repeat", callback_data=f"controls repeat {chat_id}", style="primary", icon_custom_emoji_id=EMOJI_REPEAT),
                    self.ikb(text="Effects", callback_data=f"controls effects {chat_id}", style="primary", icon_custom_emoji_id=EMOJI_EFFECTS),
                ]
            )
            # Row 4: Close
            keyboard.append(
                [
                    self.ikb(text="Close", callback_data=f"controls close {chat_id}", style="danger", icon_custom_emoji_id=EMOJI_CLOSE)
                ]
            )
            
        return self.ikm(keyboard)

    def help_markup(
        self, _lang: dict, back: bool = False
    ) -> types.InlineKeyboardMarkup:
        # স্ক্রিনশট ১-এর মতো শুধুমাত্র একটি সুন্দর ব্যাক বাটন দেখানোর জন্য
        if back:
            rows = [
                [
                    self.ikb(text=_lang["back"], callback_data="help back", style="primary", icon_custom_emoji_id=EMOJI_BACK)
                ]
            ]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo"]
            buttons = [
                self.ikb(text=_lang[f"help_{i}"], callback_data=f"help {cb}")
                for i, cb in enumerate(cbs)
            ]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]

        return self.ikm(rows)

    def lang_markup(self, _lang: str) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()

        buttons = [
            self.ikb(
                text=f"{name} ({code}) {'✔️' if code == _lang else ''}",
                callback_data=f"lang_change {code}",
            )
            for code, name in langs.items()
        ]
        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, url=config.SUPPORT_CHAT)]])

    def play_queued(
        self, chat_id: int, item_id: str, _text: str
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=_text, callback_data=f"controls force {chat_id} {item_id}"
                    )
                ]
            ]
        )

    def queue_markup(
        self, chat_id: int, _text: str, playing: bool
    ) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"
        return self.ikm(
            [[self.ikb(text=_text, callback_data=f"controls {_action} {chat_id} q")]]
        )

    def settings_markup(
        self, lang: dict, admin_only: bool, cmd_delete: bool, language: str, chat_id: int
    ) -> types.InlineKeyboardMarkup:
        admin_text = "✔️" if admin_only else "❌"
        delete_text = "✔️" if cmd_delete else "❌"

        return self.ikm(
            [
                [
                    self.ikb(
                        text=lang["play_mode"] + " ➜",
                        callback_data="settings",
                    ),
                    self.ikb(text=admin_text, callback_data="settings play"),
                ],
                [
                    self.ikb(
                        text=lang["cmd_delete"] + " ➜",
                        callback_data="settings",
                    ),
                    self.ikb(text=delete_text, callback_data="settings delete"),
                ],
                [
                    self.ikb(
                        text=lang["language"] + " ➜",
                        callback_data="settings",
                    ),
                    self.ikb(text=lang_codes[language], callback_data="language"),
                ],
            ]
        )

    def start_key(
        self, lang: dict = None, private: bool = False
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="Add to Group",
                        url=f"https://t.me/{app.username}?startgroup=true",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_ADD_GROUP
                    )
                ],
                [
                    self.ikb(
                        text="Channel",
                        url="https://t.me/SmartCoderDev",
                        style="danger",
                        icon_custom_emoji_id=EMOJI_CHANNEL
                    ),
                    self.ikb(
                        text="Group",
                        url="https://t.me/CoderChatZone",
                        style="success",
                        icon_custom_emoji_id=EMOJI_GROUP
                    ),
                ],
                [
                    self.ikb(
                        text="Bot Owner",
                        url="https://t.me/TheSmartRajib",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_OWNER
                    )
                ],
            ]
        )

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text="❐", copy_text=link),
                    self.ikb(text="Youtube", url=link),
                ],
            ]
        )