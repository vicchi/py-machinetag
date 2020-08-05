import re
import types

def from_string(string, **kwargs):
    return machinetag(string, None, None, **kwargs)

def from_triple(ns, pred, value, **kwargs):
    return machinetag(ns, pred, value, **kwargs)

class sanitize:

    def __init__ (self):

        self.ns_filter = r'[^a-zA-Z0-9_]+'
        self.pred_filter = r'[^a-zA-Z0-9_]+'
        self.value_filter = None

    def __filter__(self, v, p):

        if p:
            v = re.sub(p, '', v)

        return v

    def prepare_namespace(self, ns):
        return ns

    def prepare_predicate(self, pred):
        return pred

    def prepare_value(self, value):
        return value

    def filter_namespace(self, ns):
        ns = self.prepare_namespace(ns)
        return self.__filter__(ns, self.ns_filter)

    def filter_predicate(self, pred):
        pred = self.prepare_predicate(pred)
        return self.__filter__(pred, self.pred_filter)

    def filter_value(self, value):
        value = self.prepare_predicate(value)
        return self.__filter__(value, self.value_filter)

class machinetag :
    """Object methods to parse and inspect machine tags

    from machinetag.common import machinetag

    str_mt = "flickr:user=straup"

    mt1 = machinetag(str_mt)

    if mt1.is_machinetag() :
        print("MT1 : %s" % mt1)
        print("MT1 namespace : %s" % mt1.namespace())

    mt2 = machinetag("aero", "airport", "SFO")

    if mt2.is_machinetag() :
        print("MT2 : %s" % mt2)
        print("MT2 : is numeric %s" % mt2.is_numeric())

    mt3 = machinetag("temp", "celcius", 20)

    if mt3.is_machinetag() :
        print("MT3 : %s" % mt3)
        print("MT3 : is numeric %s" % mt3.is_numeric())
        print("MT3 : type %s" % type(mt3.value()))

    mt4 = machinetag("geo:lat=24.234")

    if mt4.is_machinetag() :
        print("MT4 : %s" % mt4)
        print("MT4 : is numeric %s" % mt4.is_numeric())
        print("MT4 : type %s" % type(mt4.value()))
    """

    def __init__ (self, ns_or_tagraw, pred=None, value=None, **kwargs) :
        """Parse a raw tag, or the component parts of machine tag and return a machine tag object"""
        self.__namespace__ = None
        self.__predicate__ = None
        self.__value__ = None
        self.__ismachinetag__ = False
        self.__iswildcard__ = False
        self.__isnumeric__ = False

        allow_wildcards = kwargs.get('allow_wildcards', False)

        if pred :

            re_nspred = re.compile(r"^([a-z](?:[a-z0-9_]+))$", re.IGNORECASE)
            re_nspred_wildcard = re.compile(r"^((?:[a-z](?:[a-z0-9_]+))|\*)$", re.IGNORECASE)

            if re_nspred.match(ns_or_tagraw) and re_nspred.match(pred) and value :
                self.__namespace__ = ns_or_tagraw
                self.__predicate__ = pred
                self.__value__ = value
                
            elif allow_wildcards:

                ns_m = re_nspred_wildcard.findall(ns_or_tagraw)
                pred_m = re_nspred_wildcard.findall(pred)

                if ns_m and pred_m :

                    if ns_m[0][0] != '*':
                        self.__namespace__ = ns_or_tagraw

                    if pred_m[0][0] != '*':
                        self.__predicate__ = pred

                    if value != '*' and value != '':
                        self.__value__ = value

                if self.__namespace__ != None or self.__predicate__ != None or self.__value__ != None:
                    self.__iswildcard__ = True
                    
            else:
                pass

        else :

            re_tag = re.compile(r"^([a-z](?:[a-z0-9_]+))\:([a-z](?:[a-z0-9_]+))\=(.+)$", re.IGNORECASE)
            re_tag_wildcard = re.compile(r"^((?:[a-z](?:[a-z0-9_]+))|\*)\:((?:[a-z](?:[a-z0-9_]+))|\*)\=(.*)$", re.IGNORECASE)

            m = re_tag.findall(ns_or_tagraw)

            if m :
                self.__namespace__ = m[0][0]
                self.__predicate__ = m[0][1]
                self.__value__ = m[0][2]
                
            elif allow_wildcards and not ns_or_tagraw in ('*:*=', '*:*=*'):

                m = re_tag_wildcard.findall(ns_or_tagraw)

                if m :

                    self.__iswildcard__ = True

                    if m[0][0] != '*':
                        self.__namespace__ = m[0][0]

                    if m[0][1] != '*':
                        self.__predicate__ = m[0][1]

                    if m[0][2] != '*' and m[0][2] != '':
                        self.__value__ = m[0][2]

                if self.__namespace__ != None or self.__predicate__ != None or self.__value__ != None:
                    self.__iswildcard__ = True

            else:
                pass

        if self.__namespace__ and self.__predicate__ and self.__value__ :
            self.__ismachinetag__ = True

        elif self.__iswildcard__:
            self.__ismachinetag__ = True

        else:
            pass

        if self.__ismachinetag__ and self.__value__ != None:

            valtype = type(self.__value__)

            if valtype == types.IntType or valtype == types.FloatType :
                self.__isnumeric__ = True
            else :
                re_num = re.compile(r"^-?\d+(\.\d+)?$", re.IGNORECASE)
                m = re_num.findall(self.__value__)

                if m :

                    self.__isnumeric__ = True

                    if m[0] :
                        self.__value__ = float(self.__value__)
                    else :
                        self.__value__ = int(self.__value__)

    #

    def __str__ (self) :
        """Returns the object as formatted machine tag string"""

        return self.as_string()

    #

    def __unicode__ (self) :
        """Returns the object as formatted machine tag string"""

        return self.as_string()

    #

    def is_machinetag (self) :
        """Returns true or false depending on whether or not the arguments
        passed to the constructor were able to be parsed as a machine tag"""

        return self.__ismachinetag__

    def is_wildcard_machinetag (self) :

        return self.__iswildcard__

    #

    def is_numeric (self) :
        """Returns true or false depending on whether or not the machine tag
        object's value is an integer or a float"""

        return self.__isnumeric__ 

    #

    def namespace (self) :
        """Returns a string containing the machine tag object's namespace"""

        return self.__namespace__

    #

    def predicate (self) :
        """Returns a string containing the machine tag object's predicate"""

        return self.__predicate__

    #

    def value (self) :
        """Returns a string -- or if the value is numeric an integer or float --
        containing the machine tag object's value"""

        return self.__value__

    #

    def as_string (self) :
        """Returns the object as formatted machine tag string"""

        if self.is_wildcard_machinetag():

            ns = self.namespace()
            pred = self.predicate()
            value = self.value()

            if ns == None:
                ns = "*"
            
            if pred == None:
                pred = "*"

            if value == None:
                value = ""

            return "%s:%s=%s" % (ns, pred, value)

        if self.is_machinetag() :

            return "%s:%s=%s" % (self.namespace(), self.predicate(), self.value())

    #

    def magic_8s(self):

        if self.is_wildcard_machinetag():
            raise Exception("magic_8s not supported for wildcard machinetags")

        ns = self.namespace()
        pred = self.predicate()
        value = self.value()

        parts = [
            '%s:' % ns,
            '%s:%s=' % (ns, pred),
            '%s:%s=%s' % (ns, pred, value),
            '=%s' % value,
            ':%s=' % pred,
            '%s=%s' % (pred, value)
            ]

        return map(self.encode_magic_8s, parts)

    def encode_magic_8s(self, str):

        str = str.replace('8', '88')
        str = str.replace(':', '8c')
        str = str.replace('=', '8e')
        str = str.replace('_', '8u')

        return str

    def decode_magic_8s(self, str):

        str = str.replace('8u', '_')
        str = str.replace('8e', '=')
        str = str.replace('8c', ':')
        str = str.replace('88', '8')

        return str

if __name__ == "__main__" :

    str_mt = "flickr:user=straup"

    mt1 = machinetag(str_mt)

    if mt1.is_machinetag() :
        print("MT1 : %s" % mt1)
        print("MT1 namespace : %s" % mt1.namespace())

    mt2 = machinetag("aero", "airport", "SFO")

    if mt2.is_machinetag() :
        print("MT2 : %s" % mt2)
        print("MT2 : is numeric %s" % mt2.is_numeric())

    mt3 = machinetag("temp", "celcius", 20)

    if mt3.is_machinetag() :
        print("MT3 : %s" % mt3)
        print("MT3 : is numeric %s" % mt3.is_numeric())
        print("MT3 : type %s" % type(mt3.value()))

    mt4 = machinetag("geo:lat=24.234")

    if mt4.is_machinetag() :
        print("MT4 : %s" % mt4)
        print("MT4 : is numeric %s" % mt4.is_numeric())
        print("MT4 : type %s" % type(mt4.value()))

    for p in mt1.magic_8s():
        print("lazy 8s encoded: %s decoded: %s" % (p, mt1.decode_magic_8s(p)))
