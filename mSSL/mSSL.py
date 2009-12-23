#!/usr/bin/env python
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import os,sys
import xml.etree.ElementTree as ConfigTree
from xml.etree.ElementTree import Element
import pytils.translit

gladefile = "mSSL.glade"

if sys.platform == "linux2" :
	properties_file = os.environ['HOME']+"/.mSSL"
	openSSL_bin_filter = "openssl"
	openSSL_bin_default = "/usr/bin/openssl"
	workdir_default = os.environ['HOME'] + "/"
	path_separator="/"
	tmpdir="/tmp/"
elif sys.platform == "win32" :
	properties_file = os.environ['APPDATA']+"\\.mSSL"
	openSSL_bin_filter = "openssl.exe"
	openSSL_bin_default = "C:\\openSSL\\bin\\openssl.exe"
	workdir_default = unicode ( os.environ['USERPROFILE'].decode('cp1251') + "\\Рабочий стол\\" )
	path_separator="\\"	
	tmpdir=os.environ['TMP']
else:
	print 'Unknown OS...'
	sys.exit()

if not os.path.exists(properties_file):
	print ( "Creating config" )
	config = ConfigTree.Element("config")
	# Описания пользователя
	user_creditionals = ConfigTree.SubElement (config, "user_creditionals")
	user_creditionals.set ("step","0")
        countryName = ConfigTree.SubElement (user_creditionals, "countryName")
	countryName.text = "Russia"
	countryName.set ("id","0")
        stateOrProvinceName = ConfigTree.SubElement (user_creditionals, "stateOrProvinceName")
	stateOrProvinceName.text = "city"
	stateOrProvinceName.set ("id","0")
        localityName = ConfigTree.SubElement (user_creditionals, "localityName")
        localityName.text = "."
	organizationName = ConfigTree.SubElement (user_creditionals, "organizationName")
        organizationName.text = "."
	organizationalUnitName = ConfigTree.SubElement (user_creditionals, "organizationalUnitName")
	organizationalUnitName.text = "."
        commonName = ConfigTree.SubElement (user_creditionals, "commonName")
	commonName.text = "."
        emailAddress = ConfigTree.SubElement (user_creditionals, "emailAddress")
	emailAddress.text =".@."
        UID = ConfigTree.SubElement (user_creditionals, "UID")
	UID.text = "."
	# Настройки программы
        preferences = ConfigTree.SubElement (config, "preferences")
        workdir = ConfigTree.SubElement (preferences, "workdir")
	workdir.text = workdir_default
	openssl_bin = ConfigTree.SubElement (preferences, "openssl_bin")
	openssl_bin.text = openSSL_bin_default
        
	ctree = ConfigTree.ElementTree ( config )
        ctree.write ( properties_file )
else :
	ctree = ConfigTree.ElementTree ()
	ctree.parse ( properties_file )
	config=ctree.getroot()

max_step=5
start_step=int(config.find("user_creditionals").get("step"))
class mSSLgui:
	def __init__(self):
		windowname = "mSSLwindow"
		self.wTree = gtk.glade.XML (gladefile,windowname)
		window = self.wTree.get_widget( windowname )
		dic = { 
			"on_imagemenuitem_about_activate" : self.about_show,
			"on_imagemenuitem_quit_activate" : self.close_app,
			"on_usercreditionals_imagemenuitem_activate" : self.user_creditionals_editor,
			"on_preferences_imagemenuitem_activate" : self.preferences_show,
			"on_main_button_clicked" : self.main_button_clicked,
			"on_reset_menuitem_activate" : self.reset_clicked,
		      }
		self.wTree.signal_autoconnect(dic)
		main_progress=self.wTree.get_widget( "main_progress" )
		
		if start_step == 0 :
				main_progress.set_fraction(0)
				main_progress.set_text("1/" + str(max_step) + unicode(" Получение корневоого сертификата"))
		elif start_step == 1 :
				main_progress.set_fraction(1.0/max_step)
				main_progress.set_text("2/" + str(max_step) + unicode(" Генерация секретного ключа"))
		elif start_step == 2 :
				main_progress.set_fraction(2.0/max_step)
				main_progress.set_text("3/" + str(max_step) + unicode(" Генерация запроса сертификата"))
		elif start_step == 3 :
				main_progress.set_fraction(3.0/max_step)
				main_progress.set_text("4/" + str(max_step) + unicode(" Получение сертификата"))
		elif start_step == 4 :
				main_progress.set_fraction(4.0/max_step)
				main_progress.set_text("5/" + str(max_step) + unicode(" Создание пакета PKCS12"))
		elif start_step == 5 :
				main_progress.set_fraction(1)
				main_progress.set_text(unicode("Пакет с сертификатом создан !"))
		window.connect("destroy", self.close_app)
		window.show()
	

	def user_creditionals_editor(self,widget):
		def save (widget) :
			countryName = config.find("user_creditionals/countryName")
			localityName = config.find("user_creditionals/localityName")
			stateOrProvinceName = config.find("user_creditionals/stateOrProvinceName")
			organizationName = config.find("user_creditionals/organizationName")
			organizationalUnitName = config.find("user_creditionals/organizationalUnitName")
			commonName = config.find("user_creditionals/commonName")
			emailAddress = config.find("user_creditionals/emailAddress")
			UID = config.find("user_creditionals/UID")

			countryName.text = country_combobox.get_active_text ()
			countryName.set ( "id", str ( country_combobox.get_active () ) )
			localityName.text = pytils.translit.translify ( unicode (localityName_entry.get_text () ) )
			stateOrProvinceName.text = stateOrProvinceName_combobox.get_active_text ()
			stateOrProvinceName.set ( "id", str ( stateOrProvinceName_combobox.get_active () ) )
			organizationName.text = pytils.translit.translify ( unicode (organizationName_entry.get_text () ))
			organizationalUnitName.text = pytils.translit.translify ( unicode (organizationalUnitName_entry.get_text () ))
			commonName.text = pytils.translit.translify ( unicode (commonName_entry.get_text () ))
			emailAddress.text = pytils.translit.translify ( unicode (emailAddress_entry.get_text () ))
			UID.text = pytils.translit.translify ( unicode (UID_entry.get_text () ))

			ctree.write ( properties_file )
			user_creditionals_window.destroy()			

		def cancel(widget):
			user_creditionals_window.destroy()			

		self.user_creditionals_wTree = gtk.glade.XML (gladefile,"user_creditionals_window")
		user_creditionals_window = self.user_creditionals_wTree.get_widget( "user_creditionals_window" )
		dic = { 
			"on_user_creditionals_save_button_clicked" : save,
			"on_user_creditionals_cancel_button_clicked": cancel,
		      }
		self.user_creditionals_wTree.signal_autoconnect(dic)

		country_combobox = self.user_creditionals_wTree.get_widget( "country_combobox" )
		localityName_entry = self.user_creditionals_wTree.get_widget( "localityName_entry" )
		stateOrProvinceName_combobox = self.user_creditionals_wTree.get_widget( "stateOrProvinceName_combobox")
		organizationName_entry = self.user_creditionals_wTree.get_widget( "organizationName_entry" )
		organizationalUnitName_entry = self.user_creditionals_wTree.get_widget( "organizationalUnitName_entry" )
		commonName_entry = self.user_creditionals_wTree.get_widget( "commonName_entry" )
		emailAddress_entry = self.user_creditionals_wTree.get_widget( "emailAddress_entry" )
		UID_entry = self.user_creditionals_wTree.get_widget( "UID_entry" )
		
		country_combobox.set_active ( int( config.find("user_creditionals/countryName").get("id") ) )
		localityName_entry.set_text ( config.find("user_creditionals/localityName").text )
		stateOrProvinceName_combobox.set_active ( int( config.find("user_creditionals/stateOrProvinceName").get("id") ) )
		organizationName_entry.set_text ( config.find("user_creditionals/organizationName").text )
		organizationalUnitName_entry.set_text ( config.find("user_creditionals/organizationalUnitName").text )
		commonName_entry.set_text ( config.find("user_creditionals/commonName").text )
		emailAddress_entry.set_text ( config.find("user_creditionals/emailAddress").text )
		UID_entry.set_text ( config.find("user_creditionals/UID").text )

		user_creditionals_window.run()

	def preferences_show(self,widget):
		def save (widget) :
			workdir = config.find("preferences/workdir")
			openssl_bin = config.find("preferences/openssl_bin")
			workdir.text = unicode ( workdir_filechooserbutton.get_filename() + path_separator )
			openssl_bin.text = openssl_filechooserbutton.get_filename ()
			ctree.write ( properties_file )
			preferences_window.destroy()
		def cancel (widget) :
			preferences_window.destroy()
		preferences_windowname = "preferences_dialog"
		self.preferences_wTree = gtk.glade.XML (gladefile,preferences_windowname)
		preferences_window = self.preferences_wTree.get_widget( preferences_windowname )
		dic = { 
			"on_save_button_clicked" : save,
			"on_cancel_button_clicked": cancel,
		      }
		self.preferences_wTree.signal_autoconnect(dic)
		workdir_filechooserbutton = self.preferences_wTree.get_widget( "workdir_filechooserbutton" )
		openssl_filechooserbutton = self.preferences_wTree.get_widget( "openssl_filechooserbutton" )
		
		workdir_filechooserbutton.set_filename ( config.find("preferences/workdir").text )
		openssl_filechooserbutton.set_filename ( config.find("preferences/openssl_bin").text )
		filter = gtk.FileFilter()
		filter.add_pattern (openSSL_bin_filter)
		filter.set_name (openSSL_bin_filter)
		openssl_filechooserbutton.add_filter ( filter )
		preferences_window.run()

	def about_show(self,widget):
		about_windowname = "mSSLabout"
		self.about_wTree = gtk.glade.XML (gladefile,about_windowname)
		about_window = self.about_wTree.get_widget( about_windowname )
		about_window.run()
		about_window.destroy()
	
	def main_button_clicked(self,widget):
		openssl_bin_program = config.find("preferences/openssl_bin").text
		workdir_path = config.find("preferences/workdir").text
		step=int(config.find("user_creditionals").get("step"))
		main_progress=self.wTree.get_widget( "main_progress" )
		if step == 0 :
				if not os.path.exists( workdir_path +"cacert.pem" ) :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, 
							unicode("Файл корневого сертификата \n" + workdir_path + "cacert.pem не найден!\n" +
								"Этот файл Вы можете получить в центре выдачи цифровых сертификатов Организации"))
					dialog.run()
					dialog.destroy()
				else :
					if not step == max_step : step += 1
					config.find("user_creditionals").set ("step",str(step))
					ctree.write ( properties_file )
					main_progress.set_fraction(1.0/max_step)
					main_progress.set_text("2/" + str(max_step) + unicode(" Генерация секретного ключа"))	
		elif step == 1 :
				cur_command = openssl_bin_program + ' genrsa -out "' + workdir_path + 'privkey.pem" 2048'
				if sys.platform == "win32" :
					os.system(cur_command.encode("cp1251"))
				else :
					os.system(cur_command)
				if os.path.exists( workdir_path +"privkey.pem" ) :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,gtk.BUTTONS_OK, 
								unicode("Файл приватного ключа  \n" + workdir_path + "private.pem успешно создан!\n"))
					dialog.run()
					dialog.destroy()				
					if not step == max_step : step += 1
					config.find("user_creditionals").set ("step",str(step))
					ctree.write ( properties_file )
					main_progress.set_fraction(2.0/max_step)
					main_progress.set_text("3/" + str(max_step) + unicode(" Генерация запроса сертификата"))
				else :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, 
							unicode("Файл приватного ключа \n" + workdir_path + "private.pem не создан!" +
								"Произошла непредвиденная ошибка: обратитесь в службу технической поддержки."))
					dialog.run()
					dialog.destroy()
					
		elif step == 2 :
				#Создаем файл конфигурации для OpenSSL				
				tmpconfig = tmpdir + path_separator + "mssl.tmp"		
				tmpconfig_file = open (tmpconfig,'w')
				tmpconfig_file.write ( "[ req ]\ndistinguished_name      = req_distinguished_name\n[ req_distinguished_name ]" )
				for item in [ 'countryName','stateOrProvinceName','localityName','organizationName','organizationalUnitName','commonName','emailAddress','UID'] :
					tmpconfig_file.write ( item + " = \n" + item + "_default = " + config.find("user_creditionals/"+ item ).text + "\n" )
				tmpconfig_file.close()
				
				cur_command = openssl_bin_program + ' req -batch -new -key "' + workdir_path + 'privkey.pem" -out "' + workdir_path + 'user-cert.csr" -config ' + tmpconfig
				if sys.platform == "win32" :
					os.system(cur_command.encode("cp1251"))
				else :
					os.system(cur_command)

				if os.path.exists( workdir_path +"user-cert.csr" ) :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,gtk.BUTTONS_OK, 
								unicode("Файл запроса сертификата  \n" + workdir_path + "user-cert.csr успешно создан!\n"))
					dialog.run()
					dialog.destroy()				
					if not step == max_step : step += 1
					config.find("user_creditionals").set ("step",str(step))
					ctree.write ( properties_file )
					main_progress.set_fraction(3.0/max_step)
					main_progress.set_text("4/" + str(max_step) + unicode(" Получение сертификата"))
				else :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, 
							unicode("Файл запроса сертификата \n" + workdir_path + "user-cert.csr не создан!" +
								"Произошла непредвиденная ошибка: обратитесь в службу технической поддержки."))
					dialog.run()
					dialog.destroy()
		elif step == 3 :
				if os.path.exists( workdir_path +"user-cert.pem" ) :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,gtk.BUTTONS_OK, 
								unicode("Файл сертификата  \n" + workdir_path + "user-cert.pem получен!\n"))
					dialog.run()
					dialog.destroy()				
					if not step == max_step : step += 1
					config.find("user_creditionals").set ("step",str(step))
					ctree.write ( properties_file )
					main_progress.set_fraction(4.0/max_step)
					main_progress.set_text("5/" + str(max_step) + unicode(" Создание пакета PKCS12"))
				else :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, 
							unicode("Файл сертификата \n" + workdir_path.decode("utf-8") + "user-cert.pem не получен!" ))
					dialog.run()
					dialog.destroy()

		elif step == 4 or step == 5 :
				def ok (widget):
					self.password_value = password_entry.get_text ()
					password_dialog.destroy()
					cur_command = ( openssl_bin_program + ' pkcs12 -export -in "' + workdir_path + 'user-cert.pem" -inkey "' + workdir_path + 'privkey.pem" -certfile "' + 
					workdir_path + 'cacert.pem" -out "' + workdir_path + 'user.p12" -password pass:'+ self.password_value )
					if sys.platform == "win32" :
						os.system(cur_command.encode("cp1251"))
					else :
						os.system(cur_command)

				self.password_wTree = gtk.glade.XML (gladefile,"password_dialog")
				password_dialog = self.password_wTree.get_widget( "password_dialog" )
				dic = { 
					"on_ok_button_clicked" : ok,
				      }
				self.password_wTree.signal_autoconnect(dic)
				password_entry = self.password_wTree.get_widget( "password_entry" )
				password_dialog.run ()

				if os.path.exists( workdir_path +"user.p12" ) :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,gtk.BUTTONS_OK, 
								unicode("Файл пакета \n" + workdir_path + "user.p12 успешно создан!\n"))
					dialog.run()
					dialog.destroy()				
					if not step == max_step :
						step += 1
						config.find("user_creditionals").set ("step",str(step))
						ctree.write ( properties_file )
						main_progress.set_fraction(1)
						main_progress.set_text(unicode("Пакет с сертификатом создан !"))
				else :
					dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, 
							unicode("Файл сертификата \n" + workdir_path + "user.p12 не создан! \n" + 
								"Произошла непредвиденная ошибка: обратитесь в службу технической поддержки." ))
					dialog.run()
					dialog.destroy()

	def reset_clicked(self, widget):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO, 
			unicode("Данное действие удалит все сгенерированые файлы в рабочей директории, в том числе и корневой сертификат организации.\nПродолжить?"))
		response=dialog.run()
		dialog.destroy()				
		if response == gtk.RESPONSE_YES :
			for f in ['privkey.pem','cacert.pem','user-cert.pem','user-cert.csr','user.p12'] :
				try:
					os.remove( config.find("preferences/workdir").text + path_separator + f )
				except:
					print unicode("Невозможно удалить файл " + f)
			config.find("user_creditionals").set ("step","0")
			ctree.write ( properties_file )
			gtk.main_quit()
	def close_app(self, widget):	
        	gtk.main_quit()

mSSL = mSSLgui()
gtk.main()



