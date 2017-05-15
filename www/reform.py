
#
# Copyright (c) 2005-2006 Michael Eddington
# Copyright (c) 2004 IOActive Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# Authors:
#   Michael Eddington (meddington@gmail.com)

# $Id$

# Class version really just calls "static" methods below.
class Reform:
	def HtmlEncode(strInput, default=''):
		return HtmlEncode(strInput, default)
	HtmlEncode = staticmethod(HtmlEncode)
	
	def HtmlAttributeEncode(strInput, default=''):
		return HtmlAttributeEncode(strInput, default)
	HtmlAttributeEncode = staticmethod(HtmlAttributeEncode)
	
	def XmlEncode(strInput, default=''):
		return XmlEncode(strInput, default)
	XmlEncode = staticmethod(XmlEncode)
	
	def XmlAttributeEncode(strInput, default=''):
		return XmlAttributeEncode(strInput, default)
	XmlAttributeEncode = staticmethod(XmlAttributeEncode)
	
	def JsString(strInput, default=''):
		return JsString(strInput, default)
	JsString = staticmethod(JsString)
	
	def VbsString(strInput, default=''):
		return VbsString(strInput, default)
	VbsString = staticmethod(VbsString)

## ##########################################################

def HtmlEncode(strInput, default=''):
	
	if strInput == None or len(strInput) == 0:
		strInput = default
		
		if strInput == None or len(strInput) == 0:
			return ''
	
	# Allow: a-z A-Z 0-9 SPACE , .
	# Allow (dec): 97-122 65-90 48-57 32 44 46
	
	out = ''
	for char in strInput:
		c = ord(char)
		if ((c >= 97 and c <= 122) or
			(c >= 65 and c <= 90 ) or
			(c >= 48 and c <= 57 ) or
			c == 32 or c == 44 or c == 46):
			out += char
		else:
			out += "&#%d;" % c
	
	return out

def HtmlAttributeEncode(strInput, default=''):
	
	if strInput == None or len(strInput) == 0:
		strInput = default
		
		if strInput == None or len(strInput) == 0:
			return ''
	
	# Allow: a-z A-Z 0-9
	# Allow (dec): 97-122 65-90 48-57
	
	out = ''
	for char in strInput:
		c = ord(char)
		if ((c >= 97 and c <= 122) or
			(c >= 65 and c <= 90 ) or
			(c >= 48 and c <= 57 )):
			out += char
		else:
			out += "&#%d;" % c
	
	return out

def XmlEncode(strInput, default=''):
	return HtmlEncode(strInput, default)

def XmlAttributeEncode(strInput, default=''):
	return HtmlAttributeEncode(strInput, default)

def JsString(strInput, default=''):
	
	if strInput == None or len(strInput) == 0:
		strInput = default
		
		if strInput == None or len(strInput) == 0:
			return "''"
	
	# Allow: a-z A-Z 0-9 SPACE , .
	# Allow (dec): 97-122 65-90 48-57 32 44 46
	
	out = ''
	for char in strInput:
		c = ord(char)
		if ((c >= 97 and c <= 122) or
			(c >= 65 and c <= 90 ) or
			(c >= 48 and c <= 57 ) or
			c == 32 or c == 44 or c == 46):
			out += char
		elif c <= 127:
			out += "\\x%02X" % c
		else:
			out += "\\u%04X" % c
	
	return "'%s'" % out

def VbsString(strInput, default=''):
	
	if strInput == None or len(strInput) == 0:
		strInput = default
		
		if strInput == None or len(strInput) == 0:
			return '""'
	
	# Allow: a-z A-Z 0-9 SPACE , .
	# Allow (dec): 97-122 65-90 48-57 32 44 46
		
	out = ''
	inStr = 0	# Boolean (0 false, 1 true)
				# Using numerical for backwards
				# compatability
		
	for char in strInput:
		c = ord(char)
		if ((c >= 97 and c <= 122) or
			(c >= 65 and c <= 90 ) or
			(c >= 48 and c <= 57 ) or
			c == 32 or c == 44 or c == 46):
			
			if inStr == 0:
				inStr = 1
				out += '&"'
			
			out += char
		else:
			if inStr == 0:
				out += "&chrw(%d)" % c
			else:
				inStr = 0
				out += "\"&chrw(%d)" % c
		
	if inStr == 1:
		out += '"'
		
	return out.lstrip('&')

import unittest

class ReformUnittest(unittest.TestCase):
	
	def testHtmlEncode(self):
		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.",
			Reform.HtmlEncode("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,."), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.HtmlEncode("<>&\""), "Usual suspects")
		# Other characters
		self.failUnlessEqual("&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.HtmlEncode("`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation")
		# Unicode characters
		toEncode = ""
		encodedStr = ""
		for i in range(127,6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i
		
		self.failUnlessEqual(encodedStr,
			Reform.HtmlEncode(toEncode), "Unicode characters to 6000")
	
	def testHtmlEncodeDefault(self):
		# Usual stuff
		self.failUnlessEqual("default", 
			Reform.HtmlEncode(None, "default"), "Checking default")
		
		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.",
			Reform.HtmlEncode(None, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,."), "Non encoding chars via default")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.HtmlEncode(None, "<>&\""), "Usual suspects via default")
		# Other characters
		self.failUnlessEqual("&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.HtmlEncode(None, "`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation via default")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i
		
		self.failUnlessEqual(encodedStr,
			Reform.HtmlEncode(None, toEncode), "Unicode characters to 6000 via default")
		
		# The following are sanity checks
		
		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.",
			Reform.HtmlEncode("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.", "default"), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.HtmlEncode("<>&\"", "default"), "Usual suspects")
		# Other characters
		self.failUnlessEqual("&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.HtmlEncode("`~!@#$%^&*()_+=-{}|\\][:;'/?><", "default"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i
		
		self.failUnlessEqual(encodedStr,
			Reform.HtmlEncode(toEncode, "default"), "Unicode characters to 6000")

	def testHtmlAttributeEncode(self):
		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321",
			Reform.HtmlAttributeEncode("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321"), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.HtmlAttributeEncode("<>&\""), "Usual suspects")
		# Other characters
		self.failUnlessEqual("&#32;&#44;&#46;&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.HtmlAttributeEncode(" ,.`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i
		
		self.failUnlessEqual(encodedStr,
			Reform.HtmlAttributeEncode(toEncode), "Unicode characters to 6000")

	def testHtmlAttributeEncodeDefault(self):
		# Usual stuff
		self.failUnlessEqual("default",
			Reform.HtmlAttributeEncode(None, "default"), "Checking default")
		
		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321",
			Reform.HtmlAttributeEncode(None, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321"), "Non encoding chars via default")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.HtmlAttributeEncode(None, "<>&\""), "Usual suspects via default")
		# Other characters
		self.failUnlessEqual("&#32;&#44;&#46;&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.HtmlAttributeEncode(None, " ,.`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation via default")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i
		
		self.failUnlessEqual(encodedStr,
			Reform.HtmlAttributeEncode(None, toEncode), "Unicode characters to 6000 via default")
		
		# The following are sanity checks
		
		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321",
			Reform.HtmlAttributeEncode("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321", "default"), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.HtmlAttributeEncode("<>&\"", "default"), "Usual suspects")
		# Other characters
		self.failUnlessEqual("&#32;&#44;&#46;&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.HtmlAttributeEncode(" ,.`~!@#$%^&*()_+=-{}|\\][:;'/?><", "default"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i

		self.failUnlessEqual(encodedStr,
			Reform.HtmlAttributeEncode(toEncode, "default"), "Unicode characters to 6000")


	def testXmlEncode(self):
		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.",
			Reform.XmlEncode("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,."), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.XmlEncode("<>&\""), "Usual suspects")
		# Other characters
		self.failUnlessEqual("&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.XmlEncode("`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i
		
		self.failUnlessEqual(encodedStr,
			Reform.XmlEncode(toEncode), "Unicode characters to 6000")


	def testXmlEncodeDefault(self):
		self.failUnlessEqual("",
			Reform.XmlEncode(None, None), "None for both parameters")
		# Usual stuff
		self.failUnlessEqual("default",
			Reform.XmlEncode(None, "default"), "Checking default")

		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.",
			Reform.XmlEncode(None, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,."), "Non encoding chars via default")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.XmlEncode(None, "<>&\""), "Usual suspects via default")
		# Other characters
		self.failUnlessEqual("&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.XmlEncode(None, "`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation via default")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i

		self.failUnlessEqual(encodedStr,
			Reform.XmlEncode(None, toEncode), "Unicode characters to 6000 via default")

		# The following are sanity checks

		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.",
			Reform.XmlEncode("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.", "default"), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.XmlEncode("<>&\"", "default"), "Usual suspects")
		# Other characters
		self.failUnlessEqual("&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.XmlEncode("`~!@#$%^&*()_+=-{}|\\][:;'/?><", "default"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i

		self.failUnlessEqual(encodedStr,
			Reform.XmlEncode(toEncode, "default"), "Unicode characters to 6000")


	def testXmlAttributeEncode(self):
		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321",
			Reform.XmlAttributeEncode("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321"), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.XmlAttributeEncode("<>&\""), "Usual suspects")
		# Other characters
		self.failUnlessEqual("&#32;&#44;&#46;&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.XmlAttributeEncode(" ,.`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i

		self.failUnlessEqual(encodedStr,
			Reform.XmlAttributeEncode(toEncode), "Unicode characters to 6000")



	def testXmlAttributeEncodeDefault(self):
		self.failUnlessEqual("",
			Reform.XmlAttributeEncode(None, None), "None for both parameters")
		# Usual stuff
		self.failUnlessEqual("default",
			Reform.XmlAttributeEncode(None, "default"), "Checking default")

		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321",
			Reform.XmlAttributeEncode(None, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321"), "Non encoding chars via default")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.XmlAttributeEncode(None, "<>&\""), "Usual suspects via default")
		# Other characters
		self.failUnlessEqual("&#32;&#44;&#46;&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.XmlAttributeEncode(None, " ,.`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation via default")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i

		self.failUnlessEqual(encodedStr,
			Reform.XmlAttributeEncode(None, toEncode), "Unicode characters to 6000 via default")

		# The following are sanity checks

		# Non encoded characters
		self.failUnlessEqual("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321",
			Reform.XmlAttributeEncode("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321", "default"), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("&#60;&#62;&#38;&#34;",
			Reform.XmlAttributeEncode("<>&\"", "default"), "Usual suspects")
		# Other characters
		self.failUnlessEqual("&#32;&#44;&#46;&#96;&#126;&#33;&#64;&#35;&#36;&#37;&#94;&#38;&#42;&#40;&#41;&#95;&#43;&#61;&#45;&#123;&#125;&#124;&#92;&#93;&#91;&#58;&#59;&#39;&#47;&#63;&#62;&#60;",
			Reform.XmlAttributeEncode(" ,.`~!@#$%^&*()_+=-{}|\\][:;'/?><", "default"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&#%d;" % i

		self.failUnlessEqual(encodedStr,
			Reform.XmlAttributeEncode(toEncode, "default"), "Unicode characters to 6000")



	def testJsString(self):
		# Non encoded characters
		self.failUnlessEqual("'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.'",
			Reform.JsString("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,."), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("'\\x3C\\x3E\\x26\\x22\\x5C\\x27'",
			Reform.JsString("<>&\"\\'"), "Usual suspects")
		# Other characters
		self.failUnlessEqual("'\\x60\\x7E\\x21\\x40\\x23\\x24\\x25\\x5E\\x26\\x2A\\x28\\x29\\x5F\\x2B\\x3D\\x2D\\x7B\\x7D\\x7C\\x5C\\x5D\\x5B\\x3A\\x3B\\x27\\x2F\\x3F\\x3E\\x3C'",
			Reform.JsString("`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		encodedStr += "'"
		for i in range(128, 6000):
			toEncode += unichr(i)
			encodedStr += "\\u%04X" % i
			
		encodedStr += "'"
		self.failUnlessEqual(encodedStr,
			Reform.JsString(toEncode), "Unicode characters to 6000")



	def testJsStringDefault(self):
		self.failUnlessEqual("\'\'",
			Reform.JsString(None, None), "None for both parameters")
		# Usual stuff
		self.failUnlessEqual("'default'",
			Reform.JsString(None, "default"), "Checking default")

		# Non encoded characters
		self.failUnlessEqual("'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.'",
			Reform.JsString(None, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,."), "Non encoding chars via default")
		# Usual suspects
		self.failUnlessEqual("'\\x3C\\x3E\\x26\\x22\\x5C\\x27'",
			Reform.JsString(None, "<>&\"\\'"), "Usual suspects via default")
		# Other characters
		self.failUnlessEqual("'\\x60\\x7E\\x21\\x40\\x23\\x24\\x25\\x5E\\x26\\x2A\\x28\\x29\\x5F\\x2B\\x3D\\x2D\\x7B\\x7D\\x7C\\x5C\\x5D\\x5B\\x3A\\x3B\\x27\\x2F\\x3F\\x3E\\x3C'",
			Reform.JsString(None, "`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation via default")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		encodedStr += "'"
		for i in range(128, 6000):
			toEncode += unichr(i)
			encodedStr += "\\u%04X" % i

		encodedStr += "'"
		self.failUnlessEqual(encodedStr,
			Reform.JsString(None, toEncode), "Unicode characters to 6000 via default")

		# The following are sanity checks

		# Non encoded characters
		self.failUnlessEqual("'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.'",
			Reform.JsString("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.", "default"), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("'\\x3C\\x3E\\x26\\x22\\x5C\\x27'",
			Reform.JsString("<>&\"\\'", "default"), "Usual suspects")
		# Other characters
		self.failUnlessEqual("'\\x60\\x7E\\x21\\x40\\x23\\x24\\x25\\x5E\\x26\\x2A\\x28\\x29\\x5F\\x2B\\x3D\\x2D\\x7B\\x7D\\x7C\\x5C\\x5D\\x5B\\x3A\\x3B\\x27\\x2F\\x3F\\x3E\\x3C'",
			Reform.JsString("`~!@#$%^&*()_+=-{}|\\][:;'/?><", "default"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		encodedStr += "'"
		for i in range(128, 6000):
			toEncode += unichr(i)
			encodedStr += "\\u%04X" % i

		encodedStr += "'"
		self.failUnlessEqual(encodedStr,
			Reform.JsString(toEncode, "default"), "Unicode characters to 6000")


	def testVbsString(self):
		self.failUnlessEqual("\"abc\"&chrw(60)",
			Reform.VbsString("abc<"))
		self.failUnlessEqual("chrw(60)&\"abc\"",
			Reform.VbsString("<abc"))
		# Non encoded characters
		self.failUnlessEqual("\"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.\"",
			Reform.VbsString("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,."), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("chrw(60)&chrw(62)&chrw(38)&chrw(34)&chrw(92)&chrw(39)",
			Reform.VbsString("<>&\"\\'"), "Usual suspects")
		# Other characters
		self.failUnlessEqual("chrw(96)&chrw(126)&chrw(33)&chrw(64)&chrw(35)&chrw(36)&chrw(37)&chrw(94)&chrw(38)&chrw(42)&chrw(40)&chrw(41)&chrw(95)&chrw(43)&chrw(61)&chrw(45)&chrw(123)&chrw(125)&chrw(124)&chrw(92)&chrw(93)&chrw(91)&chrw(58)&chrw(59)&chrw(39)&chrw(47)&chrw(63)&chrw(62)&chrw(60)",
			Reform.VbsString("`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&chrw(%d)" % i

		encodedStr = encodedStr[1:] # remove &

		self.failUnlessEqual(encodedStr,
			Reform.VbsString(toEncode), "Unicode characters to 6000")



	def testVbsStringDefault(self):
		self.failUnlessEqual("\"\"", 
			Reform.VbsString(None, None), "None for both parameters")
		self.failUnlessEqual("\"abc\"&chrw(60)",
			Reform.VbsString(None, "abc<"))
		self.failUnlessEqual("chrw(60)&\"abc\"",
			Reform.VbsString(None, "<abc"))
		# Usual stuff
		self.failUnlessEqual("\"default\"",
			Reform.VbsString(None, "default"), "Checking default")

		# Non encoded characters
		self.failUnlessEqual("\"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.\"",
			Reform.VbsString(None, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,."), "Non encoding chars via default")
		# Usual suspects
		self.failUnlessEqual("chrw(60)&chrw(62)&chrw(38)&chrw(34)&chrw(92)&chrw(39)",
			Reform.VbsString(None, "<>&\"\\'"), "Usual suspects via default")
		# Other characters
		self.failUnlessEqual("chrw(96)&chrw(126)&chrw(33)&chrw(64)&chrw(35)&chrw(36)&chrw(37)&chrw(94)&chrw(38)&chrw(42)&chrw(40)&chrw(41)&chrw(95)&chrw(43)&chrw(61)&chrw(45)&chrw(123)&chrw(125)&chrw(124)&chrw(92)&chrw(93)&chrw(91)&chrw(58)&chrw(59)&chrw(39)&chrw(47)&chrw(63)&chrw(62)&chrw(60)",
			Reform.VbsString(None, "`~!@#$%^&*()_+=-{}|\\][:;'/?><"), "Punctuation via default")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&chrw(%d)" % i

		encodedStr = encodedStr[1:] # remove &
		self.failUnlessEqual(encodedStr,
			Reform.VbsString(None, toEncode), "Unicode characters to 6000 via default")

		# The following are sanity checks

		# Non encoded characters
		self.failUnlessEqual("\"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.\"",
			Reform.VbsString("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321 ,.", "default"), "Non encoding chars")
		# Usual suspects
		self.failUnlessEqual("chrw(60)&chrw(62)&chrw(38)&chrw(34)&chrw(92)&chrw(39)",
			Reform.VbsString("<>&\"\\'", "default"), "Usual suspects")
		# Other characters
		self.failUnlessEqual("chrw(96)&chrw(126)&chrw(33)&chrw(64)&chrw(35)&chrw(36)&chrw(37)&chrw(94)&chrw(38)&chrw(42)&chrw(40)&chrw(41)&chrw(95)&chrw(43)&chrw(61)&chrw(45)&chrw(123)&chrw(125)&chrw(124)&chrw(92)&chrw(93)&chrw(91)&chrw(58)&chrw(59)&chrw(39)&chrw(47)&chrw(63)&chrw(62)&chrw(60)",
			Reform.VbsString("`~!@#$%^&*()_+=-{}|\\][:;'/?><", "default"), "Punctuation")
		# Unicode characters
		toEncode = u''
		encodedStr = ''
		for i in range(127, 6000):
			toEncode += unichr(i)
			encodedStr += "&chrw(%d)" % i

		encodedStr = encodedStr[1:] # remove &
		self.failUnlessEqual(encodedStr,
			Reform.VbsString(toEncode, "default"), "Unicode characters to 6000")


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(ReformUnittest)
	unittest.TextTestRunner(verbosity=2).run(suite)

# end
