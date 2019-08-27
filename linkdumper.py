#!/usr/bin/python
#### AUTHOR - Arbaz Hussain
from burp import IBurpExtender
from burp import IMessageEditorTab,IMessageEditorTabFactory
from java.io import PrintWriter
import sys,re,urllib

regex_str = r'((href|src|icon|data|url)=[\'"]?([^\'" >;]+)|((?:(?:https?|ftp):\\/\\/)?[\w/\-?=%.]+\\?.[\w/\-?=%.]+))'
WHITELIST_MEMES = ['HTML','Script','Other text','CSS','JSON','script','json',"XML",'xml',"text","TEXT","app"]

class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
	def registerExtenderCallbacks(self, callbacks):
		self._callbacks = callbacks
		self._helpers = callbacks.getHelpers()
		sys.stdout = callbacks.getStdout()
		self._stdout = PrintWriter(callbacks.getStdout(), True)

		callbacks.setExtensionName("LinkDumper")
		callbacks.registerMessageEditorTabFactory(self)
		return 

	def createNewInstance(self,controller,editable):
		return LinkFetcherTab(self,controller,editable)


class LinkFetcherTab(IMessageEditorTab):
	def __init__(self,extender,controller,editable):
		self._extender = extender
		self._helpers = extender._helpers
		self._editable = editable

		self._txtInput = extender._callbacks.createTextEditor()
		self._txtInput.setEditable(editable)

	def getTabCaption(self):
		return "LINK-DUMPER"

	def getUiComponent(self):
		return self._txtInput.getComponent()

	def isEnabled(self,content,isRequest):
		r = self._helpers.analyzeResponse(content)
		if str(r.getInferredMimeType()) in WHITELIST_MEMES:
			msg = content[r.getBodyOffset():].tostring()
			msg = msg.replace('\\x3d','=').replace('\\x26','&').replace('\\x22','"').replace('\\x23','#').replace('\\x27',"'")
			regex = re.compile(regex_str,re.VERBOSE|re.IGNORECASE)
			re_r = regex.findall(msg)
			if len(re_r) != 0:
				self._links = list(set([tuple(j for j in re_r if j)[-1] for re_r in re_r]))
				self.final_links = '\n'.join(self.FilteringLinks(self._links))
				return len(re_r)

	def setMessage(self,content,isRequest):
		if content is None:
			self._txtInput.setText(None)
			self._txtInput.setEditable(False)
		else:
			self._txtInput.setText(self.final_links)
			self._currentMessage = self.final_links

	def getMessage(self):
		return self._currentMessage

	def isModified(self):
		return self._txtInput.isTextModified()

	def getSelectedData(self):
		return self._txtInput.getSelectedText()

	def Sorting(self,lst): 
	    lst2 = sorted(lst, key=len,reverse=True) 
	    return lst2 


	def FilteringLinks(self,urllist):
		final_unsorted_list = []
		final_sorted_list = []
		final_list = []
		if urllist:
			for each_url in urllist:
				if '\u002' in each_url: ###! UNICODE
					each_url = each_url.encode('utf-8').decode('unicode-escape','ignore').replace('\\x3d','=').replace('\\x26','&').replace('\\x22','"').replace('\\x23','#').replace('\\x27',"'")
					if '%3A' or '%2F' in each_url: ###! URL
						each_url = urllib.unquote(each_url).decode('utf-8','ignore').replace('\\x3d','=').replace('\\x26','&').replace('\\x22','"').replace('\\x23','#').replace('\\x27',"'")
						final_list.append(each_url)
					else:
						final_list.append(each_url.replace('\\x3d','=').replace('\\x26','&').replace('\\x22','"').replace('\\x23','#').replace('\\x27',"'"))
				if '%3A' or '%2F' in each_url:
					each_url = urllib.unquote(each_url).decode('utf-8','ignore').replace('\\x3d','=').replace('\\x26','&').replace('\\x22','"').replace('\\x23','#').replace('\\x27',"'")
					final_list.append(each_url)
				else:
					final_list.append(each_url.replace('\\x3d','=').replace('\\x26','&').replace('\\x22','"').replace('\\x23','#').replace('\\x27',"'"))

			for each_list in final_list:
				if each_list.startswith('/') or '://' in each_list or len(each_list.split('/')) > 1:
					final_sorted_list.append(each_list)


			for each_list in final_list:
				if each_list not in final_sorted_list:
					final_unsorted_list.append(each_list)

			temp_list = self.Sorting(final_unsorted_list)
			return final_sorted_list + temp_list
