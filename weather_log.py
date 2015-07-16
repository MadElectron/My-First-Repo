#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

filepath = 'access.log'

# Данное регулярное выражение точно выделяет только HTTP-код ответа, рефферера и время ответа, необходимые в задаче
Pattern  = re.compile(r'''\[.*\]\spogoda.yandex.\w{1,3}\s
	\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s
	"GET\s\/.*\sHTTP\/\d\.\d"\s(\d{3})\s
	"([^"]*)"\s"[^"]*"\s"[^"]*"\s
	(\d.\d{1,3})\s-\s\d*''', re.VERBOSE)

def unparse_record( rec, refferers, ave_time ):
	""" Обработка отдельной запси лога: функция разбирает запись rec, добавляет 
валидного реферера (с кодом 200) в список рефереров reffferers и накапливает 
суммарное время ответа ave_time """
	
	m = re.search( Pattern, rec )
	if m :
		resp_code, ref, resp_time = m.groups()
		if resp_code == '200' and ref != '-':
			refferers.append( ref )	
		ave_time += float( resp_time ) 
		return ave_time

def top_refferers( filepath ) :
	""" Формирование топа рефереров и вычисление среднего времени ответа """
	refferers = []
	ave_time = 0
	with open( filepath, 'rt', encoding = 'ascii') as src :
		for k, rec in enumerate( src ): 
			ave_time = unparse_record( rec, refferers, ave_time )
		ref_set  = set( refferers )		
		ref_dict = dict( (k, refferers.count(k)) for k in ref_set ) 
		ref_dict = sorted( ref_dict, key = ref_dict.get, reverse = True) 
	return ref_dict[0:10], ave_time / (k+1)

ref_top, time = top_refferers( filepath )
print( '=== TOP 10 REFFERERS ===')
for r in ref_top : 
	print( r )
print( '\nAVERAGE RESPONSE TIME = ' + str( round( time, 3 )) )
