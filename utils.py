# -*- coding: utf-8

from 	markdown import markdown

def checkClean(s):
	if(s==None):
		return False
	s2 = markdown(s.decode("utf-8"), safe_mode="escape")
	if s2.startswith("<p>"):
		s2 = s2[3:]
	if s2.endswith("</p>"):
		s2 = s2[:-4]
	return s2==s

# TODO: add some bleach
def clean(s):
	if(s==None):
		return ""
	s2 = markdown(s.decode("utf-8"), safe_mode="escape")
	if s2.startswith("<p>"):
		s2 = s2[3:]
	if s2.endswith("</p>"):
		s2 = s2[:-4]
	return s2
