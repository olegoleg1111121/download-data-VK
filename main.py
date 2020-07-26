import vk_api
import configparser
import os
import sys
import time
import random

config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
LOGIN = config.get('VK', 'LOGIN')
PASSWORD = config.get('VK', 'PASSWORD')
VK_TOKEN = config.get('VK', 'TOKEN', fallback=None)

def main():
	LOG = autorize()
	if LOG != 1:
		print('Неправильные логин или пароль, '+str(LOG))
		return
	REGIM = int(input('1. - спарсить диалоги + вложения (HTML)\nВыберите режим: '))
	if REGIM == 1:
		times = time.time()
		dialogs()
		named_tuple = time.localtime(time.time()-times) # получить struct_time
		time_string = time.strftime("%M:%S", named_tuple)
		print(time_string,'секунд занял парсинг')













def dialogs():
	local = getdialogs()
	b = 0
	for i in local:
		b+=1
		history(i)
		print(b)








def getdialogs():
	local = []
	vk_session = vk_api.VkApi(token=VK_TOKEN)
	vk = vk_session.get_api()
	colvo = vk.messages.getConversations(count=1)
	local+= colvo['items']
	colvo = int(round(colvo['count']/100))
	#print(colvo)
	for i in range (0,colvo):
		cold = vk.messages.getConversations(count=100,offset=i*100)
		local+=cold['items']
		#print(local)
	return local

def autorize():
	try:
		vk_session = vk_api.VkApi(token=VK_TOKEN)
		vk = vk_session.get_api()
	except Exception as error:
		return(error)
	return 1













def history(message):
	vk_session = vk_api.VkApi(token=VK_TOKEN)
	vk = vk_session.get_api()
	ID = str(message['conversation']['peer']['id'])
	if ID[0:3] == '200':
		pass
	else:
		if not os.path.isdir("РЕЗУЛЬТАТЫ"):
			os.mkdir("РЕЗУЛЬТАТЫ")
		if ID[0] == '-':
			return
		#print(message['conversation']['peer']['id'])
		user = vk.users.get(user_ids=message['conversation']['peer']['id'])
		print(user[0]['first_name'],user[0]['last_name'])
		try:
			file = open(f"РЕЗУЛЬТАТЫ/{user[0]['first_name']} {user[0]['last_name']}.html", "w",encoding='utf-8')
		except:
			try:
				file = open(f"РЕЗУЛЬТАТЫ/{user[0]['first_name']} {random.randint(1,255)}.html", "w",encoding='utf-8')
			except:
				file = open(f"РЕЗУЛЬТАТЫ/{random.randint(1,255)} {user[0]['last_name']}.html", "w",encoding='utf-8')
		file.write(f'''<!DOCTYPE html>
<html>

 <head>

  <meta charset="utf-8"/>
<title>Exported Data</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>

  <link href="data/css/style.css" rel="stylesheet"/>

  <script src="data/js/script.js" type="text/javascript">

  </script>

 </head>

 <body onload="CheckLocation();">

  <div class="page_wrap">

   <div class="page_header">

    <div class="content">

     <div class="text bold">
{user[0]['first_name']} {user[0]['last_name']}
	 </div>

    </div>

   </div>

   <div class="page_body chat_page">

    <div class="history">''')

		message = vk.messages.getHistory(count=1,peer_id=ID,rev=1)
		times = message['items'][0]['date']
		date(file,message['items'][0])
		time_string = time.strftime("%m/%d/%Y", time.localtime(times))
		name = (user[0]['first_name']+' '+user[0]['last_name'])
		local = []
		newmess = 0
		colvo = int(round(message['count']/100))
		if colvo == 0:
			colvo = 1
		for i in range(0,colvo):
			message = vk.messages.getHistory(count=100,peer_id=ID,rev=1,offset=i*100)
			local+=message['items']
		for i in local:
			if i['date'] - times > 86400:
				times = i['date']
				date(file,i)
				newmess = 1
			else:
				newmess = 0
			time_string = time.strftime("%H:%M",time.localtime(i['date']))
			if ID == str(i['from_id']):
				try:
					index = local.index(i)
					if local[index-1]['from_id'] == i['from_id'] and newmess == 0:
						join(file,i)	
					else:
						he_message(name,file,i)
				except:
					he_message(name,file,i)
			else:
				try:
					index = local.index(i)
					if local[index-1]['from_id'] == i['from_id'] and newmess == 0:
						join(file,i)
					else:
						me_message(file,i)
				except:
					me_message(file,i)
		file.close()


def date(file,message):
	time_string = time.strftime("%H:%M", time.localtime(message['date']))
	file.write(f'''<div class="message service" id="message-1">

      <div class="body details">
{time_string}
      </div>

     </div>''')

def me_message(file,message):
	named_tuple = time.localtime(message['date'])
	time_string = time.strftime("%H:%M", named_tuple)
	file.write(f'''<div class="message default clearfix" id="message46828">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic5" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
Я
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="12.07.2020 12:48:16">
{time_string}
       </div>

       <div class="from_name">
Я
       </div>

       <div class="text">
{message['text']}
       </div>

      </div>

     </div>''')
	if message['attachments'] != None and message['attachments'] != []:
		media(file,message)

def join(file,message):
	named_tuple = time.localtime(message['date'])
	time_string = time.strftime("%H:%M", named_tuple)
	file.write(f'''<div class="message default clearfix joined" id="message46829">

      <div class="body">

       <div class="pull_right date details" title="12.07.2020 12:48:18">
{time_string}
       </div>

       <div class="text">
{message['text']}
       </div>

      </div>

     </div>''')
	if message['attachments'] != None and message['attachments'] != []:
		media(file,message)


def he_message(name,file,message):
	named_tuple = time.localtime(message['date'])
	time_string = time.strftime("%H:%M", named_tuple)
	try:
		names = (f'{name.split(" ")[0][0]}{name.split(" ")[1][0]}')
	except:
		names = name
	#print(name.split(" ")[0] +' '+ name.split(" ")[1])
	file.write(f'''<div class="message default clearfix" id="message46826">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic5" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
{names}
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="12.07.2020 12:47:39">
{time_string}
       </div>

       <div class="from_name">
{name}
       </div>

       <div class="text">
{message['text']}
       </div>

      </div>

     </div>''')
	if message['attachments'] != None and message['attachments'] != []:
		media(file,message)



def media(file,message):
	for mess in message['attachments']:
		if mess['type'] == 'photo':
			try:
				file.write(f'''<div class="media_wrap clearfix">

        <a class="photo_wrap clearfix pull_left" href="{mess['photo']['sizes'][6]['url']}">

         <img class="photo" src="{mess['photo']['sizes'][6]['url']}" style="width: {message['attachments'][0]['photo']['sizes'][6]['width']}px; height: {mess['photo']['sizes'][6]['height']}px">

        </a>

       </div>''')
			except:
				print(mess)
		elif mess['type'] == 'audio_message':
			try:
				file.write(f'''<div class="media_wrap clearfix">

        <a class="media clearfix pull_left block_link media_voice_message" href="{mess['audio_message']['link_ogg']}">

         <div class="fill pull_left">

         </div>

         <div class="body">

          <div class="title bold">
Голосовое сообщение
          </div>

          <div class="status details">
{mess['audio_message']['duration']}
          </div>

         </div>

        </a>

       </div>''')
			except:
				print(mess)






if __name__ == '__main__':
	main()