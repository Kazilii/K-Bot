from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from discord import Member
from discord import TextChannel
from discord import File
from random import choice as RNG
import os
import requests
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import base64
import mimetypes
from shutil import copyfile

PATH = "/home/dawn/bots/sweetiebot/media/"

class Profile(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=814)
		self.directory = os.path.dirname(os.path.realpath(__file__))
		default_user = {
			"Motto": None,
			"Score": 0,
			"Vanity_Url": None,
			"Level": 0,
			"XP": 0,
			"Required_XP": 40,
			"Total_Messages": 0,
			"Color": None,
			"Forum_Url": None,
			"New_Profile": True
		}
		self.config.register_user(**default_user)
		self.check_folders()

	def check_folders(self):
		if not os.path.exists(f"{self.directory}/resources"):
			print("Creating resources folder...")
			os.makedirs(f"{self.directory}/resources")

		if not os.path.exists(f"{self.directory}/resources/USERDATA"):
			print("Creating USERDATA folder.")
			os.makedirs(f"{self.directory}/resources/USERDATA")

		if not os.path.exists(f"{self.directory}/resources/DEFAULTS"):
			print("Creating Default resource folder")
			os.makedirs(f"{self.directory}/resources/DEFAULTS")

			urls = ["https://cdn.discordapp.com/attachments/501449462066053120/611988398835630134/profilebackground.png",
					"https://cdn.discordapp.com/attachments/501449462066053120/611988398038712335/profiletransparent.png",
					"https://cdn.discordapp.com/attachments/501449462066053120/611988400718872579/boxoutline.png"]

			for url in urls:
				r = requests.get(url, allow_redirects=True)
				filename = url.split('/')[-1]
				open(f"{self.directory}/resources/DEFAULTS/{filename}", 'wb').write(r.content)

	@commands.command()
	async def makeprofile(self, ctx):
		"""Create a profile with K-Bot"""

		if await self.config.user(ctx.author).get_raw('New_Profile'):
			await ctx.send("You don't have a profile! Let's make one!")
			if not os.path.exists(f"{self.directory}/resources/USERDATA/{ctx.author.id}"):
				os.makedirs(f"{self.directory}/resources/USERDATA/{ctx.author.id}")
			if await self.config.user(ctx.author).get_raw('New_Profile'):
				await self.config.user(ctx.author).set_raw('New_Profile', value=False)
				await ctx.send("Profile activated, you may view it with `!profile` or edit it with `!editprofile`")
				return
		else:
			await ctx.send("You've already made a profile! You can check it with `!profile` or edit it with `!editprofile`")
			return
		return

	@commands.command()
	@checks.mod()
	async def say(self, ctx, channel: TextChannel, *, text):
		"""Say something in the specified channel, great for pranks!"""
		await channel.send(text)