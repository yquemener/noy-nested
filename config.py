#!/usr/bin/env python
# -*- coding: utf-8

from tornado.options import define, options

define("port", default=8888, type=int)
define("facebook_api_key", help="your Facebook application API key",
                           default="1408863776041585")

define("facebook_secret", help="your Facebook application secret",
                          default="056d1d09366b04aaf82d307124dc852f")

define("home_url", help="The URL the website will be at", 
                   default="http://localhost:8888")  
 
define("cookie_secret", help="Some entropy for the cookie_secret", 
                   default="Hé, tu sais quoi? je afdsqrwvais me le générer àl an,tn i pour l'entropie156851huguyfcvbnnjqdjsknbhgyuhjb")
 
