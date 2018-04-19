#-*-coding:utf-8-*-
#@Author:Jan Wang
#@Date:2018-4-6
#Last Modified by:Jan
#Last Modified time:2018-4/8

import pygame#
import random#
from os import path
pygame.init()
#A.常量设定
WIDTH,HEIGHT=600,800#銀幕設定
NEW_ENEMMY_GENERATE_INTERVAL=500#新敌人产生设定（毫秒）
MISSILE_LIFETIME=10000
MISSILE_INTERVAL=500

RED=(255,0,0)
GRENN=(0,255,0)
BLUE=(0,0,255)
WHITH=(255,255,255)
BLACK=(0,0,0)

#A..主角類設定..#
class Player(pygame.sprite.Sprite):#
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.flip(player_img,False,True)#图片类的导入
		self.image=pygame.transform.scale(self.image,(53,40))#改变图片size
		self.image.set_colorkey(BLACK)    #改变图片透明
		self.rect=self.image.get_rect()#
		self.radius=20
		#pygame.draw.circle(self.image,(255,0,0),self(rect.center,self.radius))
		self.rect.centerx=WIDTH/2#位置置中
		self.rect.bottom=HEIGHT#位置置中

		self.hp= 100#生命值
		self.lives= 3#生命数
		self.score= 0#分数初始
		self.hidden= False#开始不Hidden
		self.hide_time= 0#初始隐藏时间为0
		self.is_missile_firing=False
		self.start_missile_time=0
		self.last_missile_time=0

	def update(self):
		key_state=pygame.key.get_pressed()#键盘设定
		if key_state[pygame.K_LEFT]:#
			self.rect.x-= 8#
		if key_state[pygame.K_RIGHT]:#
			self.rect.x+= 8#

		if self.rect.right>WIDTH:#
			self.rect.right=WIDTH#
		if self.rect.left< 0:#
			self.rect.left= 0#
		now=pygame.time.get_ticks()#隐藏判断条件
		if self.hidden and now - self.hide_time> 1000:
			self.hidden= False
			self.rect.bottom=HEIGHT
			self.rect.centerx=WIDTH/2

		if self.is_missile_firing:#飞弹程序
			if now-self.start_missile_time<=MISSILE_LIFETIME:
				if now-self.last_missile_time>MISSILE_INTERVAL:
					missile=Missile(self.rect.center)
					missiles.add(missile)
					self.last_missile_time=now
		else:
			self.is_missile_firing=False

	def shoot(self):
		bullet=Bullet(self.rect.centerx,self.rect.centery)
		bullets.add(bullet)#
		shoot_sound.play()

	def hide(self):
		self.hidden= True
		self.rect.y=- 200#往上移到Y-200位置
		self.hide_time=pygame.time.get_ticks()

	def fire_missile(self):
		self.is_missile_firing=True
		self.start_missile_time=pygame.time.get_ticks()

#B..敵人類設定..#
class Enemy(pygame.sprite.Sprite):#
	def __init__(self):#
		pygame.sprite.Sprite.__init__(self)#
		img_width=random.randint(20, 100)
		img_height=int(img_width*70/ 72)
		self.image=pygame.transform.scale(enemy_img,(img_width,img_height))#图片类的导入
		#self.image=pygame.transform.scale(self.image,(random.randint(40,70),random.randint(35,90)))
		self.image.set_colorkey(BLACK)
		self.image_origin=self.image.copy()
		self.rect=self.image.get_rect()#
		#碰撞检查函数
		self.radius=int(img_width/2)
		#pygame.draw.circle(self.image,(255,0,0),self(rect.center,self.radius))
		
		self.rect.x=random.randint(0,WIDTH-self.rect.w)#???
		self.rect.bottom=0#流星进入点设定

		self.vx=random.randint(-2,2)#
		self.vy=random.randint(2,3)#
		#陨石转动
		self.last_time=0
		self.rotate_speed=random.randint(-5,5)#随机旋转速度
		self.rotate_angle=0
 ###..出左右边界的敌人消除###
		#if self.rect.left>WIDTH: #
		#	self.kell()
		#if self.rect.right<0:
		#	self.kill()
	def update(self):#
		self.rect.x+=self.vx#
		self.rect.y+=self.vy#
		self.rotate()

	def rotate(self):
		now=pygame.time.get_ticks()
		if now-self.last_time>30:
			self.rotate_angle=(self.rotate_angle+self.rotate_speed)%360
			self.image=pygame.transform.rotate(self.image_origin,self.rotate_angle)
			old_center=self.rect.center#更新中心点
			self.rect=self.image.get_rect()
			self.rect.center=old_center

#C..武器類設定..#
class Bullet(pygame.sprite.Sprite):#
	def __init__(self,x,y):#
		pygame.sprite.Sprite.__init__(self)#
		self.image=bullet_img
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()#
		self.radius=20##??

		self.rect.centerx=x#
		self.rect.centery=y#
	
	def update(self):#
		self.rect.y-=10#

class Missile(pygame.sprite.Sprite):#导弹小精灵
	def __init__(self,center):#
		pygame.sprite.Sprite.__init__(self)#
		self.image=missile_img
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()#
		self.rect.center=center#
		self.radius=20
	
	def update(self):#
		self.rect.y-=5#		
		
class Explosion(pygame.sprite.Sprite):#爆炸效果及精灵小组
	def __init__(self,center):#
		pygame.sprite.Sprite.__init__(self)#
		self.image=pygame.transform.scale(explosion_animation[0],(10,20))
		self.rect=self.image.get_rect()#
		self.rect.center=center#爆炸位置调整更新
		self.image.set_colorkey(BLACK)#爆炸背景清除
		self.frame=0
		self.last_time=pygame.time.get_ticks()# AA.控制播放速度
		explosion_sound.play()

	def update(self):#爆炸效果时间控制
		now=pygame.time.get_ticks()# AA.
		if now-self.last_time>40:#40
			if self.frame<len(explosion_animation):
				self.image=explosion_animation[self.frame]
				self.frame+=1
				self.last_time=now
			else:
				self.kill()

class PowerUp(pygame.sprite.Sprite):#
	def __init__(self,center):#
		pygame.sprite.Sprite.__init__(self)#
		#产生概率（0~50% 生命值/50%~80%飞弹/>80%生命数
		random_num=random.random()
		if random_num>=0 and random_num<0.5:
			self.type='add_hp'
		elif random_num>=0.5 and random_num<0.8:
			self.type='add_missile'
		else:
			self.type='add_life'
		self.image=powerup_imgs[self.type]
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()#
		self.rect.center=center#

	def update(self):
		self.rect.y+= 5
		
def draw_text(text,surface,color,x, y,size):
	font_name=pygame.font.match_font('arial')
	font=pygame.font.Font(font_name,size)
	text_surface=font.render(text, True,color)
	text_rect=text_surface.get_rect()
	text_rect.midtop=(x,y)
	surface.blit(text_surface,text_rect)

def draw_ui():
	pygame.draw.rect(screen,GRENN,(10,10,player.hp,15))
	pygame.draw.rect(screen,WHITH,(10,10,100,15),2)

	draw_text(str(player.score),screen,WHITH,WIDTH/2,10,20)

	img_rect=player_img_small.get_rect()
	img_rect.right=WIDTH-10
	img_rect.y=10
	for i in range(player.lives):
		screen.blit(player_img_small,img_rect)
		img_rect.right=img_rect.x-10

def show_menu():
	global screen,game_state
	
	screen.blit(background_img,background_rect)

	draw_text('Space Shooter!',screen,WHITH,WIDTH/2,500,40)
	draw_text('Press Space Key to start',screen,GRENN,WIDTH/2,200,40)
	draw_text('Press Esc key to quit',screen,RED,WIDTH/2,350,40)
	
	event_list=pygame.event.get()
	for event in event_list:#
		if event.type==pygame.QUIT:#
			pygame.quit()
			quit()#
		if event.type==pygame.KEYDOWN:#
			if event.key==pygame.K_ESCAPE:#
				pygame.quit()
				quit()#
			if event.key==pygame.K_SPACE:#判斷按下空格#
				game_state=1

	pygame.display.flip()
		
#D..畫面設定#
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init()
pygame.init()#初始化操作/重要图片导入在此之后
#pygame.mixer.init()..会延迟

screen=pygame.display.set_mode((WIDTH,HEIGHT))#$
pygame.display.set_caption("Jan's My Game")#
clock=pygame.time.Clock()#
#图像导入
img_dir=path.join(path.dirname(__file__),'img')#导入路径

background_dir=path.join(img_dir,'background.png')#导入背景图片
background_img=pygame.image.load(background_dir).convert()#获取background图片尺寸信息
background_rect=background_img.get_rect()

player_dir=path.join(img_dir,'spaceShips_009.png')#导入玩家图片
player_img=pygame.image.load(player_dir).convert()
player_img_small=pygame.transform.scale(player_img,(26,20))
player_img_small.set_colorkey(BLACK)

enemy_dir=path.join(img_dir,'spaceMeteors_002.png')#导入敌方图片
enemy_img=pygame.image.load(enemy_dir).convert()

bullet_dir=path.join(img_dir,'spaceMissiles_027.png')#导入武器图片
bullet_img=pygame.image.load(bullet_dir).convert()
missile_dir=path.join(img_dir,'spaceMissiles_007.png')#导入武器图片
missile_img=pygame.image.load(missile_dir).convert()

explosion_animation=[]
for i in range(9):
	explosion_dir=path.join(img_dir,'regularExplosion0{}.png'.format(i))
	img=pygame.image.load(explosion_dir).convert()
	img.set_colorkey(BLACK)
	img=pygame.transform.scale(img,(76,75))
	explosion_animation.append(img)
#补给增加
powerup_imgs={}
powerup_add_hp_dir=path.join(img_dir,'red.png')
powerup_imgs['add_hp']=pygame.image.load(powerup_add_hp_dir).convert()
powerup_add_life_dir=path.join(img_dir,'star.png')
powerup_imgs['add_life']=pygame.image.load(powerup_add_life_dir).convert()
powerup_add_missile_dir=path.join(img_dir,'green.png')
powerup_imgs['add_missile']=pygame.image.load(powerup_add_missile_dir).convert()

sound_dir=path.join(path.dirname(__file__),'sound')#导入路径
shoot_sound=pygame.mixer.Sound(path.join(sound_dir,'shoot.wav'))
explosion_sound=pygame.mixer.Sound(path.join(sound_dir,'explosion.wav'))
pygame.mixer.music.load(path.join(sound_dir,"war.mp3"))
#画面群组设定##
player=Player()#

enemys=pygame.sprite.Group()#
for i in range(10):#敵人數量設定#
	enemy=Enemy()#
	enemys.add(enemy)#敵人精靈群組

bullets=pygame.sprite.Group()#武器群組設定#
explosions=pygame.sprite.Group()#爆炸精灵群组设定#
powerups=pygame.sprite.Group()#补给精灵
missiles=pygame.sprite.Group()#飞弹精灵族群
last_enemy_generate_time=0#记录上次敌人产生时间

#E..遊戲控制#
game_over=False
game_state=0#
pygame.mixer.music.set_volume(2)#Min为1
pygame.mixer.music.play(loops=-1)#背景音乐（-1表示不断循环）

while not game_over:
	clock.tick(60)

##...MENU....................................
	if game_state==0:
		show_menu()
	elif game_state==1:
		now=pygame.time.get_ticks()#控制爆炸时间长短
		if now-last_enemy_generate_time>NEW_ENEMMY_GENERATE_INTERVAL:
			enemy=Enemy()
			enemys.add(enemy)
			last_enemy_generate_time=now#敌人产生控制

		event_list=pygame.event.get()
		for event in event_list:#
			if event.type==pygame.QUIT:#
				game_over=True#
			if event.type==pygame.KEYDOWN:#
				if event.key==pygame.K_ESCAPE:#
					game_over=True
				if event.key==pygame.K_SPACE:#判斷按下空格#
					player.shoot()#按下空格發射#
				
		screen.fill(BLACK)#
		screen.blit(background_img,background_rect)#屏幕画出背景图像
	#F..角色狀態更新..#
		enemys.update()#敵人
		player.update()#玩家
		bullets.update()#武器刷新
		explosions.update()#爆炸
		powerups.update()#补品
		missiles.update()#导弹

	#G..交鋒設定..#
		hits=pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_rect_ratio(0.8))#碰撞检查函数
		#hits=pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle)#碰撞检查函数
		for hit in hits:
			player.hp-=hit.radius#按比例扣血
			if player.hp<0:
				player.lives-=1#生命数控制
				player.hp=100
				player.hide()#调用函数
				if player.lives==0:
					game_over=True
				
		hits=pygame.sprite.groupcollide(bullets,enemys,True,True)#碰撞後消除
		for hit in hits:
			enemy=Enemy()
			enemys.add(enemy)
			explosion=Explosion(hit.rect.center)#💥产生时间
			explosions.add(explosion)
			player.score+=hit.radius#print(player.score)#看得分情况
			if random.random()>0.9:#补给品概率:
				powerup=PowerUp(hit.rect.center)#补给品产生点
				powerups.add(powerup)

		hits=pygame.sprite.groupcollide(missiles,enemys,True,True)#碰撞後消除
		for hit in hits:
			enemy=Enemy()
			enemys.add(enemy)
			explosion=Explosion(hit.rect.center)#💥产生时间
			explosions.add(explosion)
			player.score+=hit.radius#print(player.score)#看得分情况
			if random.random()>0.9:#补给品概率:
				powerup=PowerUp(hit.rect.center)#补给品产生点
				powerups.add(powerup)

	#补给品的碰撞检测
		hits=pygame.sprite.spritecollide(player,powerups,True)#碰撞检查函数
		for hit in hits:
			if hit.type=='add_hp':
				player.hp+=25
				if player.hp>100:
					player.hp=100#生命值上限值
			elif hit.type=='add_life':
				player.lives+=1
				if player.lives>3:
					player.lives=3#生命值上限值
			else:
				player.fire_missile()

	#..畫面更新..#图像绘制
		screen.blit(player.image,(player.rect.x,player.rect.y))#画面刷新
		enemys.draw(screen)##画面刷新
		bullets.draw(screen)##画面刷新
		missiles.draw(screen)
		explosions.draw(screen)##画面刷新
		powerups.draw(screen)

		draw_ui()#UI绘制

		pygame.display.flip()#
	##pygame quit()