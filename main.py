

import json
import os
import platform
from typing import Union
import discord

from lib.jtakl import Jtalk



def run_bot():

    jtalk = Jtalk()     # Jtalkインスタンス
    current_status = {} # テキストチャンネルとボイスクライアントの紐付け
    # = {
    #   "str: {text_channel}": {
    #       "voice_client": object: voice_client,
    #       "caller": object: ctx.author
    # }

    intents = discord.Intents.all()
    intents.message_content = True
    bot = discord.Bot(intents=intents)

    @bot.event
    async def on_ready():
        """起動メッセージ"""
        print(f'{"-"*30}\non_ready: discord_bot_manager')
        print(f'python_version: {platform.python_version()}')
        print(f'pycord_version: {discord.__version__}')


    @bot.event
    async def on_message(ctx: discord.ApplicationContext):
        """テキスト投稿"""
        print(f'ctx.type.name: {ctx.type.name}')    # メッセージタイプ

        if ctx.type.name != 'default':
            return  # デフォルトメッセージタイプ以外は早期リターン

        if str(ctx.channel.id) not in current_status.keys():
            return  # 読み上げるテキストチャンネルではない場合は早期リターン
        else:
            # ボイスクライアント取得（ボットが退室していても、オブジェクトは残ります。）
            voice_client: discord.VoiceClient = current_status[str(ctx.channel.id)]['voice_client']

        # 音声ファイル生成・パス取得
        #jtalk = Jtalk()
        wav_path = jtalk.create_wav(ctx.clean_content)
        # 発話
        voice_client.play(discord.FFmpegPCMAudio(wav_path))
        # 音声ファイル削除
        jtalk.del_old_wav()


    @bot.event
    async def on_voice_state_update(member, before, after):
        """VC入退室イベント（BOTの入室しているVCの人数がゼロになったら自動で退出する機能）"""
        voice_client_temp = [vc for vc in bot.voice_clients if vc.guild.id == member.guild.id]# and vc.channel.id == channel_id]
        voice_client = voice_client_temp[0] if voice_client_temp else None
        
        if voice_client == None:
            return

        # ボットではないユーザー数取得
        vc_join_users: int = [mbr for mbr in voice_client.channel.members if mbr.bot == False]
        
        # ユーザーがいなければ退室
        if len(vc_join_users) == 0:
            await voice_client.disconnect()


    @bot.slash_command(description='読み上げボットがボイスチャンネルに参加します。')
    async def tts_join(ctx: discord.ApplicationContext):
        """読み上げボットVC_Join"""
        author_voice = ctx.author.voice     # caller が入室しているVC
        voice_channel = author_voice.channel if author_voice != None else None
        text_channel = ctx.channel
        if voice_channel == None:
            await ctx.respond(content=f'```ユーザーがボイスチャンネルに入室していません。\nボイスチャンネルに入室してから、再度コマンドを実行して下さい。```', ephemeral=True)
    
        if ctx.guild.id in [vc.server_id for vc in bot.voice_clients]:
            # ボットはギルド内のボイスチャンネルに入っている。
            if ctx.author.voice.channel.id in [vc.channel.id for vc in bot.voice_clients]:
                await ctx.respond(content=f'```既にボイスチャンネルに入室しています。```', ephemeral=True)
            else:
                await ctx.respond(content=f'```既に他のボイスチャンネルに入室しています。```', ephemeral=True)
        else:
            # ボットはギルド内のボイスチャンネルに入っていない。
            voice_client = await voice_channel.connect()
            await ctx.respond(content=f'```ボイスチャンネルに入室しました。\nボットがVCを退室するまで他ユーザーのコマンド操作を受け付けません。```', ephemeral=True)
            current_status[str(text_channel.id)] = {'voice_client': voice_client, 'caller': ctx.author}


    @bot.slash_command(description='読み上げボットがボイスチャンネルから退室します。（呼び出したユーザー以外のコマンドは受け付けません。）')
    async def tts_bye(ctx: discord.ApplicationContext):
        """読み上げボットVC_Bye"""
        for tc_id, value in current_status.items():
            is_match_text_channel = (ctx.channel.id == int(tc_id))
            is_match_caller = (ctx.author == value['caller'])
            is_active_voice_client = True if value['voice_client'] else False
            if is_match_text_channel and is_match_caller and is_active_voice_client:
                await value['voice_client'].disconnect()
                await ctx.respond(content=f'```ボイスチャンネルから退室しました。```', ephemeral=True)
            else:
                msg = '\n'.join([
                    '無効なコマンドです。考えられる原因は',
                    '・呼び出したユーザーではない。',
                    '・呼び出したテキストチャンネルではない。',
                    '・既にボットが退室している。'
                ])
                await ctx.respond(
                    content=f"```{msg}```",
                    ephemeral=True
                )


    bot.run(get_config_json('discord_bot')['token'])


def get_config_json(name: str) -> Union[list, dict]:
    """configフォルダ内の設定を取得して返します。"""
    path = f'{os.path.abspath(os.path.dirname(__file__))}/config/{name}.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    run_bot()

    