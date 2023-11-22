from pydantic import BaseModel


class Intents(BaseModel):
    guilds: bool
    guild_members: bool
    guild_messages: bool
    guild_message_reactions: bool
    direct_message: bool
    open_forums_event: bool
    audio_or_live_channel_member: bool
    unknown: bool
    interaction: bool
    message_audit: bool
    forums_event: bool
    audio_action: bool
    public_guild_messages: bool

    @classmethod
    def default(cls):
        return cls(
            guilds=True,
            guild_members=True,
            guild_messages=False,
            guild_message_reactions=True,
            direct_message=True,
            open_forums_event=True,
            audio_or_live_channel_member=True,
            unknown=False,
            interaction=True,
            message_audit=True,
            forums_event=False,
            audio_action=True,
            public_guild_messages=True
        )

    @classmethod
    def all(cls):
        return cls(
            guilds=True,
            guild_members=True,
            guild_messages=True,
            guild_message_reactions=True,
            direct_message=True,
            open_forums_event=True,
            audio_or_live_channel_member=True,
            unknown=True,
            interaction=True,
            message_audit=True,
            forums_event=True,
            audio_action=True,
            public_guild_messages=True
        )

    @classmethod
    def none(cls):
        return cls(
            guilds=False,
            guild_members=False,
            guild_messages=False,
            guild_message_reactions=False,
            direct_message=False,
            open_forums_event=False,
            audio_or_live_channel_member=False,
            unknown=False,
            interaction=False,
            message_audit=False,
            forums_event=False,
            audio_action=False,
            public_guild_messages=False
        )

    def to_int(self):
        return 0 | self.guilds << 0 + \
            0 | self.guild_members << 1 + \
            0 | self.guild_messages << 9 + \
            0 | self.guild_message_reactions << 10 + \
            0 | self.direct_message << 12 + \
            0 | self.open_forums_event << 18 + \
            0 | self.audio_or_live_channel_member << 19 + \
            0 | self.unknown << 25 + \
            0 | self.interaction << 26 + \
            0 | self.message_audit << 27 + \
            0 | self.forums_event << 28 + \
            0 | self.audio_action << 29 + \
            0 | self.public_guild_messages << 30
