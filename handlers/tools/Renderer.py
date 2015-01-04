# -*- coding: utf-8

from datetime import datetime

def DocumentHeader(doc):
	# TODO: make a clean unicde/str conversion
	score = len(doc['plusvote'])-len(doc['minusvote'])
	s = ""
	if(doc.get('expired', False)):
		s += "<div class='expireddoc'>\n<span class='expiredtag'>[expiré]</span>"
	if doc['type']=="discussion":
		s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
		s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
		s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
		s+="  <span class='documentsummarytype'>[Discussion]</span>\n"
		s+="  <span class='documentsummarytitle'><a href='/document/"+str(doc['_id'])+"'>" +doc['title']+"</a></span>\n"
		s+="   par \n"
		s+="  <span class='documentsummaryauthor'>"+doc['author']+"</span>\n"
		s+="  <span class='documentsummarydate'>en date du "+str(datetime(*doc['time'][:7]))+"</span>\n"
	elif doc['type']=="spending":
		s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
		s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
		s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
		s+="  <span class='documentsummarytype'>[Dépense]</span>\n"
		s+="  <span class='documentsummaryamount'>["+str(doc['amount'])+"&euro;]</span>\n"
		s+="  <span class='documentsummarytitle'><a href='/document/"
		s+=str(doc['_id'])+"'>" + doc['title'].encode("utf-8")+"</a></span>\n"
		s+="   par \n"
		s+="  <span class='documentsummaryauthor'>"+str(doc['author'])+"</span>\n"
		s+="  <span class='documentsummarydate'>en date du "+str(datetime(*doc['time'][:7]))+"</span>\n"
	elif doc['type']=="election":
		s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
		s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
		s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
		s+="  <span class='documentsummarytype'>[Election]</span>\n"
		s+=u"  <span class='documentsummarytitle'><a href='/document/"+str(doc['_id'])
		s+="'>Remplacer " +str(doc['togo'])+" par "+unicode(doc['toenter'])+"</a></span>\n"
		s+=u"   proposé par \n"
		s+="  <span class='documentsummaryauthor'>"+doc['author']+"</span>\n"
		s+="  <span class='documentsummarydate'>en date du "+str(datetime(*doc['time'][:7]))+"</span>\n"
	elif doc['type']=="status":
		s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
		s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
		s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
		s+="  <span class='documentsummarytype'>[Statuts]</span>\n"
		s+="  <span class='documentsummarytitle'><a href='/document/"+str(doc['_id'])+"'>"+doc['title']+"</a></span>\n"
		s+=u"   proposé par \n"
		s+="  <span class='documentsummaryauthor'>"+doc['author']+"</span>\n"
		s+="  <span class='documentsummarydate'>en date du "+str(datetime(*doc['time'][:7]))+"</span>\n"
	elif doc['type']=="vote":
		s+="  <span class='plusvotebutton'><a href='/plusvote/"+str(doc['_id'])+"'>+</a></span>"
		s+="  <span class='documentsummaryscore'>"+str(score)+"</span>\n"
		s+="  <span class='minusvotebutton'><a href='/minusvote/"+str(doc['_id'])+"'>-</a></span>"
		s+="  <span class='documentsummarytype'>[Vote]</span>\n"
		s+="  <span class='documentsummarytitle'><a href='/document/"+str(doc['_id'])+"'>"+doc['title']+"</a></span>\n"
		s+="   proposé par \n"
		s+="  <span class='documentsummaryauthor'>"+doc['author']+"</span>\n"
		s+="  <span class='documentsummarydate'>en date du "+str(datetime(*doc['time'][:7]))+"</span>\n"
	if(doc.get('expired', False)):
		s+="</div>\n"
	return s

def CurrentBudget(db, amount):
	s=u""
	s+=u"<div class='budget'>"
	s+=u"<h1>État du budget pour ce mois</h1>"
	s+=u" <table class='budgetdetails'>\n"
	s+=u"  <tr><td>Coût</td><td>Titre</td><td>Reste</td></tr>\n"
	s+=u"  <tr><td>-</td><td>-</td><td>"+ str(amount) +u" €</td></tr>\n"
	bitems = []
	for l in db.documents.find({"expired":False}):
		print l
		if l["type"]=="spending":
			score = len(l['plusvote'])-len(l['minusvote'])
			bitems.append([score, l])
	bitems.sort()
	bitems.reverse()
	print type(s)
	
	for i in bitems:
		valid = amount>=i[1]["amount"]
		if valid:
			amount -= i[1]["amount"]
		print type(s)
		s+= BudgetItem(i[1], valid, amount)
		print type(s)
		
	s+=u" </table>"
	s+=u" <div class='bottomline'>Reste reporté le mois suivant: " + str(amount) + u" € </div>"
	s+=u"</div>"
	return s


def BudgetItem(item, valid, remains):
	s=u""
	if(valid):
		s+="<tr class='validbudgetitem'>\n"
	else:
		s+="<tr class='invalidbudgetitem'>\n"
	s+=" <td class='amount'>" + unicode(item["amount"]) + u" €</td>\n"
	s+=" <td class='title'><a href='/document/"+str(item['_id'])+"'>" + item["title"] + "</a></td>\n"
	
	s+=" <td class='remain'>" + str(remains) + u" €</td>\n"
	s+="</tr>\n"
	return s
	
def HumanDate(d):
	s=""
	return s
