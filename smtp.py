#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetEnvironment.py
#  Test Network Environment, OpenFlow Table Management
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

CRLF = '\r\n'


from socket import *

# Print direction of messages
def printi( _t, *_as ): print( '<--   ' + _t % _as ) # in
def printo( _t, *_as ): print( '-->   ' + _t % _as ) # out
def printx( _t, *_as ): print( 'xxx   ' + _t % _as ) # err

# Email to send to the recipient
msg = '\r\nI love computer networks!'
endmsg = '\r\n.\r\n'



#MARK: - MAIL SERVER
class MailServer( __builtins__.object ):
	# Default values
	defaults = dict(
		host = 'localhost',
		port = 6789,
		ports = [25, 465, 587]
	)
	#
	def __init__( self, **kwargs ):
		# Initialize from a property list
		plist = self.defaults
		plist.update(kwargs)
		# Set values from list
		self.mailserver = plist['host']
		self.port = plist['port']
		self.all_ports = plist['ports']
		# Determine server location
		self.host = self.mailserver
		self.ip = gethostbyname( self.host )
	# Host name and Port number
	def addr( self ):
		return ( self.host, self.port )
	# IP address and Port nubmer
	def ipaddr( self ):
		return ( self.ip, self.port )


# Google Mail server host and port
serverHost = 'smtp.gmail.com'
serverPort = 587
# Create a reference to the server
mailserver = MailServer( host = serverHost, port = serverPort )
#MARK: Server -



#MARK: - MAIL CLIENT
# Create a client connected to a server
class Client( __builtins__.object ):
	#
	def __init__( self ):
		self.sock = socket( AF_INET, SOCK_STREAM )
		self.host = '0'
		self.port = 0
	# Start TCP Connection with a MailServer
	def connect( self, server ):
		print( '** Connecting to the MailServer... **' )
		print( '   Destination: %s:%s' % server.ipaddr() )
		print('')
		self.sock.connect( (server.host, server.port) )
		print( '** Established TCP connection **' )
		print( '   Source: %s:%s' % (client.addr()) )
		print( '   Socket: %s' % client.sock )
		print('')
	
	# Socket send
	def send( self, data ):
		self.lastSent = data
		return self.sock.send( data )
	# Socket receive
	def recv( self, bytes = 1024 ):
		return self.sock.recv( bytes )
	
	#MARK: Send and Receive SMTP commands
	# Send and display an SMTP command
	def send_smtp( self, _message ):
		self.send( (_message + CRLF).encode() )
		printo( _message )
	# Receive and display SMTP response
	def get_smtp( self, expected_code = 250 ):
		_response = self.recv(1024).decode()
		printi( _response )
		code = str(expected_code)
		if ( _response[:3] != code ):
			printx( '%s reply not received from server.' % code )
	
	# Host name and Port number
	def addr( self ):
		_addr = self.sock.getsockname()
		(self.host, self.port) = _addr
		return _addr
	# Last sent message
	def last( self ):
		return self.lastSent.decode()


# Create a client and establish a TCP connection with mailserver
client = Client()
client.connect( mailserver )
# Email to send to the recipient
msg = '\r\nI love computer networks!'
endmsg = '\r\n.\r\n'

# Short send/get functions
send = lambda msg : client.send_smtp( msg )
get = lambda code : client.get_smtp( code )
#MARK: Client -





#MARK: - SMTP Commands
class SMTP:
	HELO = 'HELO gmail.com'
	STARTTLS = 'STARTTLS'
	AUTH = 'AUTH LOGIN'
	MAILFROM = 'MAIL FROM:<maximpuchkov1@gmail.com>' # <maximpuchkov1@gmail.com>'
	RCPTTO = 'RCPT TO:<maxim_puchkov@sfu.ca>' # <mpuchkov@sfu.ca>'
	DATA = 'DATA'
	QUIT = 'QUIT'
	
	_FROMALICE = 'MAIL FROM: <alice@gmail.com>\r\n'
	_TOBOB = 'RCPT TO: <bob@yahoo.com>\r\n'





#MARK: - Send commands to the mail server

try:
	# Connection acknowledgement
	get( 220 )
	# Introduce client
	send( SMTP.HELO )        # send HELO
	get( 250 )               # expect status 250 (OK)
	
	# Enable security
	send( SMTP.STARTTLS )
	get( 220 )               # server is ready to start TLS
	# From / To addresses
	send( SMTP.MAILFROM )    # --- any command will close the connection
	get( 250 )
	send( SMTP.RCPTTO )
	get( 250 )
	
	# Message content
	## DATA header
	send( SMTP.DATA )
	get( 354 )
	## Message body
	send( msg )
	#client.get_smtp( 0 )
	send( endmsg )
	get( 250 )
	# Quit
	send ( SMTP.QUIT )
	get( 251 )

except:
	print( '\n\n\nAn error occurred before this command was sent:' )
	print( '\t %s' % client.last() )
	print( 'Exiting %s...' % __file__ )

