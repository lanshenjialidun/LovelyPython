# HTMLStream test

import HIP

H=HIP.HTMLStream()

aDict={"one":"unan","two":"daou","three":"tri"}
H + aDict - type(aDict) + '<p>'

H + "Types<br>"
for v in [HIP,HIP.HTMLStream,H]:
    H - v - type(v) +"<br>"

