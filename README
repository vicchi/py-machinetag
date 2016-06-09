# py-machinetag

## Usage

```
NAME
    machinetag

FILE
    machinetag/machinetag/__init__.py

CLASSES
    machinetag
    
    class machinetag
     |  Object methods to parse and inspect machine tags
     |  
     |  from machinetag import machinetag
     |  
     |  str_mt = "flickr:user=straup"
     |  
     |  mt1 = machinetag(str_mt)
     |  
     |  if mt1.is_machinetag() :
     |      print "MT1 : %s" % mt1
     |      print "MT1 namespace : %s" % mt1.namespace()
     |  
     |  mt2 = machinetag("aero", "airport", "SFO")
     |  
     |  if mt2.is_machinetag() :
     |      print "MT2 : %s" % mt2
     |      print "MT2 : is numeric %s" % mt2.is_numeric()
     |      
     |  mt3 = machinetag("temp", "celcius", 20)
     |  
     |  if mt3.is_machinetag() :
     |      print "MT3 : %s" % mt3
     |      print "MT3 : is numeric %s" % mt3.is_numeric()
     |      print "MT3 : type %s" % type(mt3.value())
     |      
     |  mt4 = machinetag("geo:lat=24.234")
     |  
     |  if mt4.is_machinetag() :
     |      print "MT4 : %s" % mt4
     |      print "MT4 : is numeric %s" % mt4.is_numeric()
     |      print "MT4 : type %s" % type(mt4.value())
     |  
     |  Methods defined here:
     |  
     |  machinetag(self, ns_or_tagraw, pred=None, value=None)
     |      Parse a raw tag, or the component parts of machine tag and return a machine tag object
     |  
     |  __str__(self)
     |      Returns the object as formatted machine tag string
     |  
     |  __unicode__(self)
     |      Returns the object as formatted machine tag string
     |  
     |  as_string(self)
     |      Returns the object as formatted machine tag string
     |  
     |  is_machinetag(self)
     |      Returns true or false depending on whether or not the arguments
     |      passed to the constructor were able to be parsed as a machine tag
     |  
     |  is_numeric(self)
     |      Returns true or false depending on whether or not the machine tag
     |      object's value is an integer or a float
     |  
     |  namespace(self)
     |      Returns a string containing the machine tag object's namespace
     |  
     |  predicate(self)
     |      Returns a string containing the machine tag object's predicate
     |  
     |  value(self)
     |      Returns a string -- or if the value is numeric an integer or float --
     |      containing the machine tag object's value
```
