#!/usr/bin/env python
 
import httplib2

h = httplib2.Http()
r, content = h.request("http://google.com")

print content[0:100]