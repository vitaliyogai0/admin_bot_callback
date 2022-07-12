
from flask import Flask, jsonify, request

import json
import vk

VK_TOKEN = '30ff64751510d1ec631ae1b8a07e2dd3c927d8ff467e8ba3bd93751099302b9123cd4b5a54376a2cc0ef2'
SECRET_KEY = 'limbos402'

API_VERSION = 5.101

bot = vk.API(access_token = VK_TOKEN, v = API_VERSION)

def add_friend(user_id):
	bot.friends.add(user_id = user_id)

def del_friend(user_id):
	bot.friends.delete(user_id = user_id)

def pin_msg(chat_id, conversation_msg_ids):
	bot.messages.pin(
		peer_id = get_peer_id(chat_id),
		conversation_message_id = conversation_msg_ids[0]
	)

def invite_user(chat_id, user_id):
	assert bot.friends.areFriends(user_ids = user_id)[0]['friend_status'] == 3
	bot.messages.addChatUser(chat_id = chat_id, user_id = user_id)

def delete_msg(chat_id, conversation_msg_ids):
	bot.messages.delete(
		message_ids = get_by_conversation_msg_ids(chat_id, conversation_msg_ids),
		delete_for_all = 1
	)

def get_by_conversation_msg_ids(chat_id, conversation_msg_ids):
	return [
		i['id'] for i in
		bot.messages.getByConversationMessageId(
			peer_id = get_peer_id(chat_id),
			conversation_message_ids = conversation_msg_ids
		)['items']
	]

def get_peer_id(chat_id):
	return 2000000000 + chat_id

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def index():
	data = json.loads(request.data)

	task = data.get('task')
	bot_id = data.get('bot_id')
	extra = data.get('object')

	try:
		assert data.get('secret_key') == SECRET_KEY

		if task == 'confirm_bot':
			pass

		elif task == 'invite_user':
			invite_user(extra['chat_id'], extra['user_id'])

		elif task == 'delete_msg':
			delete_msg(extra['chat_id'], extra['conversation_msg_ids'])

		elif task == 'add_friend':
			add_friend(extra['user_id'])

		elif task == 'del_friend':
			del_friend(extra['user_id'])

		elif task == 'pin_msg':
			pin_msg(extra['chat_id'], extra['conversation_msg_ids'])

	except Exception as e:
		print(e)
		return jsonify(response = 0)

	print(1)
	return jsonify(response = 1)
